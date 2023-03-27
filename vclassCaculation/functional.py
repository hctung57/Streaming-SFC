from datetime import datetime
import csv
import pandas as pd
from constants import *

def generate_file_time():
    localdate = datetime.now()
    generate_file_time = "{}_{}_{}_{}h{}".format(
        localdate.day, localdate.month, localdate.year, localdate.hour, localdate.minute)
    return generate_file_time


def write_to_csv(data, file_name):
    if data != None:
        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
    return

def write_log_data_to_csv(data, file_name):
    fps_values = []
    if data != None:
        data = data.decode().split("\n")
        for line in data:
            if "FPS" in line:
                fps = float(line.split('FPS:')[1].split()[0])
                fps_values.append(fps)
        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in fps_values:
                value = []
                value.append(row)
                writer.writerow(value)
    return