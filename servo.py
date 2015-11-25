#!/usr/bin/python

import RPi.GPIO as GPIO
import time

RIGHT = 0.8 
LEFT = 1.6 
CENTER = 1.2 

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(0)

def update(ms):
  duty = ((ms/1000.0)*50)*100
  pwm.ChangeDutyCycle(duty)

def ring_bell():
  update(RIGHT)
  time.sleep(2)
  update(LEFT)
  time.sleep(0.35)
  update(RIGHT)
  time.sleep(0.5)
  update(CENTER)
  time.sleep(1)

ring_bell()
pwm.stop()
GPIO.cleanup()
