#!/bin/bash
echo "Noise Suppression filter starting..."
echo "nginx: starting up nginx..."
/usr/local/nginx/sbin/nginx
echo "nginx is running..."
start_function() {
    export SOURCE_AUDIO_URL="$(getent hosts $SOURCE_AUDIO_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_AUDIO_PORT"
    echo "exported url of source audio: $SOURCE_AUDIO_URL"
    #Start the Noise Suppression filter
    ffmpeg -re -i "rtmp://$SOURCE_AUDIO_URL/live/audio" -af "arnndn=m=/noisesuppress/cb.rnnn" -f flv rtmp://localhost/live/audio
    # Reduce noise from audio using Reccurent Neural Network
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
while true; do :; done
