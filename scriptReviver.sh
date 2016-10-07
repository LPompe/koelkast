until python processmanager.py > /data/logs/cameralog 1>&2 &; do
    echo "Main program loop crashed $?.  Respawning.." >&2 >> /data/logs/systemlog.log
    sleep 10
done
