#!/usr/bin/env python3

import os
from recognizer import Recognizer
import RPi.GPIO as GPIO
import time
import requests
import datetime

recognizer_filename = '/home/pi/tracker/static/trained.yml'
if not os.path.isfile(recognizer_filename): exit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)

rec = Recognizer(recognizer_filename=recognizer_filename, source=0)
URL = 'http://192.168.1.10/api/attendance/'

while True:
    if not GPIO.input(17):
        user = rec.get_label()
        data = {'user': user, 'date': datetime.datetime.now()}
        with open('log.txt', 'a+') as log:
            log.write(str(data))
            log.write('\n')
            if user is not None and user > -1:
                response = requests.post(URL, data=data)
                log.write(str(response))
                log.write('\n')
            log.flush()
        time.sleep(1)
