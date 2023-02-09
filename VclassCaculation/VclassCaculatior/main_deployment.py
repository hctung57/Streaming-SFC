

# custom lib import
import KubernetesAPI
from VNFInfomation import *
from constants import *
import time

SFC = [[SOURCE_STREAMING_VNF, FACE_DETECTION_VNF,MATCH_AUDIO_VIDEO_VNF]]
NFV_TRANSCODER_RESOUTION = R_480P

SOURCE_STREAMING_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                             client.V1EnvVar(name='SOURCE_RTMP_PORT', value='')]

TRANSCODER_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                       client.V1EnvVar(
                                           name='SOURCE_RTMP_PORT', value=''),
                                       client.V1EnvVar(name='RESOLUTION', value='')]

FACE_DETECTION_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                           client.V1EnvVar(name='SOURCE_RTMP_PORT', value='')]

BACKGROUND_BLUR_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                            client.V1EnvVar(name='SOURCE_RTMP_PORT', value='')]

MATCH_AUDIO_VIDEO_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
                                              client.V1EnvVar(
                                                  name='SOURCE_RTMP_PORT', value=''),
                                              client.V1EnvVar(
                                                  name='SOURCE_AUDIO_SERVICE', value=''),
                                              client.V1EnvVar(
                                                  name='SOURCE_AUDIO_PORT', value=''),
                                              client.V1EnvVar(name='DELAY_AUDIO_VIDEO_TIME', value='1')]


def generate_service_name(service_name: str, service_id: str):
    return service_name + "-" + service_id + "-service"


def create_sfc(sfc, sfc_id: str):
    previous_vnf = None
    for vnf in sfc:
        if vnf.service_name != NFV_SOURCE_STREAMING_SERVICE_NAME:
            vnf.environment_variable[0].value = generate_service_name(
                previous_vnf.service_name, sfc_id)
            vnf.environment_variable[1].value = str(previous_vnf.service_port)
            if vnf.service_name == NFV_TRANSCODER_SERVICE_NAME:
                vnf.environment_variable[2].value = str(NFV_TRANSCODER_RESOUTION)
            if vnf.service_name == NFV_MATCH_AUDIO_VIDEO_SERVICE_NAME:
                vnf.environment_variable[2].value = generate_service_name(sfc[0].service_name, sfc_id)
                vnf.environment_variable[3].value = str(sfc[0].service_port)
        message = KubernetesAPI.create_namespaced_service(
            vnf.service_name, sfc_id, vnf.service_port)
        print(message)
        message = KubernetesAPI.create_namespaced_deployment(
            vnf.service_name, sfc_id, vnf.dokcer_image,
            vnf.container_port, vnf.environment_variable)
        print(message)
        previous_vnf = vnf


def delete_sfc(sfc, sfc_id: str):
    for vnf in sfc:
        message = KubernetesAPI.delete_namespaced_deployment(
            vnf.service_name, sfc_id)
        print(message)
        message = KubernetesAPI.delete_namespaced_service(
            vnf.service_name, sfc_id)
        print(message)


i = 1
for sfc in SFC:
    create_sfc(sfc, str(i))
    i = i + 1
time.sleep(200)
i = 1
for sfc in SFC:
    delete_sfc(sfc, str(i))
    i = i + 1
