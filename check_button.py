import RPi.GPIO as GPIO
import time
import os
import httplib
import base64
import ssl
import json
import urllib


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.02)
    input_state = GPIO.input(17)
    if input_state == False:
        print('Button Pressed')

        #Clear out the existing screen
        conn = httplib.HTTPConnection('127.0.0.1', 8080)
        headers = {'Accept''': "application/json",
                   'Content-Type': "application/json"}

        req = conn.request('POST', 'clear', headers=headers)
        res = conn.getresponse()
        print res.read()
