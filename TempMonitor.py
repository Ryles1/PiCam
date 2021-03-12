import numpy as np
from os import popen
import datetime


class TempMonitor:
    def __init__(self):
        self.cpu_temps = {'temps': [], 'times': []}
        self.ambient_temps = []
        self.tzdelta = datetime.timezone(datetime.timedelta(hours=-7))

    def measure_temp(self):
        temp = int(popen("vcgencmd measure_temp").readline())
        dt = datetime.datetime.now(tz=self.tzdelta)
        time = dt.strftime("%m/%d/%Y, %H:%M:%S")
        self.cpu_temps['temps'].append(temp)
        self.cpu_temps['times'].append(time)
        return

