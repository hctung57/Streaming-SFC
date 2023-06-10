import librtmp
import logging
import configargparse
import threading


def parser_args():
    parser = configargparse.ArgParser(formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--source_rtmp_1",
                        help="source stream 1 path")
    parser.add_argument("-name", "--source_name_1",
                        help="source stream 1 path")
    parser.add_argument("-rep", "--repp",
                        help="rep")
    return parser.parse_args()


def calculate_bitrate(packet_size: int, duration: int):
    bitrate = (packet_size * 8) / duration
    return bitrate


# parser init
args = parser_args()
source_rtmp_1 = args.source_rtmp_1
source_name_1 = args.source_name_1
rep = args.repp
url_1 = f'rtmp://{source_rtmp_1}/live/stream'

logging.basicConfig(filename='packet/' + source_name_1+'-'+rep + '.log', level=logging.INFO,
                    format='%(number_video_packet)s - %(send_request_time)s - %(start_receive_time)s - '
                           '%(receive_complete_time)s - %(timestamp)s - %(current_bitrate)s')

def rtmp_connect(function: str, url: str):
    conn = librtmp.RTMP(url, live=True)
    conn.connect()
    stream = conn.create_stream(update_buffer=True)
    number_video_packet = 0
    pre_packet_timestamp = 0
    current_bitrate = 0
    print("Start capture packet")
    while conn.connected:
        packet, send_request_time, start_receive_time, receive_complete_time = conn.read_packet()
        if packet:
            if packet.channel == 7:
                if number_video_packet != 0:
                    current_duration = packet.timestamp - pre_packet_timestamp
                    print(function, "Packet size:", packet.packet.m_nBodySize)
                    current_bitrate = calculate_bitrate(
                        packet_size=packet.packet.m_nBodySize, duration=current_duration)
                    pre_packet_timestamp = packet.timestamp
                number_video_packet += 1
                logging.info('', extra={
                    'number_video_packet': number_video_packet, 'send_request_time': send_request_time,
                    'start_receive_time': start_receive_time, 'receive_complete_time': receive_complete_time,
                    'timestamp': packet.timestamp, 'current_bitrate': current_bitrate,})
        else:
            print("End of stream")
            break

rtmp_connect(source_name_1, url_1)
