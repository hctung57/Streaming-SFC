
import time

# custom lib import
import kubernetesAPI
from VNFInfomation import *
from constants import *

# SFC = [[SOURCE_STREAMING_VNF],
#        [TRANSCODER_VNF, BACKGROUND_BLUR_VNF, FACE_DETECTION_VNF, MATCH_AUDIO_VIDEO_VNF],
#        [NOISE_SUPRESS_VNF]]
SFC = []

SFC1 = [[SOURCE_STREAMING_VNF],
        [TRANSCODER_VNF, MATCH_AUDIO_VIDEO_VNF],
        [NOISE_SUPRESS_VNF]]
SFC2 = [[SOURCE_STREAMING_VNF],
        [MATCH_AUDIO_VIDEO_VNF],
        [NOISE_SUPRESS_VNF]]
SFC3 = [[SOURCE_STREAMING_VNF]]
SFC.append(SFC1)
SFC.append(SFC2)


# NOTE: generate a k8s service name using service and id
def generate_service_name(service_name: str, service_id: str):
    return service_name + "-" + service_id + "-service"


def create_sfc(sfc, sfc_id: str):
    for chain_number in range(0, len(sfc)):

        if chain_number == 0:
            for vnf in sfc[chain_number]:
                message = kubernetesAPI.create_namespaced_service(
                    vnf.service_name, sfc_id, vnf.service_port)
                print(message)

                message = kubernetesAPI.create_namespaced_deployment(
                    vnf.service_name, sfc_id, vnf.dokcer_image,
                    vnf.container_port, vnf.environment_variable, vnf.node_name)
                print(message)

        elif chain_number == 2:
            for vnf in sfc[chain_number]:

                vnf.environment_variable[0].value = generate_service_name(
                    SOURCE_STREAMING_VNF.service_name, sfc_id)
                vnf.environment_variable[1].value = str(
                    SOURCE_STREAMING_VNF.service_port)

                message = kubernetesAPI.create_namespaced_service(
                    vnf.service_name, sfc_id, vnf.service_port)
                print(message)

                message = kubernetesAPI.create_namespaced_deployment(
                    vnf.service_name, sfc_id, vnf.dokcer_image,
                    vnf.container_port, vnf.environment_variable, vnf.node_name)
                print(message)

        # if chain_number == 3:
        #     #this is code for face recognition
        #     continue

        else:
            previous_vnf = None
            for index, vnf in enumerate(sfc[chain_number]):

                if index == 0:
                    vnf.environment_variable[0].value = generate_service_name(
                        SOURCE_STREAMING_VNF.service_name, sfc_id)
                    vnf.environment_variable[1].value = str(
                        SOURCE_STREAMING_VNF.service_port)

                else:
                    vnf.environment_variable[0].value = generate_service_name(
                        previous_vnf.service_name, sfc_id)
                    vnf.environment_variable[1].value = str(
                        previous_vnf.service_port)

                if vnf.service_name == NFV_TRANSCODER_SERVICE_NAME:
                    vnf.environment_variable[2].value = str(
                        NFV_TRANSCODER_RESOUTION)

                if vnf.service_name == NFV_MATCH_AUDIO_VIDEO_SERVICE_NAME:
                    if len(sfc[chain_number]) == 1:
                        vnf.environment_variable[2].value = generate_service_name(
                            NOISE_SUPRESS_VNF.service_name, sfc_id)
                        vnf.environment_variable[3].value = str(
                            NOISE_SUPRESS_VNF.service_port)
                    else:
                        vnf.environment_variable[2].value = generate_service_name(
                            SOURCE_STREAMING_VNF.service_name, sfc_id)
                        vnf.environment_variable[3].value = str(
                            SOURCE_STREAMING_VNF.service_port)

                message = kubernetesAPI.create_namespaced_service(
                    vnf.service_name, sfc_id, vnf.service_port)
                print(message)

                message = kubernetesAPI.create_namespaced_deployment(
                    vnf.service_name, sfc_id, vnf.dokcer_image,
                    vnf.container_port, vnf.environment_variable, vnf.node_name)
                print(message)
                previous_vnf = vnf
    return


def delete_sfc(sfc, sfc_id: str):
    for chain_nunber in sfc:
        for vnf in chain_nunber:
            message = kubernetesAPI.delete_namespaced_deployment(
                vnf.service_name, sfc_id)
            print(message)
            message = kubernetesAPI.delete_namespaced_service(
                vnf.service_name, sfc_id)
            print(message)
    return
# i = 1
# for sfc in SFC:
#     create_sfc(sfc, str(i))
#     i += 1
# # time.sleep(300)
# i = 1   
# for sfc in SFC:
#     delete_sfc(sfc, str(i))
#     i += 1
