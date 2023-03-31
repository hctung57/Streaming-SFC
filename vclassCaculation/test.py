from kubernetes import client, config
import subprocess
config.load_kube_config()
ApiV1 = client.CoreV1Api()
AppV1 = client.AppsV1Api()

class KubernetesPod:
    def __init__(self, pod_name, pod_status, pod_ip, node_name, sum_pod_container, number_container_ready):
        self.pod_name = pod_name
        self.pod_status = pod_status
        self.pod_ip = pod_ip
        self.node_name = node_name
        self.sum_pod_container = sum_pod_container
        self.number_container_ready = number_container_ready
def list_namespaced_pod_status(target_namespace: str = "default"):
    list_pod_status = []
    api_get_pods_response = ApiV1.list_namespaced_pod(target_namespace)
    for pod in api_get_pods_response.items:
        current_pod_name = pod.metadata.name
        current_node_name = pod.spec.node_name
        current_pod_ip = pod.status.pod_ip
        current_pod_state = ""
        if pod.metadata.deletion_timestamp != None and (pod.status.phase == 'Running' or pod.status.phase == 'Pending'):
            current_pod_state = 'Terminating'
        elif pod.status.phase == 'Pending':
            try:
                for container in pod.status.container_statuses:
                    if container.state.waiting != None:
                        current_pod_state = container.state.waiting.reason
            except:
                current_pod_state = 'Pending'
        else:
            current_pod_state = str(pod.status.phase)
        try:
            sum_pod_container = len(pod.status.container_statuses)
        except:
            sum_pod_container = 0
        number_container_ready = 0
        if pod.status.container_statuses != None:
            for container in pod.status.container_statuses:
                if container.ready == True:
                    number_container_ready += 1
        list_pod_status.append(KubernetesPod(
            current_pod_name, current_pod_state, current_pod_ip, current_node_name, sum_pod_container, number_container_ready))
    return list_pod_status
a = list_namespaced_pod_status()
print(a)