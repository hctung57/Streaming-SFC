import threading
import time
import os
# custom library
import functional
import kubernetesAPI
import deployment
from constants import *
import VNFInfomation

SFC1 = [[VNFInfomation.SOURCE_STREAMING_VNF],
	[VNFInfomation.MATCH_AUDIO_VIDEO_VNF]]

SFC2 = [[VNFInfomation.SOURCE_STREAMING_VNF],
	[VNFInfomation.BACKGROUND_BLUR_VNF]]

SFC3 = [[VNFInfomation.SOURCE_STREAMING_VNF],
	[VNFInfomation.FACE_DETECTION_VNF]]

SFC4 = [[VNFInfomation.SOURCE_STREAMING_VNF],
	[VNFInfomation.TRANSCODER_VNF]]

SFC5 = [[VNFInfomation.SOURCE_STREAMING_VNF],
	[],
	[VNFInfomation.NOISE_SUPRESS_VNF]]

SFC6 = [[VNFInfomation.SOURCE_STREAMING_VNF],
	      [VNFInfomation.BACKGROUND_BLUR_VNF, VNFInfomation.FACE_DETECTION_VNF, VNFInfomation.TRANSCODER_VNF]]

mesure_function = NFV_SOURCE_STREAMING_SERVICE_NAME

def run_mesure_process(service_name:str, service_ip:str, rep):
	import paramiko
	ssh = paramiko.SSHClient()
	# Auto add host to known hosts
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# Connect to server
	ssh.connect("192.168.101.9", username="fil", password="1")

	command = f'cd /home/fil/tung/virtualclassroom-SFC/client && python3 rtmp_connect.py -name {service_name} -s {service_ip}:1936 -rep {rep}'
	# Do command
	(ssh_stdin, ssh_stdout, ssh_stderr) = ssh.exec_command(command)
	# Get status code of command
	exit_status = ssh_stdout.channel.recv_exit_status()
	# Print status code
	# print ("exit status: %s" % exit_status)
	# # Print content
	# for line in ssh_stderr.readlines():
	# 	print(line.rstrip())
	# Close ssh connect
	ssh.close()

def deploy_sfc_and_get_delay(target_sfc, target_sfc_id: str, file_name: str , time_to_calculate: float):
	start_time = time.monotonic()
	key = '-'+target_sfc_id+'-'
	deployment.create_sfc(target_sfc, target_sfc_id)
	print("[SCENARIO] start calculating delay")
	while (True):
		list_pod_namespaced = kubernetesAPI.list_namespaced_pod_status()
		if time.monotonic() - start_time > time_to_calculate:
			deployment.delete_pod(target_sfc[0][0].service_name, target_sfc_id)
			time.sleep(60)
			# for pod in list_pod_namespaced:
			#     if NFV_DELAY_CALCULATOR_NAME in pod.pod_name:
			#         kubernetesAPI.connect_get_namespaced_pod_exec("cat delay.log > results/temp/temp.log",pod.pod_name)
			deployment.delete_sfc(target_sfc,target_sfc_id)
			break
		else:
			continue

	return

def main(resolution, rep):
	time_to_calculate = 200
	VNFInfomation.NFV_SOURCE_STREAMING_RESOUTION = resolution
	th = threading.Thread(target=deploy_sfc_and_get_delay, args=(SFC6,"1","",time_to_calculate))
	th.start()
	time.sleep(6)
	list_service = kubernetesAPI.list_namespaced_service()
	source_streaming_service = []
	other_service = []
	for service in list_service:
		if mesure_function in service[0]:
			measure_service = service
		# if service[0] != "kubernetes":
		# 	if "source-streaming" in service[0]:
		# 		source_streaming_service = service
		# 	else:
		# 		other_service = service

	th1 = threading.Thread(target=run_mesure_process, args=(f'{measure_service[0]}-{VNFInfomation.NFV_TRANSCODER_RESOUTION}', measure_service[1], rep))
  # th1 = threading.Thread(target=run_mesure_process, args=(f'{source_streaming_service[0]}-{resolution}', source_streaming_service[1]))
	th1.start()
	th1.join()
	th.join()
	#     deploy_sfc_and_get_delay(SFC2,"1","",time_to_calculate)
	print("[SCENARIO] start done")
	return

for i in range(5):
	main(R_1080P, i)
	time.sleep(60)