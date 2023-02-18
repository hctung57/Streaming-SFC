import threading
import time
import os
# custom library
import functional
import kubernetesAPI
import deployment
# import prometheus
from constants import *


def deploy_sfc_and_get_prometheus_pod_value(target_sfc, target_sfc_id: str, file_name: str, time_to_calculate: float):
    start_time = time.monotonic()
    key = '-'+target_sfc_id+'-'
    deployment.create_sfc(target_sfc, target_sfc_id)
    while (True):
        if time.monotonic() - start_time > time_to_calculate:
            deployment.delete_sfc(target_sfc, target_sfc_id)
            break
        list_pod_namespaced = kubernetesAPI.list_namespaced_pod_status()
        for pod in list_pod_namespaced:
            if key in pod.pod_name and pod.pod_status == "Running":
                data = [time.monotonic(), pod.pod_name]
                functional.write_to_csv(data, file_name)

                # # caculate value here
                time.sleep(0.5)
    return


def get_prometheus_node_value(target_list_node: str, file_name: str, time_to_calculate: str):
    start_time = time.monotonic()
    while (True):
        if time.monotonic() - start_time > time_to_calculate:
            break
        for node in target_list_node:
            data = [time.monotonic(), node]
            functional.write_to_csv(data, file_name)
            time.sleep(0.5)
    return


def main():
    # edit number_of_repetitions here
    number_of_repetitions = 2
    time_to_caculate = 60  # sec
    print(("[START CALCULATING WITH {number_of_repetitions} REPETITION AND {time_to_caculate} SECOND]"))
    generate_file_time = functional.generate_file_time()
    os.mkdir(DATA_PROMETHEUS_FOLDER_DIRECTORY.format(generate_file_time))
    for repetition in range(0, number_of_repetitions):
        print("[SCENARIO] start repetition {repetition}")
        sfc_id = 1
        th = None
        print("[SCENARIO] start calculating pods")
        for sfc in deployment.SFC:
            file_name = DATA_PROMETHEUS_FILE_DIRECTORY.format(
                generate_file_time, str(sfc_id), generate_file_time, repetition)
            th = threading.Thread(
                target=deploy_sfc_and_get_prometheus_pod_value, args=(sfc, str(sfc_id), file_name, time_to_caculate,))
            th.start()
            sfc_id += 1
        
        # calculate nodes
        print("[SCENARIO] start calculating nodes")
        file_name_nodes = DATA_PROMETHEUS_FILE_NODE_DIRECTORY.format(
            generate_file_time, generate_file_time, repetition)
        th = threading.Thread(target=get_prometheus_node_value(
            [CLOUD, EDGE], file_name_nodes, time_to_caculate))
        th.start()
        th.join()
        time.sleep(60)
    print("[SCENARIO] done!")
    return


if __name__ == "__main__":
    main()
