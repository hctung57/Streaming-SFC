from kubernetes import client
from constants import *


class service_info:
    def __init__(self, service_name: str, dokcer_image: str,
                 container_port: int, service_port: int) -> None:
        self.service_name = service_name
        self.service_id = None
        self.dokcer_image = dokcer_image
        self.container_port = container_port
        self.service_port = service_port
        self.environment_variable = None


SOURCE_STREAMING_VNF = service_info(NFV_SOURCE_STREAMING_SERVICE_NAME,
                                    "hctung57/source-streaming-ffmpeg:1.0", 1935, 1936)
FACE_DETECTION_VNF = service_info(NFV_FACE_DETECTION_SERVICE_NAME,
                                  "hctung57/face-detection:1.0.2", 1935, 1936)
TRANSCODER_VNF = service_info(NFV_TRANSCODER_SERVICE_NAME,
                              "hctung57/transcoder:1.0.7", 1935, 1936)
BACKGROUND_BLUR_VNF = service_info(NFV_BACKGROUND_BLUR_SERVICE_NAME,
                                   "hctung57/background-blur:1.0.2", 1935, 1936)
MATCH_AUDIO_VIDEO_VNF = service_info(NFV_MATCH_AUDIO_VIDEO_SERVICE_NAME,
                                     "hctung57/match-av:1.0.0", 1935, 1936)
