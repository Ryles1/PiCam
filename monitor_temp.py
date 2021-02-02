import os
import datetime
from time import sleep

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        tzdelta = datetime.timezone(datetime.timedelta(hours=-7))
        dt = datetime.datetime.now(tz=tzdelta)
        time = dt.strftime("%m/%d/%Y, %H:%M:%S")
        return time, temp

while True:
        time, temp = measure_temp()
        with open("temp_log.txt", 'a') as f:
                f.write(f'Time: {time}, {temp}')
        sleep(1800)

