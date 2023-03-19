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
        self.environment_variable = []
        self.node_name = ""


# source streaming init
SOURCE_STREAMING_VNF = service_info(
    NFV_SOURCE_STREAMING_SERVICE_NAME, "hctung57/source-streaming-ffmpeg:1.0.1", 1935, 1936)
SOURCE_STREAMING_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                             client.V1EnvVar(name='SOURCE_RTMP_PORT', value=''),
                                             client.V1EnvVar(name='RESOLUTION', value='')]
SOURCE_STREAMING_VNF.node_name = CLOUD
NFV_SOURCE_STREAMING_RESOUTION = R_1080P

# transcoder init
TRANSCODER_VNF = service_info(
    NFV_TRANSCODER_SERVICE_NAME, "hctung57/transcoder:1.0.7", 1935, 1936)
TRANSCODER_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                       client.V1EnvVar(
                                           name='SOURCE_RTMP_PORT', value=''),
                                       client.V1EnvVar(name='RESOLUTION', value='')]
NFV_TRANSCODER_RESOUTION = R_480P
TRANSCODER_VNF.node_name = EDGE

# face detection init
FACE_DETECTION_VNF = service_info(
    NFV_FACE_DETECTION_SERVICE_NAME, "hctung57/face-detection:1.0.2", 1935, 1936)
FACE_DETECTION_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                           client.V1EnvVar(name='SOURCE_RTMP_PORT', value='')]
FACE_DETECTION_VNF.node_name = EDGE

# background blur init
BACKGROUND_BLUR_VNF = service_info(
    NFV_BACKGROUND_BLUR_SERVICE_NAME, "hctung57/background-blur:1.0.2", 1935, 1936)
BACKGROUND_BLUR_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                            client.V1EnvVar(name='SOURCE_RTMP_PORT', value='')]
BACKGROUND_BLUR_VNF.node_name = EDGE

# match audio video init
MATCH_AUDIO_VIDEO_VNF = service_info(
    NFV_MATCH_AUDIO_VIDEO_SERVICE_NAME, "hctung57/match-av:1.0.2", 1935, 1936)
MATCH_AUDIO_VIDEO_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                              client.V1EnvVar(
                                                  name='SOURCE_RTMP_PORT', value=''),
                                              client.V1EnvVar(
                                                  name='SOURCE_AUDIO_SERVICE', value=''),
                                              client.V1EnvVar(
                                                  name='SOURCE_AUDIO_PORT', value=''),
                                              client.V1EnvVar(name='DELAY_AUDIO_VIDEO_TIME', value='0')]
MATCH_AUDIO_VIDEO_VNF.node_name = EDGE

# noisesuppress init
NOISE_SUPRESS_VNF = service_info(
    NFV_NOISE_SUPPRESS_NAME, "hctung57/noisesuppress:1.0.2", 1935, 1936)
NOISE_SUPRESS_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_AUDIO_SERVICE', value=''),
                                          client.V1EnvVar(name='SOURCE_AUDIO_PORT', value='')]
NOISE_SUPRESS_VNF.node_name = EDGE

# face recognition init
FACE_RECOGNITION_VNF = service_info(
    NFV_FACE_RECOGNITION_NAME, "hctung57/face-recognition-ffmpeg:test", 1935, 1936)
FACE_RECOGNITION_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_AUDIO_SERVICE', value=''),
                                          client.V1EnvVar(name='SOURCE_AUDIO_PORT', value=''),
                                          client.V1EnvVar(name='IMAGE_URL', value='')]
FACE_RECOGNITION_VNF.node_name = EDGE
