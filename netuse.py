#!/usr/bin/python3

"""

Calculate internet usage from log files created
by a custom script.

While on windows, I had Networx monitor which used
to take care of everything but now I've been forced
to write my custom shit.

"""

import sys
import os

join = os.path.join

# Used for suggested internet usage calculation
from datetime import date, timedelta
from calendar import month_abbr as months

################################################################

# Convert string to integer, empty string is zero.
to_int = lambda s: int(s) if s.strip() else 0

# Starting period
# 'Date/Month'
Start_Period = "25/01/2015"

# Recharge this month
# (in MBs)
Total_Data = 7 * 1024

# Difference between epochs of data points
# (in seconds)
Epoch_Diff = 10 * 60 + 5

# Folder where log files are stored
Logfiles_Path = os.path.expanduser("~/.net/")

################################################################


MB = 1024 * 1024

s_day, s_month, s_year = map(int, Start_Period.split("/"))


def gen_file_list():
    """ Generate a list of files to read in. """

    down_filelist = []
    up_filelist = []

    # Read in data from files and build a list
    for month in months[s_month:]:

        # Break when month doesn't yet exist
        if not os.path.isdir(join(Logfiles_Path, month)):
            break

        print("%s: " % month, end='')

        down_path = join(Logfiles_Path, month, "down")
        up_path = join(Logfiles_Path, month, "up")

        if month == months[s_month]:
            days = range(s_day, 32)
        else:
            days = range(1, 32)

        for day in days:
            day = "%02d" % day

            # Skip when day doesn't exist
            if not os.path.isfile(join(down_path, day)):
                continue

            print("%s, " % day, end='')

            # Read in the up/down logs
            down_filelist.append(join(down_path, day))
            up_filelist.append(join(up_path, day))

        print('\n')

    return down_filelist, up_filelist


def read_files(files):
    """ Read files and generate tuples of (data,epoch). """

    lst = []

    for _file in files:
        with open(_file) as f:
            lst.extend([tuple(map(to_int, s.split(";")))
                        for s in f.readlines()])

    return lst


def calculate(lst):
    """ Calculate actual data usage from the list of tuples. """

    total = 0
    previous = (0, 0)

    for current in lst:

        # Some of the data has no epoch entries
        # only byte usage for that day
        if len(current) == 1:
            total += current[0]
            continue

        usage = current[0] - previous[0]
        duration = current[1] - previous[1]

        if duration <= Epoch_Diff:
            if usage >= 0:
                total += usage
            else:
                total += current[0]
        else:
            total += current[0]

        previous = current

    return total


def month():
    """ Print stats for the current month. """

    down_filelist, up_filelist = gen_file_list()

    total_download = calculate(read_files(down_filelist)) // MB
    total_upload = calculate(read_files(up_filelist)) // MB

    data_left = Total_Data - total_download

    start_date = date(s_year, s_month, s_day)
    end_date = start_date + timedelta(days=30)
    days_left = (end_date - date.today()).days

    suggested = data_left // days_left

    output = (
        "Downloaded:\t%4d MB \n"
        "Uploaded:\t%4d MB \n\n"
        "Data Left:\t%4d MB \n"
        "Days Left:\t%4d Days \n\n"
        "Suggested:\t%4d MB (Per Day) \n"
    ) % (total_download, total_upload, data_left, days_left, suggested)

    print(output)


def today():
    t = date.today()

    path = join(Logfiles_Path, t.strftime('%b'), "%s", t.strftime('%d'))

    download = calculate(read_files([path % "down"])) // MB
    upload = calculate(read_files([path % "up"])) // MB

    output = (
        "Downloaded:\t%4d MB \n"
        "Uploaded:\t%4d MB \n"
    ) % (download, upload)

    print(output)


if __name__ == '__main__':

    if '-t' in sys.argv:
        today()
    else:
        month()
