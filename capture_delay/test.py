import subprocess
import logging

logging.basicConfig(filename='ffmpeg.log', level=logging.INFO, format='%(asctime)s %(message)s')
cmd = ['ffmpeg','-i', '-f v4l2 -i /dev/video0', '-c:a', 'copy', 'out.wav', '-y']

process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

logging.info(process.stdout)
logging.error(process.stderr)