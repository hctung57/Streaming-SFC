#!/bin/bash
echo "nginx: starting up nginx..."
/usr/local/nginx/sbin/nginx
echo "nginx is running..."
start_function() {
    export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"
    echo "exported url of source streaming: $SOURCE_RTMP_URL"
    export SOURCE_AUDIO_URL="$(getent hosts $SOURCE_AUDIO_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_AUDIO_PORT"
    echo "exported url of source audio: $SOURCE_AUDIO_URL"
    ffmpeg -re -i "rtmp://$SOURCE_AUDIO_URL/live/audio" -itsoffset $DELAY_AUDIO_VIDEO_TIME -i "rtmp://$SOURCE_RTMP_URL/live/stream" -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 -f flv rtmp://localhost/live/stream
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