import kubernetesAPI

a = kubernetesAPI.list_namespaced_service()
for qq in a:
    print(a[0])