import librtmp
import logging

logging.basicConfig(filename='buffer.log', level=logging.INFO,
                    format='%(number_video_packet)s - %(send_request_time)s - %(start_receive_time)s - '
                           '%(receive_complete_time)s - %(timestamp)s - %(current_bitrate)s')


def calculate_bitrate(packet_size: int, duration: int):
    bitrate = (packet_size * 8) / duration
    return bitrate


conn = librtmp.RTMP("rtmp://localhost/live/stream", live=True)
conn.connect()
stream = conn.create_stream(update_buffer=True)
number_video_packet = 0
pre_packet_timestamp = 0
current_bitrate = 0
while conn.connected:
    packet, send_request_time, start_receive_time, receive_complete_time = conn.read_packet()
    if packet:
        if packet.channel == 7:
            if number_video_packet != 0:
                current_duration = packet.timestamp - pre_packet_timestamp
                current_bitrate = calculate_bitrate(
                    packet_size=packet.packet.m_nBodySize, duration=current_duration)
                pre_packet_timestamp = packet.timestamp
            number_video_packet += 1
            logging.info('', extra={
                'number_video_packet': number_video_packet, 'send_request_time': send_request_time,
                'start_receive_time': start_receive_time, 'receive_complete_time': receive_complete_time,
                'timestamp': packet.timestamp, 'current_bitrate': current_bitrate, })
    else:
        print("End of stream")
        break
