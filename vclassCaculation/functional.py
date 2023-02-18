from datetime import datetime
import csv
from constants import *

def generate_file_time():
    localdate = datetime.now()
    generate_file_time = "{}_{}_{}_{}h{}".format(
        localdate.day, localdate.month, localdate.year, localdate.hour, localdate.minute)
    return generate_file_time


def write_to_csv(data, file_name):
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
