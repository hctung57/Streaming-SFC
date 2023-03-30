from constants import *
import csv
name = "match-av-1-deployment-665dccc67c-lhmjj"
def write_log_data_to_csv(pod_name, file_name):
    if ( NFV_TRANSCODER_SERVICE_NAME in pod_name or NFV_MATCH_AUDIO_VIDEO_SERVICE_NAME in pod_name 
        or NFV_SOURCE_STREAMING_SERVICE_NAME in pod_name):
        fps_values = []
        with open('results/temp/temp.log', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                fps = float(row[0].split('fps=')[1].split()[0])
                value = []
                value.append(fps)
                value.append(pod_name)
                fps_values.append(value)
            with open(file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in fps_values:
                    writer.writerow(row)
                    
    elif NFV_BACKGROUND_BLUR_SERVICE_NAME in pod_name:
        fps_values = []
        with open('results/temp/temp.log', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                value = []
                fps = float(row[1].split('FPS:')[1].split()[0])
                value.append(fps)
                value.append(pod_name)
                fps_values.append(value)
            with open(file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in fps_values:
                    writer.writerow(row)
    else:
        fps_values = []
        with open('results/temp/temp.log', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                fps = float(row[1].split('FPS:')[1].split()[0])
                verify = (row[1].split('VERIFY:')[1].split()[0])
                value = []
                value.append(fps)
                value.append(verify)
                value.append(pod_name)
                fps_values.append(value)
            with open(file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in fps_values:
                    writer.writerow(row)
                    
file = "results/test.csv"
write_log_data_to_csv(name,file)