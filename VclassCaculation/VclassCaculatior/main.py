import threading
# custom library
import functional
import kubernetesAPI
import deployment
import prometheus
from constants import *


# NOTE: tinh toan 10 lan
def deploy_sfc_and_get_prometheus_value(target_sfc, target_sfc_id: str, file_name: str):
    deployment.create_sfc(target_sfc,target_sfc_id)
    return


def main():
    # edit number_of_repetitions here
    number_of_repetitions = 10
    generate_file_time = functional.generate_file_time()
    for repetition in range(0, number_of_repetitions):
        sfc_id = 1
        for sfc in deployment.SFC:
            file_name = DATA_PROMETHEUS_FILE_DIRECTORY.format(
                generate_file_time, sfc_id, generate_file_time, repetition)
            threading.Thread(
                target=deploy_sfc_and_get_prometheus_value, args=(sfc, sfc_id, file_name,)).start()
            sfc += 1
    return


if __name__ == "__main__":
    main()
