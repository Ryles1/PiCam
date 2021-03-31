#! python3

import sys
import TempMonitor
from os import getenv
import dotenv
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
    while len(m.cpu_temps['temps']) < num_measurements:
        diff = datetime.datetime.now() - start
        if diff > fifteen:
            m.get_temps()
    m.save_log()
    m.line_plot()

# TODO: email figure to myself
