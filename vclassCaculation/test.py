from kubernetes import client, config
from VNFInfomation import *
from constants import *
config.load_kube_config()
ApiV1 = client.CoreV1Api()
AppV1 = client.AppsV1Api()


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
                            node_name=target_node
                        )]
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

# SOURCE_STREAMING_VNF.environment_variable = [client.V1EnvVar(name='SOURCE_STREAM_SERVICE', value=''),
#                                              client.V1EnvVar(name='SOURCE_RTMP_PORT', value='')]
# SOURCE_STREAMING_VNF.node_name = CLOUD

def test():
    a = 1
    b = 2
    c = 3
    return a, b, c

ss = [{'a':a1, 'b':b1, 'c':c1}]