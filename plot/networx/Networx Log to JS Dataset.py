from datetime import datetime as DT
import xml.etree.ElementTree as ET
import glob

# The output db
opFile = open("dataset.js", "w")
opFile.write("var time = [];")
opFile.write("\nvar upload = [];")
opFile.write("\nvar download = [];")
opFile.write("\n\n")

# Slick 2D Array creation
time = [([0] * 32) for i in range(0, 13)];
upload = [([0] * 32) for i in range(0, 13)];
download = [([0] * 32) for i in range(0, 13)];

# Current Log File
for fileName in glob.glob("XML\*.xml"):

    # Build a parse tree
    tree = ET.parse(fileName).find("dialup")

    # Let's Rock This Show!!
    for item in tree.findall("item"):

        conName = item.find("connection").text

        # The other connections were 'free internet'
        if conName != "MBlaze USB Modem":
            continue

        since = item.find("since").text
        sessStart = DT.strptime(since, "%Y-%m-%d %H:%M:%S")
        # sessDuration = timedelta(seconds=int(dur))

        # Read data
        time[sessStart.date().month][sessStart.date().day] += int(item.find("duration").text)
        upload[sessStart.date().month][sessStart.date().day] += int(item.find("out").text)
        download[sessStart.date().month][sessStart.date().day] += int(item.find("in").text)

# Write Output to file.
for i in range(1, 13):
    opFile.write("time[" + str(i) + "] = " + str(time[i]) + ";")
    opFile.write("\nupload[" + str(i) + "] = " + str(upload[i]) + ";")
    opFile.write("\ndownload[" + str(i) + "] = " + str(download[i]) + ";")
    opFile.write("\n\n")

opFile.close()
