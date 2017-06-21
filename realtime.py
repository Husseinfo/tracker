#!/usr/bin/env python3

import cv2
import RPi.GPIO as GPIO
import time
import requests
import datetime
import base64

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

video_capture = cv2.VideoCapture(0)
URL = 'http://127.0.0.1:8000/api/attendance/'
while True:
    if not GPIO.input(17):
        print("pressed")
        images = []
        for i in range(3): video_capture.read()
        for i in range(3):
            img = video_capture.read()[1]
            name = 'temp' + str(i) + '.png'
            cv2.imwrite(name, img)
            with open(name, 'rb') as file:
                images.append(base64.b64encode(file.read()).decode('utf-8'))
        date = time.mktime(datetime.datetime.now().timetuple())
        data = {'images': images, 'date': date, 'inout': None}
        response = requests.post(URL, json=data)
        response.c
        print(response.status_code)
        time.sleep(5)
