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
        # need to parse this response, gives back a string "temp=31.5'C"
        temp_string = popen("vcgencmd measure_temp").readline()
        temp_num = temp_string.split('=')[1][:4]
        temp = float(temp_num)
        now = dt.datetime.now(tz=self.tzdelta)
        ambient = self.get_ambient(self.city, self.province, self.country, self.weather_api)
        self.cpu_temps['temps'].append(temp)
        self.cpu_temps['times'].append(now)
        self.ambient_temps['temps'].append(ambient)
        self.ambient_temps['times'].append(now)
        return

    def line_plot(self, times=None, temps=None):
        times = times if times is not None else [t.strftime("%I:%M") for t in self.cpu_temps['times']]
        temps = temps if temps is not None else self.cpu_temps['temps']
        ambients = self.ambient_temps['temps']
        if ambients:
            plt.plot(times, temps, 'ro', times, ambients, 'bs')
        else:
            plt.plot(times, temps, 'ro')
        plt.xlabel('Time')
        plt.ylabel('Temp (degC)')
        filename = dt.datetime.strftime(dt.datetime.now(), "%d_%m_%Y") + '_Temp.jpg'
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
        return filename

    def get_ambient(self, city=None, prov=None, country=None, api_key=None):
        # The below is to allow for testing without having to explicitly call the location and api key
        if city is None:
            city = self.city
        if prov is None:
            prov = self.province
        if country is None:
            country = self.country
        if api_key is None:
            api_key = self.weather_api
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{prov},{country}&appid={api_key}'
        data = requests.get(url).text
        weather_data = json.loads(data)
        ambient_temp = float(weather_data['main']['temp'])
        return ambient_temp

    def save_log(self):
        with open('temp_log.txt', 'w') as f:
            for i in range(len(self.cpu_temps.values())):
                temp = self.cpu_temps['temps'][i]  # TODO: IndexError on this line
                time_dt = self.cpu_temps['times'][i]
                time_str = time_dt.strftime("%D/%M/%Y %H:%M:%S")
                f.write(f'Time: {time_str}, temp: {temp}\n')
