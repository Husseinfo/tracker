#!/usr/bin/env python3

import os
from recognizer import Recognizer
import RPi.GPIO as GPIO
import time

recognizer_filename = '../../static/trained.yml'
if not os.path.isfile(recognizer_filename): exit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)

rec = Recognizer(recognizer_filename=recognizer_filename, source=0)

while True:
    if not GPIO.input(17):
        detected = rec.get_label()
        print(detected)
        time.sleep(1)
