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

        memory_metrics = prom.custom_query(
            query=MEMORY_NODE_QUERY.format(job, job, job, job, job))
        memory_usage_value = memory_metrics[0].get('value')[1]

        bandwidth_receive_metrics = prom.custom_query(
            query=BANDWIDTH_RECEIVE_NODE_QUERY.format(job))
        bandwidth_receive_value = bandwidth_receive_metrics[0].get('value')[1]
        
        bandwidth_transmit_metrics = prom.custom_query(
            query=BANDWIDTH_TRANSMIT_NODE_QUERY.format(job))
        bandwidth_transmit_value = bandwidth_transmit_metrics[0].get('value')[1]
    except:
        return
    return CPU_usage_value, memory_usage_value, bandwidth_receive_value, bandwidth_transmit_value, time


def monitoring_pod(pod_name):
    metric = f"container_label_io_kubernetes_pod_name='{pod_name}'"

    query_network_receive = 'container_network_receive_bytes_total{' + metric + '}'
    query_network_transmit = 'container_network_transmit_bytes_total{' + metric + '}'
    query_cpu = 'container_cpu_usage_seconds_total{' + metric + '}'
    query_ram_1 = 'container_memory_working_set_bytes{' + metric + '}'
    query_ram_2 = 'container_spec_memory_limit_bytes{' + metric + '}'

    CPU_Pods = prom.custom_query(f'sum({query_cpu}) * 100')
    CPU_Usage_Pods = CPU_Pods[0].get('value')
    time = datetime.fromtimestamp(
        CPU_Usage_Pods[0]).strftime("%A, %B %d, %Y %I:%M:%S")
    CPU_Pod_value = CPU_Usage_Pods[1]

    Memory_Pods = prom.custom_query(
        query=f"(sum({query_ram_1}) / sum({query_ram_2})) * 100")
    Memory_Usage_pod = Memory_Pods[0].get('value')
    Memory_Pod_value = Memory_Usage_pod[1]

    Bandwidth_pod = prom.custom_query(
        query=f"sum(rate({query_network_receive}[5m]) + rate({query_network_transmit}[5m]))")
    Bandwidth_Usage = Bandwidth_pod[0].get('value')
    Bandwidth_Pod_value = Bandwidth_Usage[1]

    return CPU_Pod_value, Memory_Pod_value, Bandwidth_Pod_value, time

# NOTE: Check output of streaming over last nfv


def check_streaming_running_succeed(target_sfc_id: str):
    return


def caculate_power_node_prometheus(target_node_name: str):
    return
