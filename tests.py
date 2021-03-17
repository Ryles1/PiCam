import unittest
from TempMonitor import TempMonitor
import dotenv
from os import getenv

dotenv.load_dotenv()
API_KEY = getenv('WEATHER_API')
CITY = getenv('CITY')
PROVINCE = getenv('PROVINCE')
COUNTRY = getenv('COUNTRY')

class TestTempMonitor(unittest.TestCase):
    def testplot(self):
        pass

    def test_ambient(self):
        m = TempMonitor(CITY, PROVINCE, COUNTRY, API_KEY)
        ambient = m.get_ambient()
        self.assertIsNotNone(ambient, msg='Test failed - ambient is None')


if __name__ == '__main__':
    unittest.main()