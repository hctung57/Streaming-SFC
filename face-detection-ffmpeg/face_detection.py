import cv2
import mediapipe as mp
import configargparse
import time
import subprocess
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#parser func
def parser_args():
    parser = configargparse.ArgParser(description="Face Detection NFV FIL HUST",
                            formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--source_rtmp",
                        help="source stream path")
    return parser.parse_args()

#parser init
args = parser_args()
source_rtmp = args.source_rtmp

#URL destination streaming (nginx server)
rtmp_url = "rtmp://localhost/live/stream"

#Source Streaming path
path = f"rtmp://{source_rtmp}/live/stream"
# cap = cv2.VideoCapture(path)
cap = cv2.VideoCapture(path)

# gather video info to ffmpeg
font = cv2.FONT_HERSHEY_DUPLEX
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

command = ['ffmpeg', '-re',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmp_url]
           
# using subprocess and pipe to fetch frame data
p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=True)

#global variable
sum_frame = 1
sum_face_true = 0
print_fps_period = 1
frame_count = 1
t0 = time.monotonic()
print_fps = 0
clear = mp_drawing.DrawingSpec(color=(255,0,0), thickness= 0, circle_radius = 0)
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.4) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    num_face = 0
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    # Draw the face detection annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      for detection in results.detections:
        mp_drawing.draw_detection(image, detection, clear )
      num_face = len(results.detections)
    #print number of face in frame
    cv2.putText(image,"Face:"+str(num_face),(25,25), font, 1.0, (255,0,0), 1)
    cv2.putText(image,"FPS:{:6.2f}".format(print_fps),(25,50), font, 1.0, (255,0,0), 1)
    #fps calculate
    sum_frame += 1
    frame_count += 1
    td = time.monotonic() - t0
    if td > print_fps_period:
        current_fps = frame_count / td
        print_fps = current_fps
        print("FPS: {:6.2f}".format(current_fps), end="\r")
        frame_count = 0
        t0 = time.monotonic()
    # write to pipe
    p.stdin.write(image.tobytes())
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()