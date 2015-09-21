# Network Data Usage

While on Windows, I used [Networx](https://www.softperfect.com/products/networx/) to track my bandwidth usage, but I couldn't find anything similar for Linux so I created my own little thing -it's far from perfect, but it works!

![Screenshot](screenshot.png)

## Design

The application has two parts actually, a bash script that runs as a cron job and dumps transferred bytes to files, and a Python script that processes the files to generate cumulative statistics like Total data downloaded/uploaded, Data Left and Suggested Usage.

## Installation

```bash
git clone https://github.com/dufferzafar/netuse ~/Downloads

sudo ln ~/Downloads/netuse/netuse.py /usr/bin/netuse
sudo chmod +x /usr/bin/netuse

cp ~/Downloads/netuse/config.py.example ~/Downloads/netuse/config.py

crontab -e
```

`*/10 * * * * ~/Downloads/netuse/dumper`

## Todo

* Make this, the data dumping cron job and a network usage appindicator all a part of a single big application.
