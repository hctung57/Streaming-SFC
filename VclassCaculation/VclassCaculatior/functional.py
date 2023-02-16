from datetime import datetime
import csv
from constants import *

def generate_file_time():
    localdate = datetime.now()
    generate_file_time = "{}_{}_{}_{}h{}".format(
        localdate.day, localdate.month, localdate.year, localdate.hour, localdate.minute)
    return generate_file_time


def write_to_csv(data, file_name, fieldnames):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
a = generate_file_time()
print(a)
DATA_PROMETHEUS_FILE_DIRECTORY.format(a,a,"1","1")
print(DATA_PROMETHEUS_FILE_DIRECTORY)