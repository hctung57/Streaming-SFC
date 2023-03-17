from os import system
log = []
log.append(system("kubectl exec -it background-blur-1-deployment-6c69dfb9d9-kr2cg -- cat nginx.sh"))
print(log[0])