# NFV service name
NFV_FACE_DETECTION_SERVICE_NAME = "face-detection"
NFV_FACE_RECOGNITION_NAME = "face-recognition"
NFV_BACKGROUND_BLUR_SERVICE_NAME = "background-blur"
NFV_SOURCE_STREAMING_SERVICE_NAME = "source-streaming"
NFV_MATCH_AUDIO_VIDEO_SERVICE_NAME = "match-av"
NFV_TRANSCODER_SERVICE_NAME = "transcoder"
NFV_NOISE_SUPPRESS_NAME = "noise-suppress"

# Transcoder resolution
R_1080P = 1080
R_720P = 720
R_480P = 480
R_360P = 360
R_144P = 144

# Node name
CLOUD = "cloud"
EDGE = "edge"

POWER_MONITOR = CLOUD
# Directory
DATA_PROMETHEUS_FILE_DIRECTORY = "/home/server1/virtualclassroom-SFC/vclassCaculation/results/{}/data_prom_sfc_{}_{}_repeat_time_{}.csv"
DATA_PROMETHEUS_FILE_NODE_DIRECTORY = "/home/server1/virtualclassroom-SFC/vclassCaculation/results/{}/data_prom_nodes_sfc_{}_{}_repeat_time_{}.csv"
DATA_PROMETHEUS_FOLDER_DIRECTORY = "/home/server1/virtualclassroom-SFC/vclassCaculation/results/{}"
FPS_FILE_DIRECTORY = "/home/server1/virtualclassroom-SFC/vclassCaculation/results/{}/fps_prom_sfc_{}_{}_repeat_time_{}.csv"
# Prometheus query
POWER_NODE_QUERY = "power_of_node{}"
CPU_NODE_QUERY = "100 - (avg by (instance, job)(irate(node_cpu_seconds_total{}[1m]))*100)"
MEMORY_NODE_QUERY = "((node_memory_MemTotal_bytes{}-node_memory_MemFree_bytes{}-node_memory_Cached_bytes{}-node_memory_Buffers_bytes{})/node_memory_MemTotal_bytes{})*100 "
BANDWIDTH_RECEIVE_NODE_QUERY = "irate(node_network_receive_bytes_total{}[1m])"
BANDWIDTH_TRANSMIT_NODE_QUERY= "irate(node_network_transmit_bytes_total{}[1m])"
CPU_POD_QUERY = "avg(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name='{}', container_label_io_cri_containerd_kind='container'}}[1m]))*100"
MEMORY_POD_QUERY = "sum(container_memory_working_set_bytes{{container_label_io_kubernetes_pod_name='{}'}})"
BANDWIDTH_RECEIVE_POD_QUERY = "irate(container_network_receive_bytes_total{{container_label_io_kubernetes_pod_name='{}'}}[1m])"
BANDWIDTH_TRANSMIT_POD_QUERY = "irate(container_network_transmit_bytes_total{{container_label_io_kubernetes_pod_name='{}'}}[1m])"