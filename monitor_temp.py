#! python3

import sys
import TempMonitor
from os import getenv
import dotenv
import keyboard
import datetime


dotenv.load_dotenv()

API_KEY = getenv('WEATHER_API')
CITY = getenv('CITY')
PROVINCE = getenv('PROVINCE')
COUNTRY = getenv('COUNTRY')

if __name__ == '__main__':
    m = TempMonitor.TempMonitor(CITY, PROVINCE, COUNTRY, API_KEY)
    # TODO: UPDATE THIS TO TAKE ARGUMENT FLAGS FOR TIME, MEASUREMENTS
    start = datetime.datetime.now()
    fifteen = datetime.timedelta(minutes=15)
    try:
        num_measurements = int(sys.argv[1])
    except IndexError:
        num_measurements = 40
    m.get_temps()
    while True:
        diff = datetime.datetime.now() - start
        if diff > fifteen:
            m.get_temps()
        elif keyboard.is_pressed('q'):
            with open('temp_log.txt', 'w') as f:
                for i in range(len(m.cpu_temps.values())):
                    temp = list(m.cpu_temps.values())[0][i]
                    time_dt = list(m.cpu_temps.values())[1][i]
                    time_str = time_dt.strftime("%D/%M/%Y %H:%M:%S")
                    f.write(f'Time: {time_str}, temp: {temp}')
            m.line_plot()
            sys.exit()
