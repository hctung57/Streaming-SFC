#!/usr/bin/env python3
import speech_recognition as sr
import sys
import os
import subprocess
from pathlib import Path
from dir_monitor import DirMonitor 

# command = ['ffmpeg',
#         '-y',
#         '-re', # '-re' is requiered when streaming in "real-time"
#         '-i', 'pipe:1',
#         '-f', 'flv', 
#         'rtmp://localhost/live/out']
# p = subprocess.Popen(command, stdin=subprocess.PIPE)
print("Speech to text....")
def process_audio(audio_file_path, x="center"):
    if x == "center":
        w = "(w-text_w)/2"
        h = "(h-text_h)/2 +250"
    elif x == "left":
        w = "10"
        h = "h - 30"
    else:
        w = "0"
        y = "0"
       
    print("audio_file_path: ",audio_file_path)
    
    file_path=os.path.join(audio_file_path)
    file_name = Path(file_path).stem
    output = "out/out" + file_name + ".wav"
    os.system(f"""ffmpeg -i {audio_file_path} -acodec pcm_s16le -ac 1 -ar 22050 {output}""")
    

    # r = sr.Recognizer()
    # with sr.AudioFile(output) as source:
    #     audio_listened = r.record(source)
    #     # try converting it to text
    #     try:
    #         text = r.recognize_google(audio_listened)
    #     except sr.UnknownValueError as e:
    #         text = ""
    text = ""
    os.system(f"""ffmpeg -re -i {audio_file_path} -vf drawtext="fontfile=/path/to/font.ttf:text={text}: fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5:boxborderw=5: x={w}: y={h}" -f flv rtmp://localhost/live/out""")    
    # p.stdin.write(file_path)
    print(file_path.encode())
audio_home=sys.argv[1]
dirMonitor=DirMonitor(audio_home,"foo","ts",process_audio)
dirMonitor.listen()

