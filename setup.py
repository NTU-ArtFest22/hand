#!/usr/bin/env python

import RPi.GPIO as GPIO
import PhotoProcess
import time

btnPin = 18
poseLedPin = 23

def init():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(poseLedPin, GPIO.OUT)
    GPIO.output(poseLedPin, GPIO.LOW)

    GPIO.add_event_detect(btnPin, GPIO.RISING, callback=takePic, bouncetime=350)

# after 3 sec(blink 3 times) take a photo
def takePic(channel):
    blink(poseLedPin, 3)
    # continuous shooting: gphoto2 -I 1 -F 4 --capture-image-and-download --no-keep

    filename = PhotoProcess.takePic()
    PhotoProcess.uploadPic(filename)


def blink(pin, number):
    for i in range(number):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(1)

def main():
    init()
    while True:
        pass

if __name__ == '__main__':
    main()
