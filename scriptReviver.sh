#!/bin/sh -
until python /home/pi/git/koelkast/processmanager.py > /data/logs/cameralog; do
    echo "Main program loop crashed $?.  Respawning.." >&2 >> /data/logs/systemlog.log
    echo "Main program loop crashed $?.  Respawning.." >&2
    sleep 10
done
