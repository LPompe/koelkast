#!/bin/sh -
until python /home/pi/git/koelkast/processmanager.py > /data/logs/cameralog; do
    echo "Main program loop crashed $?.  Respawning.." >&2 >> /data/logs/systemlog.log
    echo "Main program loop crashed $?.  Respawning.." >&2
    python /home/pi/git/koelkast/rollbar_report.py $?
    sleep 10
done
