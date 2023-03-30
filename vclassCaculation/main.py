import threading
import time
import os
# custom library
import functional
import kubernetesAPI
import deployment
import prometheus
from constants import *
import VNFInfomation


def deploy_sfc_and_get_prometheus_pod_value(target_sfc, target_sfc_id: str, file_name: str,file_name_fps:str , time_to_calculate: float):
    start_time = time.monotonic()
    key = '-'+target_sfc_id+'-'
    deployment.create_sfc(target_sfc, target_sfc_id)
    print("[SCENARIO] start calculating pods")
    while (True):
        list_pod_namespaced = kubernetesAPI.list_namespaced_pod_status()
        if time.monotonic() - start_time > time_to_calculate:
            for pod in list_pod_namespaced:
                if key in pod.pod_name and pod.pod_status == "Running":
                    if not (NFV_NOISE_SUPPRESS_NAME in pod.pod_name):
                        kubernetesAPI.connect_get_namespaced_pod_exec("cat app.log > results/temp/temp.log",pod.pod_name)
                        functional.write_log_data_to_csv(pod.pod_name, file_name_fps)
            deployment.delete_sfc(target_sfc, target_sfc_id)
            break
        for pod in list_pod_namespaced:
            if key in pod.pod_name and pod.pod_status == "Running":
                try:
                    cpu, memory, bandwidth_transmit, bandwidth_receive, time_prom = prometheus.monitoring_pod(pod.pod_name) # type: ignore
                    data = [time_prom, cpu, memory, bandwidth_transmit, bandwidth_receive, pod.pod_name]
                    functional.write_to_csv(data, file_name)
                except:
                    # print("Error when call monitoring!")
                    continue
                # # caculate value here
        time.sleep(0.5)
    return


def get_prometheus_node_value(target_list_node , file_name: str, time_to_calculate: int):
    start_time = time.monotonic()
    print("[SCENARIO] start calculating nodes")
    while (True):
        if time.monotonic() - start_time > time_to_calculate:
            break
        for node in target_list_node:
            try:
                cpu, memory, bandwidth_transmit, bandwidth_receive, time_prom = prometheus.monitoring_node(node) # type: ignore
                data = [time_prom, cpu, memory, bandwidth_transmit, bandwidth_receive, node]
                functional.write_to_csv(data, file_name)
            except:
                continue
        time.sleep(0.5)

    return


def main(resolution):
    VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION = resolution
    print("source streaming resolution: ",VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION)
    # edit number_of_repetitions here
    number_of_repetitions = 5
    time_to_caculate = 300  # sec
    print("[START CALCULATING WITH", number_of_repetitions,
          " REPETITION AND", time_to_caculate, "SECOND]")
    generate_file_time = functional.generate_file_time()
    os.mkdir(DATA_PROMETHEUS_FOLDER_DIRECTORY.format(generate_file_time))
    sfc_id = 1
    for sfc in deployment.SFC:
        for repetition in range(0, number_of_repetitions):
            print("[SCENARIO] start repetition:", repetition)
            file_name = DATA_PROMETHEUS_FILE_DIRECTORY.format(
                generate_file_time, str(sfc_id), str(VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION), repetition)
            file_name_fps = FPS_FILE_DIRECTORY.format(
                generate_file_time, str(sfc_id), str(VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION), repetition)
            th = threading.Thread(
                target=deploy_sfc_and_get_prometheus_pod_value, args=(sfc, str(sfc_id), file_name, file_name_fps,time_to_caculate,))
            th.start()
            # calculate nodes (1 tab)
            file_name_nodes = DATA_PROMETHEUS_FILE_NODE_DIRECTORY.format(
                generate_file_time, sfc_id, str(VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION),repetition)
            th = threading.Thread(target=get_prometheus_node_value(
                [CLOUD, EDGE], file_name_nodes, time_to_caculate))
            th.start()
            th.join()
            time.sleep(60)
        sfc_id += 1
    print("[SCENARIO] done!")
    return


if __name__ == "__main__":
    # main(R_1080P)
    # main(R_720P)
    # main(R_480P)
    # main(R_360P)
    
    VNFInfomation.SOURCE_STREAMING_VNF.node_name = EDGE
    VNFInfomation.MATCH_AUDIO_VIDEO_VNF.node_name = CLOUD
    VNFInfomation.NOISE_SUPRESS_VNF.node_name = CLOUD
    VNFInfomation.FACE_RECOGNITION_VNF.node_name = CLOUD
    VNFInfomation.FACE_DETECTION_VNF.node_name = CLOUD
    VNFInfomation.TRANSCODER_VNF.node_name = CLOUD
    VNFInfomation.BACKGROUND_BLUR_VNF.node_name = CLOUD
    
    # main(R_1080P)
    # main(R_720P)
    # main(R_480P)
    main(R_360P)
    
