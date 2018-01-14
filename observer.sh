#!/bin/sh
# add this script to crontab ($crontab -e) to run it on startup
python3 main.py >> systemlog.log 2>&1;
