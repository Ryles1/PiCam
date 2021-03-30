import unittest
from TempMonitor import TempMonitor
import dotenv
from os import getenv, listdir
import datetime

dotenv.load_dotenv()
API_KEY = getenv('WEATHER_API')
CITY = getenv('CITY')
PROVINCE = getenv('PROVINCE')
COUNTRY = getenv('COUNTRY')

class TestTempMonitor(unittest.TestCase):
    def testplot(self):
        m = TempMonitor(CITY, PROVINCE, COUNTRY, API_KEY)
        temps = [1, 2, 3, 4, 5]
        delta = datetime.timedelta(minutes=15)
        times = [datetime.datetime.now() + i * delta for i in range(5)]
        m.line_plot(times=times, temps=temps)
        files = listdir()
        check = True in list(map(lambda x: x.endswith('.jpg'), files))
        self.assertTrue(check)


    def test_ambient(self):
        m = TempMonitor(CITY, PROVINCE, COUNTRY, API_KEY)
        ambient = m.get_ambient()
        self.assertIsNotNone(ambient, msg='Test failed - ambient is None')


if __name__ == '__main__':
    unittest.main()