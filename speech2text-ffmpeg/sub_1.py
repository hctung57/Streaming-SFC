#!/usr/bin/env python3
import speech_recognition as sr
from sunau import AUDIO_FILE_ENCODING_DOUBLE
import sys
import os
import wave
import subprocess
from pathlib import Path
from subprocess import check_call

from dir_monitor import DirMonitor 

print("111111111111111111111111111111")
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
    

    r = sr.Recognizer()
    with sr.AudioFile(output) as source:
        audio_listened = r.record(source)
        # try converting it to text
        try:
            text = r.recognize_google(audio_listened)
            print(text)
        except sr.UnknownValueError as e:
            text = ""

    print(text)
    texts = "dungggg"
    os.system(f"""ffmpeg -i {audio_file_path} -vf drawtext="fontfile=/path/to/font.ttf:text={text}: fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5:boxborderw=5: x={w}: y={h}" -codec:a copy -f mpegts -flush_packets 0 udp://192.168.58.1:5000?pkt_size=1316""")

    
def text(text,audio_file_path_ts, x="center"):
    if x == "center":
        w = "(w-text_w)/2"
        h = "(h-text_h)/5"
    elif x == "left":
        w = "10"
        h = "h - 30"
    else:
        w = "0"
        y = "0"
    os.system(f"""ffmpeg -i {audio_file_path_ts} -vf drawtext="fontfile=/path/to/font.ttf:text={text}: fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5:boxborderw=5: x={w}: y={h}" -codec:a copy -f mpegts -flush_packets 0 udp://192.168.58.1:5000?pkt_size=1316""")    
audio_home=sys.argv[1]
dirMonitor=DirMonitor(audio_home,"foo","ts",process_audio)
dirMonitor.listen()

