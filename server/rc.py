#!/usr/bin/env python
import sys, time, struct, pigpio, thread, json

pi = pigpio.pi()
global BRAKING, FLASHING, LEFT_PIN, RIGHT_PIN
GPIO_PIN = 4
SERVO_PIN = 7
MOTOR_PIN = 8
LEFT_PIN = 11
RIGHT_PIN = 10
TAIL_PIN = 9
BREAKING = False
FLASHING = False

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True



def lightsOn(LEFT, RIGHT, TAIL, START=140, RANGE=255):

    #print("LIGHTS ON!")
    pi.set_PWM_range(LEFT, RANGE)
    pi.set_PWM_range(RIGHT, RANGE)
    pi.set_PWM_range(TAIL, RANGE)

    pi.set_PWM_frequency(LEFT, 100)
    pi.set_PWM_frequency(RIGHT, 100)
    pi.set_PWM_frequency(TAIL, 100)

    pi.set_PWM_dutycycle(LEFT, START)
    pi.set_PWM_dutycycle(RIGHT, START)
    pi.set_PWM_dutycycle(TAIL, 10)
    return True;



def lightsFlash(LEFT, RIGHT, COUNT=3, START=140, TIME=0.02):

    global FLASHING
    if FLASHING: 
        for i in range(0, COUNT):
            pi.set_PWM_dutycycle(LEFT, 255)
            pi.set_PWM_dutycycle(RIGHT, 255)
            time.sleep(TIME)
 	    pi.set_PWM_dutycycle(LEFT, START)
 	    pi.set_PWM_dutycycle(RIGHT, START)
	    time.sleep(TIME)
    return True;



def lightsStrobe(LEFT, RIGHT, COUNT=100, START=140, TIME=0.03):
    for i in range(0, COUNT):
	pi.set_PWM_dutycycle(LEFT, 0)
	pi.set_PWM_dutycycle(RIGHT, 255)
	time.sleep(TIME)
	pi.set_PWM_dutycycle(RIGHT, 0)
 	pi.set_PWM_dutycycle(LEFT, 255)
	time.sleep(TIME)
    pi.set_PWM_dutycycle(LEFT, START)
    pi.set_PWM_dutycycle(RIGHT, START)
    return True;



def control(ENGINE=0.0, STEERING=0.0, E_PIN=MOTOR_PIN, S_PIN=SERVO_PIN):
    engine(ENGINE, E_PIN)
    steer(STEERING, S_PIN)



def engine(SPEED=0.0, PIN=MOTOR_PIN, MIN=1000, NEUTRAL=1500, MAX=2000):
    SPEED = float(SPEED)
    global BREAKING, FLASHING, LEFT_PIN, RIGHT_PIN
    if float(SPEED) == 0.0:
        BREAKING = False
        pi.set_servo_pulsewidth(PIN, NEUTRAL)
    
    elif float(SPEED) > 0:
	BREAKING = False
	VALUE = MAX - NEUTRAL
	VALUE_AFTER = MAX - VALUE + (VALUE * (SPEED / 100))
	#print(VALUE)
	#print(VALUE_AFTER)
        pi.set_servo_pulsewidth(PIN, VALUE_AFTER)
	if int(SPEED) > 90 and FLASHING == False:
            FLASHING = True
	    thread.start_new_thread(lightsFlash, (LEFT_PIN, RIGHT_PIN))
	else:
	    FLASHING = False	

    else:
        if BREAKING == False:
	    BREAKING = True
            thread.start_new_thread(brake, (9, 255))

	VALUE = NEUTRAL - MIN
        VALUE_AFTER = MIN + VALUE + (VALUE * (SPEED / 100))
        #print(VALUE)
        #print(VALUE_AFTER)
        pi.set_servo_pulsewidth(PIN, VALUE_AFTER)




def steer(SPEED=0.0, PIN=SERVO_PIN, MIN=850, CENTER=1350, MAX=1750):
    SPEED = float(SPEED)
    if float(SPEED) == 0.0:
        pi.set_servo_pulsewidth(PIN, CENTER)
    elif float(SPEED) > 0:
        VALUE = MAX - CENTER
        VALUE_AFTER = MAX - VALUE + (VALUE * (SPEED / 100))
        pi.set_servo_pulsewidth(PIN, int(VALUE_AFTER))
    else:
	VALUE = CENTER - MIN
	VALUE_AFTER = MIN + VALUE + (VALUE * (SPEED / 100))
        pi.set_servo_pulsewidth(PIN, int(VALUE_AFTER))




def brake(TAIL, RANGE=255, START=10, INTERVAL=10, TIME=0.04):
    #print("Braking")
    global BREAKING
    for i in range(START, RANGE, INTERVAL):
        pi.set_PWM_dutycycle(TAIL, i)
 	time.sleep(TIME)
    while BREAKING:
	pi.set_PWM_dutycycle(TAIL, 255)
    pi.set_PWM_dutycycle(TAIL, START)
    return True;



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
