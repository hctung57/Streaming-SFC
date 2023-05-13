sleep 15;
export SOURCE_RTMP_URL_1="$(getent hosts $SOURCE_STREAM_SERVICE_1 | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT_1"
export SOURCE_RTMP_URL_2="$(getent hosts $SOURCE_STREAM_SERVICE_2 | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT_2"
python3 capture.py -s1 $SOURCE_RTMP_URL_1 -name1 $SOURCE_STREAM_SERVICE_1 -s2 $SOURCE_RTMP_URL_2 -name2 $SOURCE_STREAM_SERVICE_2

# Just a loop to keep the container running
while true; do :; done