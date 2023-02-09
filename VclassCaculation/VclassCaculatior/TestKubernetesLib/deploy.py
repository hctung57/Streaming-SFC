from flask import Flask, render_template,request
import requests
import json
from kubernetes import client, config
from pprint import pprint

config.load_kube_config()

appsv1 = client.AppsV1Api()
corev1 = client.CoreV1Api()

# ret_deploy = appsv1.list_deployment_for_all_namespaces()

app = Flask(__name__)


def pod_deployment(data,test) :
    # if request.method == 'POST':
    #     f = request.data
    #     data = json.loads(f)
        
    # id = data['idt'] # co nhieu svc, moi svc co 1 name => data['idt][??]
    allService = data['service']
    nodeAffinity = data['NodeAffinity']
    lengthAllService = len(allService)
    a = 0
    for i in allService:

        name_metadata_deploy = i + data['idt'] +"-deployment"

        selector_matchLabels_deploy = {"app": i + "-deployment", "ID": data['idt']}

        labels_metadata_template_deploy = {"app": i + "-deployment","pod-template-hash":data['idt'] , "ID": data['idt']}

        nameImageHead, nameImageSep, nameImageTail=  i.partition(':')
        Image= i
        portContainerHead, portContainerHeadSep, portContainerHeadTail = data['port'][i].partition(':')
        
        portContainerList = [client.V1ContainerPort(container_port=int(portContainerHead)),client.V1ContainerPort(container_port=int(9900))]


        # cho vong lap for kiem tra so luong trong file json de biet duoc so luong port tu do them dung so luong vao portContainerList

        # portContainerHead chi dung khi ma json chi co 1 port 80:5000
        # portContainerHead se chua du khi co >= 2 port 80:5000, 81:5001, 6000:5900
        nodeSelector_Pod = {"kubernetes.io/hostname": nodeAffinity[a]}
        
        pod_spec=client.V1PodSpec(containers=[client.V1Container(
                        image=Image,
                        name=nameImageHead,
                        ports=portContainerList)],

                        # ports la 1 list nen em co the them nhieu tham so [1,3,4,5,7,8]

                        node_selector = nodeSelector_Pod) #name="containerport" ????

        deploy_template=client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(
                                labels=labels_metadata_template_deploy), #???
                                spec=pod_spec)
        
        deploy_spec=client.V1DeploymentSpec(
                                replicas=1,
                                selector=client.V1LabelSelector(match_labels=selector_matchLabels_deploy), #???? #sua lan 1
                                template=deploy_template)

        deploy=client.V1Deployment(kind="Deployment",
                                metadata=client.V1ObjectMeta(name=name_metadata_deploy),
                                spec=deploy_spec)    
        deploy_result=appsv1.create_namespaced_deployment(namespace="default",body=deploy)
        a+=1
        pprint(deploy_result)
    test=True
    return test

# @app.route('/registSFC', methods=['POST', 'GET'] )
def service_deployment(data,test):
    # if request.method == 'POST':
    #     f = request.data
    #     data = json.loads(f)

    allService = data['service']
    nodeAffinity = data['NodeAffinity']
    lengthAllService = len(allService)
    
    
    for i in allService:
        port_spec_head, port_spec_mid, port_spec_tail = data['port'][i].partition(':')
        name_metadata_svc = i + "-"+ data['idt'] +"-svc"
        
        port_ports_spec = port_spec_head
        target_port_port = port_spec_tail
        selector_svc = {"app": i + "-deployment", "ID": data['idt']}

        service_spec=client.V1ServiceSpec(type="ClusterIP",
                        ports=[client.V1ServicePort(target_port=int(target_port_port),port=int(port_ports_spec))],
                        selector=selector_svc)

        service=client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=name_metadata_svc),
            spec=service_spec)
        service_result=corev1.create_namespaced_service(namespace="default",body=service)
        pprint(service_result)
    test = True
    return test
    
@app.route('/registSFC', methods=['POST', 'GET'] )
def launch():
    check_pod = False
    check_svc = False
    if request.method == 'POST':
        f = request.data
        data = json.loads(f)
        check_pod = pod_deployment(data,check_pod)
        if check_pod == False:
            return 'Unsucccessful Pods Deployment'
        check_svc = service_deployment(data,check_svc)
        if check_svc == False:
            return 'Unsuccessful Services Deployment'
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001')