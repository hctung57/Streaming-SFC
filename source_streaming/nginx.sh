#!/bin/bash
echo "nginx: starting up nginx..."
/usr/local/nginx/sbin/nginx
echo "nginx is running..."
# ffmpeg -re -stream_loop -1  -i "test.mp4"  -r 30 -s 1920x1080 -f flv rtmp://localhost/live/stream
ffmpeg -re -stream_loop -1  -i "test.mp4"  -r 30 -s 1920x1080 -map 0:a -f flv "rtmp://localhost/live/audio" -map 0:v -f flv "rtmp://localhost/live/stream"
# 1920x1080p(FHD) = 2200kb
# 1280x720p(HD) = 1100kb
# 854x480p(SD)= 700kb 
# 640x360p=500kb 
# Just a loop to keep the container running
while true; do :; done