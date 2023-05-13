#!/bin/bash
echo "nginx: starting up nginx..."
/usr/local/nginx/sbin/nginx
echo "nginx is running..."
start_function() {
    export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"
    echo "exported url of source streaming: $SOURCE_RTMP_URL"
    echo "getting source streaming information..."
    sourceVideoStreamWidth=$(ffmpeg -i rtmp://$SOURCE_RTMP_URL/live/stream 2>&1 | grep 'displayWidth'| tr -dc '0-9')
    sourceVideoStreamHeight=$(ffmpeg -i rtmp://$SOURCE_RTMP_URL/live/stream 2>&1 | grep 'displayHeight'| tr -dc '0-9')
    if [ -z "$RESOLUTION" ];
    then 
        resolution=$sourceVideoStreamWidth"x"$sourceVideoStreamHeight           
        echo "Resolution value not found in setting. Using default setting "$resolution
        ffmpeg -re -analyzeduration 1 -probesize 32 -i "rtmp://$SOURCE_RTMP_URL/live/stream" -s "$resolution" -f flv rtmp://localhost/live/stream -loglevel quiet -stats 2> app.txt
    else
        if [ "$sourceVideoStreamWidth" != "" ]; then
            widthStream=$(($sourceVideoStreamWidth*$RESOLUTION/$sourceVideoStreamHeight))
            if [ $widthStream%2!=0 ]; 
            then
                widthStream=$((widthStream+1))
            fi
            resolution=$widthStream"x"$RESOLUTION
            echo "Setting resolution of streaming to" $resolution
            ffmpeg -re -analyzeduration 1 -probesize 32 -i "rtmp://$SOURCE_RTMP_URL/live/stream" -s "$resolution" -f flv rtmp://localhost/live/stream -loglevel quiet -stats 2> app.txt
        fi
    fi
    return
}
start_function
while true
do :
exit_status=$?
if [ "${exit_status}" -eq 0 ];
then
    start_function
fi
sleep 1
done
# 1920x1080p(FHD) = 2200kb
# 1280x720p(HD) = 1100kb
# 854x480p(SD)= 700kb 
# 640x360p=500kb 
# Just a loop to keep the container running
while true; do :; done