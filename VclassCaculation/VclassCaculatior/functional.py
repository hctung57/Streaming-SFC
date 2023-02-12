from datetime import datetime

def generate_file_time():
    localdate = datetime.now()
    generate_file_time = "{}_{}_{}_{}h{}".format(
        localdate.day, localdate.month, localdate.year, localdate.hour, localdate.minute)
    return generate_file_time