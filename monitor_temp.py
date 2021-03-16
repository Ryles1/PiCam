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
        try:
            num_measurements = int(sys.argv[1])
        except IndexError:
            num_measurements = 40
        for _ in range(num_measurements):
                m.get_temps()
                sleep(1800)




# TODO: use weather API to also get ambient temperature and store in array, and plot that as well
