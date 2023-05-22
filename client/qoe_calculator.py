# import time

# QoE arguments
alpha = 1
beta = 1.85
gamma = 1
theta = 0.5
MIN_QOE = -1e4

# add I-frame and p frame to a packet
# qoe = alpha * quality / 1000 - beta * rebuff/ 1000 - gamma * smooth / 1000


def pre_handle_data(buffer_data_file_name: str):
    with open(buffer_data_file_name, 'r') as file:
        lines = file.readlines()
    sum_bitrate = 0
    average_bitrate = 0
    data = []
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split('-')
            index = int(parts[0].strip())
            send_request_time = float(parts[1].strip())
            start_receive_time = float(parts[2].strip())
            receive_complete_time = float(parts[3].strip())
            timestamp = float(parts[4].strip())
            bitrate = float(parts[5].strip())
            sum_bitrate += bitrate
            entry = {
                'index': index,
                'send_request_time': send_request_time,
                'start_receive_time': start_receive_time,
                'receive_complete_time': receive_complete_time,
                'timestamp': timestamp,
                'bitrate': bitrate
            }
            data.append(entry)
    average_bitrate = sum_bitrate/len(data)
    compare_bitrate_value = 3*average_bitrate
    packet_index = 0
    pre_position_key_frame = None
    pre_key_frame_info = None
    pre_frame_info = None
    bitrate = 0
    packet_data = []
    for index, i in enumerate(data):
        if i['bitrate'] > compare_bitrate_value:
            if pre_key_frame_info != None:
                bitrate = bitrate/(index - pre_position_key_frame)
                entry = {
                    'index': packet_index,
                    'send_request_time': pre_key_frame_info['send_request_time'],
                    'start_receive_time': pre_key_frame_info['start_receive_time'],
                    'receive_complete_time': pre_frame_info['receive_complete_time'],
                    'timestamp': int(i['timestamp']) - int(pre_key_frame_info['timestamp']),
                    'bitrate': bitrate
                }
                packet_data.append(entry)
                packet_index += 1
            pre_key_frame_info = i
            pre_position_key_frame = index
        bitrate += int(i['bitrate'])
        pre_frame_info = i
    return packet_data


data = pre_handle_data("buffer.log")
t0 = data[0]['receive_complete_time']
# for index , packet in enumerate(data):
    