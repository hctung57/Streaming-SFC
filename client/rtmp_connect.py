import librtmp
import logging
import configargparse

logging.basicConfig(filename='buffer.log', level=logging.INFO,
                    format='%(number_video_packet)s - %(send_request_time)s - %(start_receive_time)s - '
                           '%(receive_complete_time)s - %(timestamp)s - %(current_bitrate)s')


def parser_args():
    parser = configargparse.ArgParser(description="Capture delay NFV FIL HUST",
                                      formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s1", "--source_rtmp_1",
                        help="source stream 1 path")
    parser.add_argument("-name1", "--source_name_1",
                        help="source stream 1 path")
    parser.add_argument("-s2", "--source_rtmp_2",
                        help="source stream 2 path")
    parser.add_argument("-name2", "--source_name_2",
                        help="source stream 2 path")
    return parser.parse_args()


def calculate_bitrate(packet_size: int, duration: int):
    bitrate = (packet_size * 8) / duration
    return bitrate


# parser init
args = parser_args()
source_rtmp_1 = args.source_rtmp_1
source_name_1 = args.source_name_1
source_rtmp_2 = args.source_rtmp_2
source_name_2 = args.source_name_2
url_1 = f'rtmp://{source_rtmp_1}/live/stream'
url_2 = f'rtmp://{source_rtmp_2}/live/stream'


def rtmp_connect(url: str, file_name: str):
    file_name = 'packet' + file_name + '.log'
    logging.basicConfig(filename=file_name, level=logging.INFO,
                        format='%(number_video_packet)s - %(send_request_time)s - %(start_receive_time)s - '
                               '%(receive_complete_time)s - %(timestamp)s - %(current_bitrate)s')
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
                    print("Packet size:", packet.packet.m_nBodySize)
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
