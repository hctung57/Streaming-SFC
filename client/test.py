import librtmp
import struct

# Create a connection
conn = librtmp.RTMP("rtmp://localhost/live/stream", live=True)
# Attempt to connect
conn.connect()
# Get a file-like object to access to the stream
stream = conn.create_stream(update_buffer=True)
i = 0
file = open(f"data/file{i}.mp4", 'wb')

while True:
    data = stream.read(2048000)
    # print("data read from buffer:",data)
    if data:
        # print(data)
        file.write(data)
        file.flush()
        print(i)
        i = i + 1
    else:
        break
