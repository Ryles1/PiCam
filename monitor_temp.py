#! python3

import sys
import TempMonitor
from os import getenv
import dotenv
import datetime
import smtplib
import ssl


dotenv.load_dotenv()

API_KEY = getenv('WEATHER_API')
CITY = getenv('CITY')
PROVINCE = getenv('PROVINCE')
COUNTRY = getenv('COUNTRY')
FROM_ADDR = getenv('FROM_ADDR')
TO_ADDR = getenv('TO_ADDR')

def send_graph(filename):
    global FROM_ADDR, TO_ADDR
    today = datetime.datetime.today().isoformat()
    port = 587
    message = f'''\
        Subject:  Temperature graph from PiCam!

        Message: See attached graph! '''
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.office365.com', port) as server:
        server.starttls(context=context)
        server.login(FROM_ADDR, '0qk6yd70')
        server.sendmail(FROM_ADDR, TO_ADDR, message)


if __name__ == '__main__':
    m = TempMonitor.TempMonitor(CITY, PROVINCE, COUNTRY, API_KEY)
    # TODO: UPDATE THIS TO TAKE ARGUMENT FLAGS FOR TIME, MEASUREMENTS
    check_time = datetime.datetime.now()
    fifteen = datetime.timedelta(minutes=15)
    try:
        num_measurements = int(sys.argv[1])
    except IndexError:
        num_measurements = 40
    m.get_temps()
    while len(m.cpu_temps['temps']) < num_measurements:
        diff = datetime.datetime.now() - check_time
        if diff > fifteen:
            m.get_temps()
            check_time = datetime.datetime.now()
    m.save_log()
    filename = m.line_plot()
    send_graph(filename)

# TODO: email figure to myself
