#!/usr/bin/env python
import sys, time, struct, pigpio, thread, json
from bluetooth import *
from rc import *

global LAST_ACTIVE
LAST_ACTIVE = int(time.time())

# Start the actual program
pi        = pigpio.pi()
GPIO_PIN  = 4
SERVO_PIN = 7
MOTOR_PIN = 8
LEFT_PIN  = 11
RIGHT_PIN = 10
TAIL_PIN  = 9

# FIRE UP THE LIGHTS
lightsOn(LEFT_PIN, RIGHT_PIN, TAIL_PIN)

# BLUETOOTH SECTION
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "sinkServer",
   service_id       = uuid,
   service_classes  = [ uuid, SERIAL_PORT_CLASS ],
   profiles         = [ SERIAL_PORT_PROFILE ]
)

def janitor():
    global LAST_ACTIVE
    while 1:
	print("JANITOR: Testing, " + str(LAST_ACTIVE))
	if (LAST_ACTIVE + 3) < time.time():
	    print("JANITOR: Zeroing Controls")
	    zeroControls(MOTOR_PIN, SERVO_PIN)
	time.sleep(1)

thread.start_new_thread(janitor, ())
print("READY FOR CONNECTIONS, RFCOMM channel %d" % port)
while True:
    client_sock, client_info = server_sock.accept()
    print("INBOUND CONNECTION ", client_info)
    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            print("COMMAND RECEIVED [%s]" % data)
	    if is_json(data):
		LAST_ACTIVE = int(time.time())
                JSON = json.loads(data)

                # We need JSON to work
                if JSON['action'] == "control":

                    # Hand off command to the car
                    control(JSON['y'], JSON['x'])

    except IOError:
        pass

    print("Bye bye")
    client_sock.close()

# Close the Socket
server_sock.close()
pi.stop()
print("SELF-DESTRUCT COMPLETE")
