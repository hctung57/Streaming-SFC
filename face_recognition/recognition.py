from urllib.request import urlopen
import cv2
import time
import logging
import configargparse
import numpy as np
import face_recognition
from face_lib import face_lib

logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - VERIFY: %(verify)s - FPS: %(fps)s')
FL = face_lib()

# get image from an URL function


def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)

    # return the image
    return image

# parser func


def parser_args():
    parser = configargparse.ArgParser(description="Face Recognition NFV FIL HUST",
                                      formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--source_rtmp",
                        help="source stream path")
    parser.add_argument("-img", "--img_url",
                        help="image url")
    return parser.parse_args()

# calculate average fps after exit

if __name__ == "__main__":
    # parser init
    args = parser_args()
    source_rtmp = args.source_rtmp
    img_url= args.img_url
    # Source Streaming path
    path = f"rtmp://{source_rtmp}/live/stream"

    # setup
    font = cv2.FONT_HERSHEY_DUPLEX
    # source video
    cap = cv2.VideoCapture(0)
    WIDTH_INPUT_STREAMING = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT_INPUT_STREAMING = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS_INPUT_STREAMING = int(cap.get(cv2.CAP_PROP_FPS))

    # get image from an URL
    # img = url_to_image(img_url)
    img=cv2.imread("IMG_0534.jpg")
    known_face_encodings = []
    known_face_encodings.append(face_recognition.face_encodings(img)[0])
    REFERENCE_IMAGE = img
    SUM_FRAME_HANDLE = 1
    SUM_FRAME_HAVE_TRUE_OUTPUT = 0
    SUM_FRAME_HAVE_FACE = 1

    # Variables to calculate fps
    print_fps_period = 1
    current_fps = 0
    frame_count = 0
    arr = []
    t0 = time.monotonic()
    process_this_frame = True
    while True:
        # Grab a single frame of video
        ret, frame = cap.read()
<<<<<<< HEAD

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                print(matches)
        process_this_frame = not process_this_frame
        frame_count += 1
        td = time.monotonic() - t0
        # cv2.imshow("aa", frame)
        if td > print_fps_period:
            current_fps = frame_count / td
            arr += [current_fps]
            # print("FPS: {:6.2f}".format(current_fps), end="\r")
            frame_count = 0
            t0 = time.monotonic()
        # logging.info('', extra={'verify': , 'fps': f'{current_fps:.2f}'})
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    cap.release()
    cv2.destroyAllWindows()
#     # loop frame by frame
#     while (True):
#         ret, frame = cap.read()
#         if ret == True:
#             notify = 'False'

#             # check if there are faces in frame and count it
#             face_in_frame = FL.get_faces(frame)
#             if face_in_frame:
#                 SUM_FRAME_HAVE_FACE += 1

#             face_exist, no_faces_detected = FL.recognition_pipeline(
#                 frame, REFERENCE_IMAGE)
#             if face_exist:
#                 notify = 'True'
#                 SUM_FRAME_HAVE_TRUE_OUTPUT += 1
#             # print("Recognition: {}".format(notify), end="\r")
#             # cv2.putText(frame,notify,(25,25), font, 1.0, (255,255,255), 1)

#             # fps calculate
#             SUM_FRAME_HANDLE += 1
#             frame_count += 1
#             td = time.monotonic() - t0
#             # cv2.imshow("aa", frame)
#             if td > print_fps_period:
#                 current_fps = frame_count / td
#                 arr += [current_fps]
#                 # print("FPS: {:6.2f}".format(current_fps), end="\r")
#                 frame_count = 0
#                 t0 = time.monotonic()
#             logging.info('', extra={'verify': notify, 'fps': f'{current_fps:.2f}'})

#             # the 'q' button is set as the
#             # quitting button you may use any
#             # desired button of your choice
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # break th loop
#         else:
#             break

# recognition_rate = (SUM_FRAME_HAVE_TRUE_OUTPUT/SUM_FRAME_HAVE_FACE)*100
# print("recognition rate: {:6.2f}".format(recognition_rate), "%")
# print("Sum frame have face:", SUM_FRAME_HAVE_FACE)
# print("Sum frame handled: ", SUM_FRAME_HANDLE)

# # After the loop release the cap object
# cap.release()
=======
        if ret == True:
            notify = 'False'

            # check if there are faces in frame and count it
            face_in_frame = FL.get_faces(frame)
            if face_in_frame:
                SUM_FRAME_HAVE_FACE += 1

            face_exist, no_faces_detected = FL.recognition_pipeline(
                frame, REFERENCE_IMAGE)
            if face_exist:
                notify = 'True'
                SUM_FRAME_HAVE_TRUE_OUTPUT += 1
            # fps calculate
            SUM_FRAME_HANDLE += 1
            frame_count += 1
            td = time.monotonic() - t0
            if td > print_fps_period:
                current_fps = frame_count / td
                arr += [current_fps]
                frame_count = 0
                t0 = time.monotonic()
            logging.info('', extra={'verify': notify, 'fps': f'{current_fps:.2f}'})

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # break th loop
        else:
            break

    recognition_rate = (SUM_FRAME_HAVE_TRUE_OUTPUT/SUM_FRAME_HAVE_FACE)*100
    print("AVERAGE FPS: ", average_fps(arr))
    print("recognition rate: {:6.2f}".format(recognition_rate), "%")
    print("Sum frame have face:", SUM_FRAME_HAVE_FACE)
    print("Sum frame handled: ", SUM_FRAME_HANDLE)

    # After the loop release the cap object
    cap.release()
>>>>>>> a00f3853603064e5936e6331c59b4424294b85bb
