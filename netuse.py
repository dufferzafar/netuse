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

# Convert string to integer, empty string is zero.
to_int = lambda s: int(s) if s.strip() else 0

# Starting period
# 'Date/Month'
Start_Period = "25/1"

# Recharge this month
# (in MBs)
Total_Data = 10 * 1024

# Folder where log files are stored
Logfiles_Path = os.path.expanduser("~/.net/")

################################################################

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dev"]

start_day, start_month = map(int, Start_Period.split("/"))


download = []
upload = []

for month in months[start_month - 1:]:

    # Break when month doesn't yet exist
    if not os.path.isdir(join(Logfiles_Path, month)):
        break

    print("---- %s ----" % month)

    down_path = join(Logfiles_Path, month, "down")
    up_path = join(Logfiles_Path, month, "up")

    if month == months[start_month - 1]:
        days = range(start_day, 32)
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
            download.extend([tuple(map(to_int, s.split(";")))
                             for s in f.readlines()])

        with open(join(up_path, day)) as f:
            upload.extend([tuple(map(to_int, s.split(";")))
                           for s in f.readlines()])

    print('\n')

# print(download)
