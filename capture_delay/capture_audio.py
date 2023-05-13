import threading
import time
import logging
import  datetime
import configargparse
import os
import re
logging.basicConfig(filename='delay.log', filemode='a', level=logging.INFO,
                    format='time: %(time)s - func: %(function_name)s')
# parser func


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


# parser init
args = parser_args()
source_rtmp_1 = args.source_rtmp_1
source_name_1 = args.source_name_1
source_rtmp_2 = args.source_rtmp_2
source_name_2 = args.source_name_2

# def read_log_file(name_of_func: str):
#     filepath = f'./{name_of_func}.log'
#     with open(filepath, 'r') as f:
#         last_line = f.readlines()[-1]
#     time_pattern = r"time=(\d{2}:\d{2}:\d{2}\.\d{2})"
#     time_match = re.search(time_pattern, last_line)
#     if time_match:
#         time_str = time_match.group(1)
#         time_parts = time_str.split(":")
#         hours = int(time_parts[0])
#         minutes = int(time_parts[1])
#         seconds_parts = time_parts[2].split(".")
#         seconds = int(seconds_parts[0])
#         milliseconds = int(seconds_parts[1])
#         total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds/100
#         return total_seconds
#     return

def read_log_file(name_of_function: str):
    filepath = f'./{name_of_function}.log'
    mod_time = os.path.getmtime(filepath)
    return mod_time

def capture_streaming(name_of_function: str, url: str):
    print("connected:", name_of_function)
    capture_time = time.monotonic()
    logging.info('', extra={'time': f'{capture_time}',
                 'function_name': f'{name_of_function}_start'})
    command = f'ffmpeg -analyzeduration 1 -fflags nobuffer -probesize 32 -re -i rtmp://{url}/live/audio -c:a copy out.wav -loglevel quiet -stats 2> {name_of_function}.log -y'
    os.system(command)

th1 = threading.Thread(target=capture_streaming, args=(
    source_name_1, source_rtmp_1)).start()
th2 = threading.Thread(target=capture_streaming, args=(
    source_name_2, source_rtmp_2)).start()

time.sleep(120)
logging.info('', extra={'time': f'{read_log_file(source_name_1)}',
                 'function_name': f'{source_name_1}_end'})
logging.info('', extra={'time': f'{read_log_file(source_name_2)}',
                 'function_name': f'{source_name_2}_end'})

os._exit(0)

