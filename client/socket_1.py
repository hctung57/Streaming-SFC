import librtmp

# Create a connection
conn = librtmp.RTMP("rtmp://localhost/live/stream", live=True)
# Attempt to connect
conn.connect()
# Get a file-like object to access to the stream
stream = conn.create_stream(update_buffer=True)
# print(1)
# file = open("file.mp4", 'wb')
# a = conn.process_packets()

while conn.connected:
    packet, send_request_time, start_receive_time, receive_complete_time = conn.read_packet()
    if packet:
        print("send_request_time:",send_request_time)
        print("start_receive_time:",start_receive_time)
        print("receive_complete_time:",receive_complete_time)
        packet.dump()
        print(packet.packet)
        # file.write(packet.body)
        # file.flush()
    else:
        print("End of stream")
        break
