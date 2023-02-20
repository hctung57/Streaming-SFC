from lib2to3.pgen2.token import COLON, SLASH

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
CLOUD = "node2"
EDGE = "node1"

# Directory
DATA_PROMETHEUS_FILE_DIRECTORY = "/home/server1/virtualclassroom-SFC/vclassCaculation/results/{}/data_prom_sfc_{}_{}_repeat_time_{}.csv"
DATA_PROMETHEUS_FILE_NODE_DIRECTORY = "/home/server1/virtualclassroom-SFC/vclassCaculation/results/{}/data_prom_nodes_{}_repeat_time_{}.csv"
DATA_PROMETHEUS_FOLDER_DIRECTORY = "/home/server1/virtualclassroom-SFC/vclassCaculation/results/{}"

# Prometheus query

CPU_NODE_QUERY = "100 - (avg by (instance, job)(irate(node_cpu_seconds_total{}[1m])) *100)"
MEMORY_NODE_QUERY = "((node_memory_MemTotal_bytes{}-node_memory_MemFree_bytes{}-node_memory_Cached_bytes{}-node_memory_Buffers_bytes{})/node_memory_MemTotal_bytes{})*100 "
BANDWIDTH_RECEIVE_NODE_QUERY = "rate(node_network_receive_bytes_total{}[1m])"
BANDWIDTH_TRANSMIT_NODE_QUERY= "rate(node_network_transmit_bytes_total{}[1m])"