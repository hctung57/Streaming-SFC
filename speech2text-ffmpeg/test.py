import subprocess
import numpy
import cv2
# def create_samp_2():
#     sample= subprocess.run(["ffmpeg", "-probesize", "50k", "-i", "rtmp://localhost/live/stream", "-c:v", "libx264", "-b:v", 
#                             "512k", "-g", "90", "-flags", "-global_header", "-map", "0", "-f", "segment",
#                             "-segment_time", "10", "-segment_list_size", "2", "-segment_format", "mpegts", "-f", "mp4", "pipe:"], stdout=subprocess.PIPE).stdout
#     return(sample)

command = ["ffmpeg", "-i", "rtmp://localhost/live/stream", 
            "-c", "copy","-flvflags", "no_duration_filesize", "-f", "segment", "-segment_time", 
            "3", "-reset_timestamps", "1", "-segment_format", "flv","pipe:1"]
p = subprocess.Popen(command,shell=False, stdout=subprocess.PIPE,
                    bufsize=10**8)

while True:
    array = numpy.frombuffer(p.stdout, dtype='uint8')
    img = cv2.imdecode(array, 1)
    cv2.imshow("window", img)


