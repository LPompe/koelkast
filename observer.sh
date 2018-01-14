#!/bin/sh
# add this script to crontab ($crontab -e) to run it on startup
until python3 main.py >> systemlog.log 2>&1; do
    echo "Main program loop crashed $?.  Respawning.." >&2 >> systemlog.log
    echo "Main program loop crashed $?.  Respawning.." >&2
    sleep 10
done


