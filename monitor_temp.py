#! python3

import sys
import TempMonitor
from os import getenv, listdir
import dotenv
import datetime
import smtplib
import ssl
from email.message import EmailMessage


dotenv.load_dotenv()

API_KEY = getenv('WEATHER_API')
CITY = getenv('CITY')
PROVINCE = getenv('PROVINCE')
COUNTRY = getenv('COUNTRY')
FROM_ADDR = getenv('FROM_ADDR')
TO_ADDR = getenv('TO_ADDR')
PASSWORD = getenv('PASSWORD')


def send_graph(filename):
    # gather message data
    global FROM_ADDR, TO_ADDR
    today = datetime.datetime.today().strftime('%D-%Y')
    port = 587
    subject = f'Temperature graph on {today} from PiCam!'
    body = 'See attached graph!'

    # create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_ADDR
    msg['To'] = TO_ADDR
    msg['Body'] = body

    # load the jpg
    with open(filename, 'rb') as f:
        img_data = f.read()
    msg.add_attachment(img_data, maintype='image', subtype='image/jpeg')

    # log in to server and send mail
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.office365.com', port) as server:
        server.starttls(context=context)
        server.login(FROM_ADDR, PASSWORD)
        server.send_message(msg, FROM_ADDR, TO_ADDR)


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
