#!/usr/bin/env python

#*** WARNING ************************************************
#*                                                          *
#* All the tests make extensive use of gpio 4 (pin P1-7).   *
#* Ensure that either nothing or just a LED is connected to *
#* gpio 4 before running any of the tests.                  *
#*                                                          *
#* Some tests are statistical in nature and so may on       *
#* occasion fail.  Repeated failures on the same test or    *
#* many failures in a group of tests indicate a problem.    *
#************************************************************

import sys
import time
import struct

import pigpio

def pulse(PIN, TIME, LENGHT):
    pulseRange = 255
    pi.set_PWM_range(PIN, pulseRange)
    pi.set_PWM_frequency(GPIO, 100)
    direction = "asc"

    for i in range(1, LENGHT):
	if direction == "asc":
	    direction = "desc"
	else: 
	    direction = "asc"

	for x in range(1, LENGHT):

	    if direction == "asc":
		 
	        value = x * (pulseRange / LENGHT)
	    else: 
	        value = (LENGHT - x) * (pulseRange / LENGHT)
	    print("Running " + str(value))
	    pi.set_PWM_dutycycle(PIN, value)
	    time.sleep(TIME)	



def test_my_servo(SERVO, MIN=850, CENTER=1350, MAX=1750):
    pi.set_servo_pulsewidth(SERVO, CENTER)
    time.sleep(3)
 
    for i in range(CENTER, MIN, -20):
	pi.set_servo_pulsewidth(SERVO, i)
	time.sleep(0.1) 

    time.sleep(3)

    for i in range(MIN, CENTER, 20):
	pi.set_servo_pulsewidth(SERVO, i)
	time.sleep(0.01)

    time.sleep(3)

    for i in range (CENTER, MAX, 20):
	pi.set_servo_pulsewidth(SERVO, i)
	time.sleep(0.1)

    time.sleep(3)

    pi.set_servo_pulsewidth(SERVO, CENTER)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(SERVO, 0)

GPIO=4
SERVO=7
pi = pigpio.pi()

print("Testing Servo")
test_my_servo(SERVO)
time.sleep(3)

print("Pulsing")
time.sleep(3)
print("Pulsing")
pulse(GPIO, 0.05, 30)
print("All done")
pi.write(4, 0)
pi.stop()

