import matplotlib.pyplot as plt
from os import popen
import datetime as dt
import requests
import json


class TempMonitor:
    def __init__(self, city, province, country, weather_api):
        self.cpu_temps = {'temps': [], 'times': []}
        self.ambient_temps = {'temps': [], 'times': []}
        self.tzdelta = dt.timezone(dt.timedelta(hours=-7))
        self.city = city
        self.province = province
        self.country = country
        self.weather_api = weather_api

    def get_temps(self):
        temp = int(popen("vcgencmd measure_temp").readline())
        now = dt.datetime.now(tz=self.tzdelta)
        ambient = self.get_ambient(self.city, self.province, self.country)
        self.cpu_temps['temps'].append(temp)
        self.cpu_temps['times'].append(now)
        return

    def line_plot(self):
        times = [t.strftime("%H:%M") for t in self.cpu_temps['times']]
        plt.plot(x=times, y=self.cpu_temps['temps'])
        plt.xlabel('Time')
        plt.ylabel('Temp (degC)')
        plt.show()
        return

    def get_ambient(self, city, prov, country, api_key):
        url = f'api.openweathermap.org/data/2.5/weather?q={city},{prov},{country}&appid={api_key}'
        data = requests.get(url)
        weather_data = json.loads(data)
        ambient_temp = float(weather_data['main']['temp'])
        return ambient_temp