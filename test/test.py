import cv2
import time
import sys
try:
  cv2.VideoCapture("rtmp://localhost/live/stream")
except:
  print("hi")
  sys.ext(1)
