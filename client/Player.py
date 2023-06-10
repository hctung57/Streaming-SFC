import numpy as np


class Player:
    def __init__(self, data):
        self.data = data
        self.t0 = data[0]['receive_complete_time']  # ms
        self.number_of_chunk = len(data) - 1
        self.play_timeline = 0  # ms  timeline of real time
        self.play_chunk = 0  # chunk id
        self.downloaded_chunk = 0  # chunk id
        self.buffer_size = 1  # chunk
        self.buffer = 0

    def get_downloaded_time_of_chunk(self, chunk_id: int):
        return self.data[chunk_id]['receive_complete_time']

    def get_bitrate_of_chunk(self, chunk_id: int):
        return self.data[chunk_id]['bitrate']

    def get_duration_of_chunk(self, chunk_id: int):
        return self.data[chunk_id]['timestamp']

    def get_smooth(self):
        # the fist packet
        if self.downloaded_chunk == 0 and self.play_chunk == 0:
            return 0
        if self.downloaded_chunk < self.play_chunk:
            return 0
        else:
            # if self.play_chunk <= self.number_of_chunk:
            smooth = abs(self.get_bitrate_of_chunk(self.play_chunk) - self.get_bitrate_of_chunk(self.play_chunk - 1))
            return smooth
        # return 0

    def download_chunk(self):
        if self.downloaded_chunk < self.number_of_chunk:
            for chunk_id in range(self.downloaded_chunk + 1, self.number_of_chunk):
                if self.get_downloaded_time_of_chunk(chunk_id) <= self.t0 + self.play_timeline:
                    # print(self.get_downloaded_time_of_chunk(chunk_id), self.t0 + self.play_timeline)
                    self.downloaded_chunk = chunk_id
                    self.buffer += self.get_duration_of_chunk(chunk_id)

    def download_delay_chunk(self):
        if self.play_chunk <= self.number_of_chunk:
            self.downloaded_chunk = self.play_chunk
            self.buffer += self.get_duration_of_chunk(self.downloaded_chunk)
            # print('download', self.get_downloaded_time_of_chunk(self.downloaded_chunk), self.t0 + self.play_timeline)
            freezing = self.get_downloaded_time_of_chunk(self.downloaded_chunk) - self.t0 - self.play_timeline
            self.play_timeline += freezing
            return freezing

    def init_buffer_timeline(self):
        # buffer chunk 0
        self.buffer = self.get_duration_of_chunk(0)

    def play_video(self, chunk_id):
        buf = self.buffer - self.get_duration_of_chunk(chunk_id)
        # print(buf, self.buffer, self.get_duration_of_chunk(chunk_id))
        self.play_timeline += np.minimum(self.buffer, self.get_duration_of_chunk(chunk_id))
        self.buffer = np.maximum(buf, 0)
        return buf

    def run(self):
        self.init_buffer_timeline()
        rebuff = 0
        pre_handle_chunk = -1
        QoE = 0
        while self.play_chunk <= self.number_of_chunk:
            print('------------')
            print("Chunk:", self.play_chunk)
            bitrate = self.get_bitrate_of_chunk(self.play_chunk)
            smooth = self.get_smooth()
            buf = self.play_video(self.play_chunk)
            if buf < 0:
                rebuff = self.download_delay_chunk()
                qoe = bitrate / 1000 - 1.85 * rebuff / 1000 - 1 * smooth / 1000
                pre_handle_chunk = self.play_chunk
                print("quality:", bitrate)
                print("Smooth:", smooth)
                print("Re-buffer:", rebuff)
                print("One step QoE:", qoe)
                QoE += qoe
            else:
                if self.play_chunk != pre_handle_chunk:
                    print(bitrate, rebuff, smooth)
                    qoe = bitrate / 1000 - 1.85 * rebuff / 1000 - 1 * smooth / 1000
                    pre_handle_chunk = self.play_chunk
                    print("quality:", bitrate)
                    print("Smooth:", smooth)
                    print("One step QoE:", qoe)
                    QoE += qoe
                else:
                    print("INFO: Skip this chunk because re-buffer")
                self.play_chunk += 1
                rebuff = 0
            self.download_chunk()
        print("------------")
        print("Your QoE is:", QoE)