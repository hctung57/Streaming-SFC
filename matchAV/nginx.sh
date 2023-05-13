#!/bin/bash
echo "nginx: starting up nginx..."
/usr/local/nginx/sbin/nginx
echo "nginx is running..."
start_function() {
    export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"
    echo "exported url of source streaming: $SOURCE_RTMP_URL"
    export SOURCE_AUDIO_URL="$(getent hosts $SOURCE_AUDIO_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_AUDIO_PORT"
    echo "exported url of source audio: $SOURCE_AUDIO_URL"
    ffmpeg -re -analyzeduration 1 -probesize 32 -i "rtmp://$SOURCE_RTMP_URL/live/stream" -itsoffset $DELAY_AUDIO_VIDEO_TIME -analyzeduration 1 -probesize 32 -i "rtmp://$SOURCE_AUDIO_URL/live/audio" -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 -f flv rtmp://localhost/live/stream
    # ffmpeg -re -i "rtmp://$SOURCE_AUDIO_URL/live/audio" -itsoffset $DELAY_AUDIO_VIDEO_TIME -i "rtmp://$SOURCE_RTMP_URL/live/stream" -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 -f flv rtmp://localhost/live/stream -loglevel quiet -stats 2> app.log
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
# Just a loop to keep the container running
while true; do :; done