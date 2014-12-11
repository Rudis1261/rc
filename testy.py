#!/usr/bin/env python
import sys
import time
import struct
import pigpio


def testPulse(PIN, TIME=0.05, LENGHT=30, INTERVAL=1):

    print("Commencing Pulse")
    pulseRange = 255
    pi.set_PWM_range(PIN, pulseRange)
    pi.set_PWM_frequency(GPIO, 100)
    direction = "asc"

    for i in range(1, LENGHT, INTERVAL):
    	if direction == "asc":
            for x in range(1, LENGHT, INTERVAL):
                print("Running " + str(value))
                pi.set_PWM_dutycycle(PIN, value)
                time.sleep(TIME)
    	    direction = "desc"
    	else:
            for x in range(LENGHT - 1, 2, -INTERVAL):
                print("Running " + str(value))
                pi.set_PWM_dutycycle(PIN, value)
                time.sleep(TIME)
    	    direction = "asc"

    print("Pulsing complete, switching off")
    pi.write(4, 0)


def testServo(PIN, MIN=850, CENTER=1350, MAX=1750):

    print("Commencing Servo Testing")
    print("Centering Steering Servo")
    pi.set_servo_pulsewidth(PIN, CENTER)

    time.sleep(3)
    print("To the left, to the left")

    for i in range(CENTER, MIN, -20):
	    pi.set_servo_pulsewidth(PIN, i)
	    time.sleep(0.1)

    print("Sir, yes sir")
    time.sleep(3)
    print("Bring it back now")

    for i in range(MIN, CENTER, 20):
	    pi.set_servo_pulsewidth(PIN, i)
	    time.sleep(0.01)

    print("Sir, yes sir")
    time.sleep(3)
    print("To the right, to the right")

    for i in range (CENTER, MAX, 20):
	    pi.set_servo_pulsewidth(PIN, i)
	    time.sleep(0.1)

    print("Sir, yes sir")
    time.sleep(3)
    print("Centering Steering Servo")

    pi.set_servo_pulsewidth(PIN, CENTER)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(PIN, 0)
    print("Servo test complete")


# Start the actual program
GPIO  = 4
SERVO = 7
pi    = pigpio.pi()

testServo(SERVO)
time.sleep(3)
testPulse(GPIO)

print("All done")

# Clear everything up and stop using the GPIO
pi.stop()