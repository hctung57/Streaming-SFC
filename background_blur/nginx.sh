#!/bin/bash
echo "nginx: starting up nginx..."
/usr/local/nginx/sbin/nginx
echo "nginx is running..."
export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"
echo "exported url of source streaming: $SOURCE_RTMP_URL"
echo "starting background blur func..."

python3 fake.py --webcam-path $SOURCE_RTMP_URL --no-foreground --no-background

while true
do :
exit_status=$?
if [ "${exit_status}" -eq 0 ];
then
    echo "Regenerate service ip address..."
    export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"
    echo "exported url of source streaming: $SOURCE_RTMP_URL"
    echo "Restarting background blur func..."
    python3 fake.py --webcam-path $SOURCE_RTMP_URL --no-foreground --no-background
fi
sleep 1
done
# Just a loop to keep the container running
while true; do :; done