import Player


# QoE arguments
# alpha = 1
# beta = 1.85
# gamma = 1
# theta = 0.5
# MIN_QOE = -1e4

# add I-frame and p-frame to a packet
# qoe = 1 * quality / 1000 - 1.85 * rebuff/ 1000 - 1 * smooth / 1000


def pre_handle_data(buffer_data_file_name: str):
    with open(buffer_data_file_name, 'r') as file:
        lines = file.readlines()
    sum_bitrate = 0
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
    print('average bitrate:',average_bitrate)
    compare_bitrate_value = 6*average_bitrate
    packet_index = 0
    pre_position_key_frame = None
    pre_key_frame_info = None
    pre_frame_info = None
    bitrate = 0
    packet_data = []
    for index, i in enumerate(data):
        if i['bitrate'] > compare_bitrate_value:
            if pre_key_frame_info is not None:
                bitrate = bitrate/(index - pre_position_key_frame)
                entry = {
                    'index': packet_index,
                    'send_request_time': pre_key_frame_info['send_request_time']*1000,
                    'start_receive_time': pre_key_frame_info['start_receive_time']*1000,
                    'receive_complete_time': pre_frame_info['receive_complete_time']*1000,
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


# def get_smooth(data, downloaded_chunk_id, chunk_id):
#     # the fist packet
#     if downloaded_chunk_id == 0 and chunk_id == 0:
#         return 0
#     if downloaded_chunk_id < chunk_id:
#         return 0
#     else:
#         smooth = abs(data[chunk_id]['bitrate'] - data[chunk_id - 1]['bitrate'])
#         return smooth


# def calculate_qoe(filename: str):
#     data = pre_handle_data(filename)
#     played_time = 0
#     downloaded_chunk_id = 1
#     number_of_chunk = len(data) - 1
#     t0 = data[0]['receive_complete_time']
#     QoE = 0
#     action_chunk_id = 0
#     while action_chunk_id <= number_of_chunk:
#         rebuf = 0
#         # check all packet downloaded
#         for packet in range(downloaded_chunk_id, number_of_chunk + 1):
#             if t0 + played_time >= data[packet]['receive_complete_time']:
#                 # print(data[packet])
#                 downloaded_chunk_id = packet
#         smooth = get_smooth(data=data, downloaded_chunk_id=downloaded_chunk_id, chunk_id=action_chunk_id)
#         buffer = data[action_chunk_id]['receive_complete_time'] - t0
#         # print("player is going to play packet", action_chunk_id, 'with timestamp: ', t0 + played_time)
#         # print("downloaded", downloaded_chunk_id, 'packet, received time',
#         #       data[action_chunk_id]['receive_complete_time'])
#         print("action chunk id fist",action_chunk_id)
#         print("downloaded chunk id second", downloaded_chunk_id)
#         if action_chunk_id <= number_of_chunk - 2:
#             if action_chunk_id <= downloaded_chunk_id - 1:
#                 # play chunk with timestamp
#                 played_time += data[action_chunk_id]['timestamp']
#                 print("buffer", data[downloaded_chunk_id]['receive_complete_time'] - t0 - played_time, t0 + played_time, data[downloaded_chunk_id]['receive_complete_time'])
#                 action_chunk_id += 1
#             else:
#                 downloaded_chunk_id += 1
#                 print("**rebuffer:", data[downloaded_chunk_id]['receive_complete_time'] - t0 - played_time,t0 + played_time,data[downloaded_chunk_id]['receive_complete_time'])
#                 played_time += data[downloaded_chunk_id]['receive_complete_time'] - t0 - played_time
#         else:
#             if action_chunk_id <= downloaded_chunk_id:
#                 played_time += data[action_chunk_id]['timestamp']
#                 print("buffer", data[downloaded_chunk_id]['receive_complete_time'] - t0 - played_time, t0 + played_time, data[downloaded_chunk_id]['receive_complete_time'])
#                 action_chunk_id += 1
#             else:
#                 downloaded_chunk_id += 1
#                 print("**rebuffer:", data[downloaded_chunk_id]['receive_complete_time'] - t0 - played_time,t0 + played_time,data[downloaded_chunk_id]['receive_complete_time'])
#                 played_time += data[downloaded_chunk_id]['receive_complete_time'] - t0 - played_time
#         print(action_chunk_id,played_time)


# calculate_qoe("buffer.log")
a = Player.Player(pre_handle_data('buffer.log'))
a.run()