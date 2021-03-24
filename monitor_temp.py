#! python3

from time import sleep
import sys
import TempMonitor
from os import getenv
import dotenv


dotenv.load_dotenv()

API_KEY = getenv('WEATHER_API')
CITY = getenv('CITY')
PROVINCE = getenv('PROVINCE')
COUNTRY = getenv('COUNTRY')

if __name__ == '__main__':
    m = TempMonitor.TempMonitor(CITY, PROVINCE, COUNTRY, API_KEY)
    # TODO: UPDATE THIS TO TAKE ARGUMENT FLAGS FOR TIME, MEASUREMENTS
    try:
        num_measurements = int(sys.argv[1])
    except IndexError:
        num_measurements = 40
    try:
        for _ in range(num_measurements):
            m.get_temps()
            sleep(1800)
    except KeyboardInterrupt:
        with open('temp_log.txt', 'w') as f:
            for i in range(len(m.cpu_temps.values())):
                temp = list(m.cpu_temps.values())[0][i]
                time_dt = list(m.cpu_temps.values())[1][i]
                time_str = time_dt.strftime("%D/%M/%Y %H:%M:%S")
                f.write(f'Time: {time_str}, temp: {temp}')
        print('Program exited by keyboard interrupt')
        m.line_plot()
        sleep(10)
        raise SystemExit

