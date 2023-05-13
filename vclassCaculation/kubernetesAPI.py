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


def list_namespaced_endpoints(target_namespce: str = "default"):
    list_endpoints = []
    get_endpoint_response = ApiV1.list_namespaced_endpoints(target_namespce)
    for endpoint in get_endpoint_response.items:
        entry = {
            "endpoint_name":endpoint.metadata.name,
            "endpoints": []
        }
        list_subnet = []
        if endpoint.subsets != None:
            for subnet in endpoint.subsets:
                ips = []
                ports = []
                if subnet.addresses != None:
                    for address in subnet.addresses:
                        ips.append(address.ip)
                if subnet.ports != None:
                    for port in subnet.ports:
                        ports.append(port.port)
                address = {
                    "ip":ips,
                    "port":ports
                }
                list_subnet.append(address)
        entry["endpoints"] = list_subnet
        list_endpoints.append(entry)
    return list_endpoints

def get_number_namespaced_pod_through_status(target_status: str, target_namespace: str = "default"):
    count = 0
    list_pod = list_namespaced_pod_status(target_namespace)
    for pod in list_pod:
        if pod.pod_status == target_status:
            count += 1
    return count


def create_namespaced_service(target_service: str, target_ID: str,
                              target_service_port: int, target_namespace: str = "default"):
    service_name = target_service + "-" + target_ID + "-service"
    service_selector = target_service + "-" + target_ID + "-deployment"
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=service_name),
        spec=client.V1ServiceSpec(
            selector={"app": service_selector, "ID": target_ID},
            type="ClusterIP",
            ports=[client.V1ServicePort(
                port=target_service_port,
                target_port="container-port")]))
    try:
        response = ApiV1.create_namespaced_service(
            namespace=target_namespace, body=body)
    except:
        return ("There is unknown error when deploy {}.".format(service_name))
    return ("Deploy {} succesfully.".format(service_name))


def create_namespaced_deployment(target_deployment: str, target_ID: str, target_image: str, target_container_port: int,
                                 target_env, target_node, target_namespace: str = "default"):
    deployment_name = target_deployment + "-" + target_ID + "-deployment"
    body = (
        client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(
                name=deployment_name
            ),
            spec=client.V1DeploymentSpec(
                selector=client.V1LabelSelector(
                    match_labels={"app": deployment_name, "ID": target_ID}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={"app": deployment_name, "ID": target_ID}
                    ),
                    spec=client.V1PodSpec(
                        containers=[client.V1Container(
                            name=target_deployment,
                            image=target_image,
                            ports=[client.V1ContainerPort(
                                container_port=target_container_port,
                                name="container-port"
                            )],
                            env=target_env,
                        )],
                        node_name=target_node
                    )
                )
            )

        )
    )
    try:
        response = AppV1.create_namespaced_deployment(
            body=body, namespace=target_namespace)
    except:
        return ("There is unknown error when deploy {}.".format(deployment_name))
    return ("Deploy {} succesfully.".format(deployment_name))


def delete_namespaced_deployment(target_deployment: str, target_ID: str, target_namespace: str = "default"):
    deployment_name = target_deployment + "-" + target_ID + "-deployment"
    try:
        AppV1.delete_namespaced_deployment(deployment_name, target_namespace)
    except:
        return ("There is unknown error when delete {}.".format(deployment_name))
    return ("Delete {} succesfully.".format(deployment_name))


def delete_namespaced_service(target_service: str, target_ID: str, target_namespace: str = "default"):
    service_name = target_service + "-" + target_ID + "-service"
    try:
        ApiV1.delete_namespaced_service(service_name, target_namespace)
    except:
        return ("There is unknown error when delete {}.".format(service_name))
    return ("Delete {} succesfully.".format(service_name))


def connect_get_namespaced_pod_exec(target_command: str, target_name: str):
    command = "kubectl exec -it {} -- {} ".format(
        target_name, target_command)
    try:
        output = subprocess.check_output(['/bin/bash', '-c', command])
    except:
        return
    return output

def list_namespaced_service(target_namespace: str = "default"):
    list_service_info = []
    result = ApiV1.list_namespaced_service(target_namespace)
    if result.items != None:
        for item in result.items:
            name = item.metadata.name
            ip = item.spec.cluster_ip
            list_service_info.append([name,ip])
    return list_service_info