#!/usr/bin/python3

"""
Calculate internet usage from log files created by a custom script.

Can also display stats like suggested usage, weekly report etc.
"""

import os
import sys

# Used for calculating suggested and hourly internet usage
from datetime import date, timedelta, datetime

# Print bar charts to terminal
# Not a module on PyPI
import termgraph

# A tiny wrapper over notify-send
# Not a module on PyPI
import notify

# Load settings from config file
# See file 'config.py.example' for what the settings mean.
from config import (
    START_DATE,
    DAYS_IN_MONTH,
    TOTAL_DATA,
    EPOCH_DIFF,
    CORRECTION_FACTOR,
    LOGFILES_PATH,
)

# How many bytes in an MB?
MB = 1024 * 1024

# Ideally, these values shouldn't be globals but passed around to functions!
s_day, s_month, s_year = map(int, START_DATE.split("/"))

# not (Explicit is better than implicit)
join = os.path.join


def gen_file_list():
    """Generate a list of 'monthly' files to read in.
    :returns: down_filelist, up_filelist

    """

    down_filelist = []
    up_filelist = []

    start_date = date(s_year, s_month, s_day)
    end_date = date.today()

    for din in daterange(start_date, end_date):
        down_path = join(LOGFILES_PATH, str(din.year),
                                                   din.strftime('%b'), "down")
        up_path = join(LOGFILES_PATH, str(din.year), din.strftime('%b'), "up")

        day = "%02d" % din.day

        # Skip when day doesn't exist
        if not os.path.isfile(join(down_path, day)):
            continue

        down_filelist.append(join(down_path, day))
        up_filelist.append(join(up_path, day))

    return down_filelist, up_filelist


def read_files(files):
    """Read files and generate tuples of (data, epoch).
    :returns: tuples

    """

    tuples = []

    for _file in files:
        with open(_file) as f:
            tuples.extend([tuple(map(to_int, s.split(";")))
                           for s in f.readlines()])

    return tuples


def calculate(tuples):
    """Calculate actual data usage from the list of tuples.
    :returns: total

    """

    total = 0
    previous = tuples[0]

    for current in tuples[1:]:

        # Some of the data has no epoch entries
        # only byte usage for that day
        if len(current) == 1:
            total += current[0]
            continue

        usage = current[0] - previous[0]
        duration = current[1] - previous[1]

        if duration <= EPOCH_DIFF and usage >= 0:
            total += usage
        else:
            total += current[0]

        previous = current

    return total


def calculate_monthly_stats():
    """Calculate stats for the current month.
    :returns: total_down, total_up, data_left,
              days_left, end_date, suggested

    """
    down_filelist, up_filelist = gen_file_list()

    total_down = calculate(read_files(down_filelist)) // MB
    total_down += correction(total_down)

    total_up = calculate(read_files(up_filelist)) // MB

    data_left = TOTAL_DATA - total_down - total_up

    start_date = date(s_year, s_month, s_day)
    end_date = start_date + timedelta(days=DAYS_IN_MONTH)

    days_left = (end_date - date.today()).days
    suggested = data_left // days_left

    return total_down, total_up, data_left, days_left, end_date, suggested


def monthly():
    """Print the monthly stats month.
    :returns: None
    
    """

    output = [
        "Downloaded:\t%4d MB",
        "Uploaded:\t%4d MB\n",
        "Data Left:\t%4d MB",
        "Days Left:\t%4d Days",
        "End Date:\t%s (11:59 PM)\n",
        "Suggested:\t%4d MB (Per Day)",
    ]

    print("\n".join(output) % calculate_monthly_stats())


def daily(t=date.today()):
    """Print stats for a single day, default today.
    :returns: None

    """

    # Path of day's file
    path = join(LOGFILES_PATH, t.strftime('%G'), t.strftime('%b'),
                                                       "%s", t.strftime('%d'))

    down = calculate(read_files([path % "down"])) // MB
    up = calculate(read_files([path % "up"])) // MB

    output = (
        "Downloaded:\t%4d MB \n"
        "Uploaded:\t%4d MB \n"
    ) % (down, up)

    print(output)


def weekly():
    """ Use termgraph to plot usage of this week. Data is 
    aggregated according to days.
    :returns: None


    """

    # Get this month's file list
    down_filelist, _ = gen_file_list()

    # Iterate over every file in this week
    week = {}
    for file in down_filelist[-7:]:
        week[file.split('/')[-1]] = calculate(read_files([file])) // MB

    data = sorted(week.items())

    print("Data downloaded this week:\n")
    termgraph.chart(
        labels=["%s%s" % (d[0], ordinal_suffix(int(d[0]))) for d in data],
        data=[d[1] for d in data],
        args=dict(
            width=30,
            suffix=" MB",
            format="{:>5.0f}",
        )
    )

    print("Total: %d MB" % sum([d[1] for d in data]))


def hourly():
    """Calculate usage of last hour.
    :returns: hourly_usage
    
    """

    # Read today's file
    t = date.today()
    path = join(LOGFILES_PATH, t.strftime('%G'), t.strftime('%b'), "%s", t.strftime('%d'))
    tuples = read_files([path % "down"])

    # Calculate timestamp of an hour ago
    hour_ago = datetime.now() - timedelta(hours=1)
    hour_ago_ts = int(hour_ago.strftime("%s"))

    # Only keep tuples of the last hour
    # whose timestamp is greater than last hour stamp
    tuples = [t for t in tuples if t[1] > hour_ago_ts]

    hourly_usage = calculate(tuples) // MB

    return hourly_usage


def noti():
    """Send notification about usage and the data remaining.
    :returns: None

    """

    _, _, data_left, _, _, suggested = calculate_monthly_stats()

    # TODO: If end date is today, add a line about that too
    # or maybe a custom alert?

    title = "Remaining Data: %d MB" % data_left
    body = "\n".join([
        "You've downloaded %d MB in the last hour.",
        "Suggested usage is %d MB per day."
    ]) % (hourly(), suggested)

    notify.send(title, body)

# ================================================================ Helper functions


def ordinal_suffix(d):
    """ Return ordnial suffixes for an integer.
    Taken from: http://stackoverflow.com/a/5891598/2043048
    """
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def to_int(s):
    """Convert string to integer, empty string is zero."""
    if s.strip() and s.strip('\0'):
        return int(s)
    else:
        return 0


def daterange(start_date, end_date):
    """Iterate over a range of dates. Both ends inclusive.
    :returns: generator 
    
    """
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def correction(n):
    """
    For reasons I can't comprehend, the results are wrong.

    My results differ significantly from what MTS shows me.

    The correction factor, if it exists, will depend on, the
    total data that has been downloaded till now.

    This is a really crude hack - I have no idea what I am doing.
    """
    return n * CORRECTION_FACTOR


# If I am being called directly (rather than being imported)
if __name__ == '__main__':

    # FIXME: Replace this with something 'real' like docopt/click
    if '-t' in sys.argv:
        daily()
    elif '-w' in sys.argv:
        weekly()
    elif '-h' in sys.argv:
        print("Data downloaded in the last hour: %d MB" % hourly())
    elif '-n' in sys.argv:
        noti()
    else:
        monthly()
