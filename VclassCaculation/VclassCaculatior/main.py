import threading
import time
import os
# custom library
import functional
import kubernetesAPI
import deployment
# import prometheus
from constants import *


# NOTE: tinh toan 10 lan
def deploy_sfc_and_get_prometheus_pod_value(target_sfc, target_sfc_id: str, file_name: str, time_to_caculate: float):
    start_time = time.monotonic()
    key = '-'+target_sfc_id+'-'
    deployment.create_sfc(target_sfc, target_sfc_id)
    while (True):
        if time.monotonic() - start_time > time_to_caculate:
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


def main():
    # edit number_of_repetitions here
    number_of_repetitions = 2
    time_to_caculate = 60  # sec
    generate_file_time = functional.generate_file_time()
    os.mkdir(DATA_PROMETHEUS_FOLDER_DIRECTORY.format(generate_file_time))
    for repetition in range(0, number_of_repetitions):
        sfc_id = 1
        th = None
        for sfc in deployment.SFC:
            file_name = DATA_PROMETHEUS_FILE_DIRECTORY.format(
                generate_file_time, str(sfc_id), generate_file_time, repetition)
            th = threading.Thread(
                target=deploy_sfc_and_get_prometheus_pod_value, args=(sfc, str(sfc_id), file_name, time_to_caculate,))
            th.start()
            sfc_id += 1
        th.join()
        time.sleep(60)
    return


if __name__ == "__main__":
    main()
