#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import requests
import datetime
import base64
import LCD
import json

TRIG = 16
ECHO = 18
URL = 'http://192.168.0.101:8000/api/attendance/'


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0: a = 0
    start = time.time()
    while GPIO.input(ECHO) == 1: a = 1
    return (time.time() - start) * 340 / 2 * 100


def clear_LCD():
    LCD.lcd_string("---- HELLO -----", 0x80)
    LCD.lcd_string("________________", 0xC0)


def wait_LCD(retry=False):
    LCD.lcd_string('     Retrying...' if retry else '   Recognizing..', 0x80)
    LCD.lcd_string('  Please  Wait..', 0xC0)


def animate_inout(inout):
    if inout:
        for i in range(1, 8):
            start = '{}{}'.format(('>' * i), (' ' * (7 - i)))
            end = '{}{}'.format((' ' * (7 - i)), ('<' * i))
            LCD.lcd_string('{}IN{}'.format(start, end), 0xC0)
            time.sleep(0.2)
    else:
        for i in range(1, 7):
            end = '{}{}'.format(('>' * i), (' ' * (7 - i)))
            start = '{}{}'.format((' ' * (7 - i)), ('<' * i))
            LCD.lcd_string('{}OUT{}'.format(start, end), 0xC0)
            time.sleep(0.2)
        LCD.lcd_string('<<<<<<<OUT>>>>>>', 0xC0)


def loop():
    b = False
    clear_LCD()
    count = 3
    while True:
        time.sleep(1)
        dis = distance()
        if dis < 100:
            print('Distance: {} cm'.format(int(dis)))
            if b:
                print('Detected, recognizing...')
                continue
            wait_LCD()
            data = {'operation': 200}
            response = requests.post(URL, json=data)
            if response.status_code == 201:
                b = True
                data = json.loads(response.text)
                user = str(data['user'])
                print('{}: {}'.format(user, 'IN' if data['inout'] else 'OUT'))
                LCD.lcd_string(user, 0x80)
                animate_inout(data['inout'])
            else:
                wait_LCD(retry=True)
                print('Unknown user')
        else:
            count = count - 1
            if count == 0:
                clear_LCD()
                count = 5
                b = False


def destroy():
    print("Process killed")
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

