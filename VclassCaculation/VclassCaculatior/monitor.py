from kubernetes import client, config
import prometheus_api_client, time, datetime, csv
from kubernetes.client.rest import ApiException
from datetime import datetime

config.load_kube_config("/home/duc/.kube/config")



        

def Monitoring_Node(node_name):
    para = f"job = '{node_name}'"
    job = '{' + para + '}'
    
    CPU_Utilisation = prom.custom_query(query=f"100 - sum(irate(node_cpu_seconds_total{job}[1m]) *100)")
    CPU_Usage = CPU_Utilisation[0].get('value')
    time = datetime.fromtimestamp(CPU_Usage[0]).strftime("%A, %B %d, %Y %I:%M:%S")
    CPU_Usage_value = CPU_Usage[1]

    
    Memory_Utilisation = prom.custom_query(query=f" ((node_memory_MemTotal_bytes{job} - node_memory_MemFree_bytes{job} - node_memory_Cached_bytes{job} - node_memory_Buffers_bytes{job}) / node_memory_MemTotal_bytes{job}) * 100 ")
    Memory_Usage = Memory_Utilisation[0].get('value')
    Memory_Usage_value = Memory_Usage[1]
    
    Bandwidth = prom.custom_query(query=f"sum(rate(node_network_receive_bytes_total{job}[1m]) + rate(node_network_transmit_bytes_total{job}[1m])) ")
    Bandwidth_1 = Bandwidth[0].get('value')
    Bandwidth_value = Bandwidth_1[1]
    return CPU_Usage_value, Memory_Usage_value, Bandwidth_value, time
    


def Monitoring_Pod(pod_name):
    metric = f"container_label_io_kubernetes_pod_name='{pod_name}'"
        
    query_network_receive = 'container_network_receive_bytes_total{' + metric + '}'
    query_network_transmit = 'container_network_transmit_bytes_total{' + metric + '}'
    query_cpu = 'container_cpu_usage_seconds_total{' + metric + '}'
    query_ram_1 = 'container_memory_working_set_bytes{' + metric + '}'
    query_ram_2 = 'container_spec_memory_limit_bytes{' + metric + '}'
    
    CPU_Pods = prom.custom_query(f'sum({query_cpu}) * 100')
    CPU_Usage_Pods = CPU_Pods[0].get('value')
    time = datetime.fromtimestamp(CPU_Usage_Pods[0]).strftime("%A, %B %d, %Y %I:%M:%S")
    CPU_Pod_value = CPU_Usage_Pods[1]

    Memory_Pods = prom.custom_query(query=f"(sum({query_ram_1}) / sum({query_ram_2})) * 100")
    Memory_Usage_pod = Memory_Pods[0].get('value')
    Memory_Pod_value = Memory_Usage_pod[1]
    
    
    Bandwidth_pod = prom.custom_query(query=f"sum(rate({query_network_receive}[5m]) + rate({query_network_transmit}[5m]))")
    Bandwidth_Usage = Bandwidth_pod[0].get('value')
    Bandwidth_Pod_value = Bandwidth_Usage[1]
    return CPU_Pod_value, Memory_Pod_value, Bandwidth_Pod_value, time

def write_cvs_node(node_name):
    fields = ['Node_name', 'CPU(%)', 'Memory(%)', 'Bandwidth', 'Time']

    mydict = [{'Node_name': node_name, 'CPU(%)': CPU_Usage_value, 'Memory(%)': Memory_Usage_value, 'Bandwidth': Bandwidth_value, 'Time': time_node}]

    filename = 'Monitor_node.csv'

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames= fields)
        
        writer.writeheader()
        
        writer.writerows(mydict)

def write_cvs_pods(pod_name):
    fields = ['Pod_name', 'CPU(%)', 'Memory(%)', 'Bandwidth', 'Time']

    mydict = [{'Pod_name': pod_name, 'CPU(%)': CPU_Pod_value, 'Memory(%)': Memory_Pod_value, 'Bandwidth': Bandwidth_Pod_value, 'Time': time_pods}]

    filename = pod_name + '.csv'

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames= fields)
        
        writer.writeheader()
        
        writer.writerows(mydict)

try:
    prom = prometheus_api_client.PrometheusConnect()
    print("Connected to Prometheus Server !!!")
    
    k8s_api_obj = client.CoreV1Api()
    api_response = k8s_api_obj.list_namespaced_pod(namespace='default')
    
    
        

    CPU_Usage_value, Memory_Usage_value, Bandwidth_value, time_node = Monitoring_Node('node_worker_1')
    write_cvs_node('node_worker_1')
    for i in api_response.items:
        pod_name = i.metadata.name
        CPU_Pod_value, Memory_Pod_value, Bandwidth_Pod_value, time_pods = Monitoring_Pod(pod_name)
        write_cvs_pods(pod_name)


except Exception as i:
    print(i)
    
