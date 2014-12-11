#!/usr/bin/env python
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



def testServo(SERVO, MIN=850, CENTER=1350, MAX=1750):
    print("Centerig Steering Servo")
    pi.set_servo_pulsewidth(SERVO, CENTER)

    time.sleep(3)
    print("To the left, to the left")

    for i in range(CENTER, MIN, -20):
	    pi.set_servo_pulsewidth(SERVO, i)
	    time.sleep(0.1)

    print("Hoorah")
    time.sleep(3)
    print("Bring it back now")

    for i in range(MIN, CENTER, 20):
	    pi.set_servo_pulsewidth(SERVO, i)
	    time.sleep(0.01)

    print("Hoorah")
    time.sleep(3)
    print("Centerig Steering Servo")

    for i in range (CENTER, MAX, 20):
	    pi.set_servo_pulsewidth(SERVO, i)
	    time.sleep(0.1)

    print("Hoorah")
    time.sleep(3)
    print("Centerig Steering Servo")

    pi.set_servo_pulsewidth(SERVO, CENTER)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(SERVO, 0)
    print("Servo test complete")


# Start the actual program
GPIO  = 4
SERVO = 7
pi    = pigpio.pi()

print("Testing Servo")
testServo(SERVO)
time.sleep(3)

print("Pulsing")
pulse(GPIO, 0.05, 30)
print("All done")

pi.write(4, 0)

# Clear everything up and stop using the GPIO
pi.stop()