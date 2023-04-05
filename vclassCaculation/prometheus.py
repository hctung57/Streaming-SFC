import prometheus_api_client
from datetime import datetime
from constants import *

print("Connected to Prometheus Server !!!")
prom = prometheus_api_client.PrometheusConnect()


def monitoring_node(node_name):
    para = f"job = '{node_name}'"
    job = '{' + para + '}'
    job1 = '{' + para + ',mode="idle"}'
    try:
        CPU_metrics = prom.custom_query(query=CPU_NODE_QUERY.format(job1))
        CPU_metric = CPU_metrics[0].get('value')
        time = CPU_metric[0]
        CPU_usage_value = CPU_metric[1]
        if node_name == POWER_MONITOR:
            power_metric = prom.custom_query(POWER_NODE_QUERY.format(job))
            power_value = power_metric[0].get('value')[1]
        else:
            power_value = 0

        memory_metrics = prom.custom_query(
            query=MEMORY_NODE_QUERY.format(job, job, job, job, job))
        memory_usage_value = memory_metrics[0].get('value')[1]

        bandwidth_receive_metrics = prom.custom_query(
            query=BANDWIDTH_RECEIVE_NODE_QUERY.format(job))
        bandwidth_receive_value = bandwidth_receive_metrics[0].get('value')[1]

        bandwidth_transmit_metrics = prom.custom_query(
            query=BANDWIDTH_TRANSMIT_NODE_QUERY.format(job))
        bandwidth_transmit_value = bandwidth_transmit_metrics[0].get('value')[
            1]
    except:
        return
    return CPU_usage_value, memory_usage_value, power_value, bandwidth_receive_value, bandwidth_transmit_value, time


def monitoring_pod(pod_name):
    try:
        CPU_pods = prom.custom_query(query=CPU_POD_QUERY.format(pod_name))
        CPU_usage_pods = CPU_pods[0].get('value')
        time = CPU_usage_pods[0]
        CPU_pod_value = CPU_usage_pods[1]
    except:
        # print("Error when query CPU!")
        return

    try:
        memory_pods = prom.custom_query(
            query=MEMORY_POD_QUERY.format(pod_name))
        memory_usage_pod = memory_pods[0].get('value')
        memory_pod_value = memory_usage_pod[1]
    except:
        # print("Error when query memory!")
        return

    try:
        bandwidth_receive_pod = prom.custom_query(
            query=BANDWIDTH_RECEIVE_POD_QUERY.format(pod_name))
        bandwidth_receive_pod_value = bandwidth_receive_pod[0].get('value')[1]
    except:
        # print("Error when query bandwidth reveive!")
        return

    try:

        bandwidth_transmit_pod = prom.custom_query(
            query=BANDWIDTH_TRANSMIT_POD_QUERY.format(pod_name))
        bandwidth_transmit_pod_value = bandwidth_transmit_pod[0].get('value')[
            1]
    except:
        # print("Error when query bandwidth transmit!")
        return

    return CPU_pod_value, memory_pod_value, bandwidth_receive_pod_value, bandwidth_transmit_pod_value, time

# NOTE: Check output of streaming over last nfv


def check_streaming_running_succeed(target_sfc_id: str):
    return


def caculate_power_node_prometheus(target_node_name: str):
    return
