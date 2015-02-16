#!/usr/bin/python3

"""

Calculate internet usage from log files created
by a custom script.

While on windows, I had Networx monitor which used
to take care of everything but now I've been forced
to write my custom shit.

"""

import os
join = os.path.join

# Used for suggested internet usage calculation
from datetime import date

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
Epoch_Diff = 10 * 60

# Folder where log files are stored
Logfiles_Path = os.path.expanduser("~/.net/")

################################################################

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dev"]

s_day, s_month, s_year = map(int, Start_Period.split("/"))

download_list = []
upload_list = []

# Read in data from files and build a list
for month in months[s_month - 1:]:

    # Break when month doesn't yet exist
    if not os.path.isdir(join(Logfiles_Path, month)):
        break

    print("%s: " % month, end='')

    down_path = join(Logfiles_Path, month, "down")
    up_path = join(Logfiles_Path, month, "up")

    if month == months[s_month - 1]:
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
        with open(join(down_path, day)) as f:
            download_list.extend([tuple(map(to_int, s.split(";")))
                                  for s in f.readlines()])

        with open(join(up_path, day)) as f:
            upload_list.extend([tuple(map(to_int, s.split(";")))
                                for s in f.readlines()])

    print('\n')


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
            if usage > 0:
                total += usage
            else:
                total += current[0]
        else:
            total += current[0]

        previous = current

    return total


total_download = calculate(download_list) // 1024 * 1024
total_upload = calculate(upload_list) // 1024 * 1024

data_left = Total_Data - total_download
days_left = date(s_year, s_month+1, s_day) - date.today()

suggested = data_left // days_left.days

output = \
"""\
Downloaded:\t%4d MB
Uploaded:\t%4d MB

Data Left:\t%4d MB

Suggested:\t%4d MB (Per Day)
""" % (total_download, total_upload, data_left, suggested)

print(output)
