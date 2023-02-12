from datetime import datetime
import threading
# custom library
import kubernetesAPI
import deployment
import prometheus
from constants import *


# NOTE: tinh toan 10 lan
def deploy_sfc_and_get_prometheus_value(target_sfc, target_sfc_id: str):

    return


def main():
    #edit number_of_repetitions here
    number_of_repetitions =  10
    
    for repetition in range(0,number_of_repetitions):
        sfc_id = 1
        for sfc in deployment.SFC:
            threading.Thread(
                target=deploy_sfc_and_get_prometheus_value, args=(sfc, sfc_id,)).start()
            sfc += 1
    return


if __name__ == "__main__":
    main()
