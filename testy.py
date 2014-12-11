#!/usr/bin/env python
import sys
import time
import struct
import pigpio


def lightsOn(LEFT, RIGHT, TAIL, START=140, RANGE=255):

    print("LIGHTS ON!")

    pi.set_PWM_range(LEFT, RANGE)
    pi.set_PWM_range(RIGHT, RANGE)
    pi.set_PWM_range(TAIL, RANGE)

    pi.set_PWM_frequency(LEFT, 100)    
    pi.set_PWM_frequency(RIGHT, 100)    
    pi.set_PWM_frequency(TAIL, 100)  

    pi.set_PWM_dutycycle(LEFT, START)
    pi.set_PWM_dutycycle(RIGHT, START)
    pi.set_PWM_dutycycle(TAIL, 10)  




def flashPass(LEFT, RIGHT, COUNT=3, START=140, TIME=0.08):

    print("FLASHING")
    for i in range(0, COUNT):
        pi.set_PWM_dutycycle(LEFT, 255)
        pi.set_PWM_dutycycle(RIGHT, 255)
        time.sleep(TIME)
 	pi.set_PWM_dutycycle(LEFT, START)
 	pi.set_PWM_dutycycle(RIGHT, START)
	time.sleep(TIME)




def flashStrobe(LEFT, RIGHT, COUNT=100, START=140, TIME=0.03):
    print("STROBING")
    for i in range(0, COUNT):
	pi.set_PWM_dutycycle(LEFT, 0)
	pi.set_PWM_dutycycle(RIGHT, 255)
	time.sleep(TIME)
	pi.set_PWM_dutycycle(RIGHT, 0)
 	pi.set_PWM_dutycycle(LEFT, 255)
	time.sleep(TIME)
    pi.set_PWM_dutycycle(LEFT, START)
    pi.set_PWM_dutycycle(RIGHT, START)




def brake(TAIL, RANGE=255, START=10, INTERVAL=10, TIME=0.04):

    print("Braking")
    for i in range(START, RANGE, INTERVAL):
        pi.set_PWM_dutycycle(TAIL, i)
 	time.sleep(TIME)
    pi.set_PWM_dutycycle(TAIL, START)




def testPulse(PIN, TIME=0.04, LENGHT=10, PULSES=30, MIN=1, INTERVAL=1):

    print("Commencing Pulse")
    pulseRange = 255
    pi.set_PWM_range(PIN, pulseRange)
    pi.set_PWM_frequency(GPIO, 100)
    direction = "asc"

    for i in range(1, PULSES, INTERVAL):
    	if direction == "asc":
            for x in range(MIN, LENGHT, INTERVAL):
                print("Running " + str(x * pulseRange / LENGHT))
                pi.set_PWM_dutycycle(PIN, (x * pulseRange / LENGHT))
                time.sleep(TIME)
    	    direction = "desc"
    	else:
            for x in range(LENGHT, MIN, -INTERVAL):
                print("Running " + str(x * pulseRange / LENGHT))
                pi.set_PWM_dutycycle(PIN, x * pulseRange / LENGHT)
                time.sleep(TIME)
    	    direction = "asc"

    print("Pulsing complete, switching off")
    pi.write(4, 0)



def testMotor(PIN, MIN=1000, NEUTRAL=1500, MAX=2000):
    
    print("Commencing Motor Testing")
    time.sleep(3)
    pi.set_servo_pulsewidth(PIN, NEUTRAL)
    pi.set_servo_pulsewidth(PIN, NEUTRAL + 60)
    time.sleep(3)
    pi.set_servo_pulsewidth(PIN, NEUTRAL)
    pi.set_servo_pulsewidth(PIN, NEUTRAL - 50)
    time.sleep(3)
    pi.set_servo_pulsewidth(PIN, NEUTRAL)
    print("Motor testing complete")



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
MOTOR = 8
LEFT  = 11
RIGHT = 10
TAIL  = 9
pi    = pigpio.pi()

lightsOn(LEFT, RIGHT, TAIL)
time.sleep(1)
brake(TAIL)
time.sleep(1)
flashPass(LEFT, RIGHT)
time.sleep(1)
flashStrobe(LEFT, RIGHT)
#exit()
testServo(SERVO)
testMotor(MOTOR)
testPulse(GPIO)

print("All done")

# Clear everything up and stop using the GPIO
pi.stop()
