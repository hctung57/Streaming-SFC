
import time

# custom lib import
import kubernetesAPI
from constants import *
import VNFInfomation

# SFC = [[SOURCE_STREAMING_VNF],
#        [TRANSCODER_VNF, BACKGROUND_BLUR_VNF, FACE_DETECTION_VNF, MATCH_AUDIO_VIDEO_VNF],
#        [NOISE_SUPRESS_VNF],
#        [FACE_RECOGNITION_VNF]]
SFC = []

SFC1 = [[VNFInfomation.SOURCE_STREAMING_VNF],
        [VNFInfomation.MATCH_AUDIO_VIDEO_VNF]]

SFC2 = [[VNFInfomation.SOURCE_STREAMING_VNF],
        [VNFInfomation.BACKGROUND_BLUR_VNF]]

SFC3 = [[VNFInfomation.SOURCE_STREAMING_VNF],
        [VNFInfomation.FACE_DETECTION_VNF]]

SFC4 = [[VNFInfomation.SOURCE_STREAMING_VNF],
        [VNFInfomation.TRANSCODER_VNF]]

SFC5 = [[VNFInfomation.SOURCE_STREAMING_VNF],
        [],
        [],
        [VNFInfomation.FACE_RECOGNITION_VNF]]

SFC6 = [[VNFInfomation.SOURCE_STREAMING_VNF],
        [],
        [VNFInfomation.NOISE_SUPRESS_VNF]]

SFC7 = [[VNFInfomation.SOURCE_STREAMING_VNF]]

SFC8 = [[VNFInfomation.SOURCE_STREAMING_VNF],
        [VNFInfomation.TRANSCODER_VNF,VNFInfomation.BACKGROUND_BLUR_VNF,VNFInfomation.MATCH_AUDIO_VIDEO_VNF]]

SFC.append(SFC1)
SFC.append(SFC2)
SFC.append(SFC3)
SFC.append(SFC4)
# SFC.append(SFC5)
SFC.append(SFC6)
# SFC.append(SFC8)


# NOTE: generate a k8s service name using service and id
def generate_service_name(service_name: str, service_id: str):
    return service_name + "-" + service_id + "-service"


def create_sfc(sfc, sfc_id: str):
    for chain_number in range(0, len(sfc)):

        if chain_number == 0:
            for vnf in sfc[chain_number]:
                # print(VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION)
                vnf.environment_variable[2].value = str(
                        VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION)
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
                    VNFInfomation.SOURCE_STREAMING_VNF.service_name, sfc_id)
                vnf.environment_variable[1].value = str(
                    VNFInfomation.SOURCE_STREAMING_VNF.service_port)

                message = kubernetesAPI.create_namespaced_service(
                    vnf.service_name, sfc_id, vnf.service_port)
                print(message)

                message = kubernetesAPI.create_namespaced_deployment(
                    vnf.service_name, sfc_id, vnf.dokcer_image,
                    vnf.container_port, vnf.environment_variable, vnf.node_name)
                print(message)

        elif chain_number == 3:
            for vnf in sfc[chain_number]:
                vnf.environment_variable[0].value = generate_service_name(
                    VNFInfomation.FACE_RECOGNITION_SOURCE.service_name, sfc_id)
                vnf.environment_variable[1].value = str(
                    VNFInfomation.FACE_RECOGNITION_SOURCE.service_port)
                vnf.environment_variable[2].value = str(
                    VNFInfomation.FACE_RECOGNITION_VERIFY_IMAGE_URL)
                
                message = kubernetesAPI.create_namespaced_deployment(
                vnf.service_name, sfc_id, vnf.dokcer_image,
                vnf.container_port, vnf.environment_variable, vnf.node_name)
                print(message)
                message = kubernetesAPI.create_namespaced_service(
                    vnf.service_name, sfc_id, vnf.service_port)
                print(message)
                
                

        else:
            previous_vnf = None
            for index, vnf in enumerate(sfc[chain_number]):
                if index == 0:
                    vnf.environment_variable[0].value = generate_service_name(
                        VNFInfomation.SOURCE_STREAMING_VNF.service_name, sfc_id)
                    vnf.environment_variable[1].value = str(
                        VNFInfomation.SOURCE_STREAMING_VNF.service_port)

                else:
                    if previous_vnf != None:
                        vnf.environment_variable[0].value = generate_service_name(
                            previous_vnf.service_name, sfc_id)
                        vnf.environment_variable[1].value = str(
                            previous_vnf.service_port)

                if vnf.service_name == NFV_TRANSCODER_SERVICE_NAME:
                    vnf.environment_variable[2].value = str(
                        VNFInfomation.NFV_TRANSCODER_RESOUTION)

                if vnf.service_name == NFV_MATCH_AUDIO_VIDEO_SERVICE_NAME:
                    if len(sfc) > 2:
                        if sfc[2]:
                                vnf.environment_variable[2].value = generate_service_name(
                                VNFInfomation.NOISE_SUPRESS_VNF.service_name, sfc_id)
                                vnf.environment_variable[3].value = str(
                                    VNFInfomation.NOISE_SUPRESS_VNF.service_port)
                    else:
                        vnf.environment_variable[2].value = generate_service_name(
                            VNFInfomation.SOURCE_STREAMING_VNF.service_name, sfc_id)
                        vnf.environment_variable[3].value = str(
                            VNFInfomation.SOURCE_STREAMING_VNF.service_port)

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
#     delete_sfc(sfc, str(i))
#     i += 1
# i = 1
# for sfc in SFC:
#     create_sfc(sfc, str(i))
#     i += 1
# time.sleep(30000)
# i = 1   
# for sfc in SFC:
#     delete_sfc(sfc, str(i))
#     i += 1
