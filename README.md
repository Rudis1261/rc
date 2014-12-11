#RC
Tamiya RC car control, using **PIGPIO**

###Objective

I need a software solution to be able to control my RC Car via an interface and the Raspbery Pi. I will be communicating with the PI via bluetooth, and sending as little commands as possible. The idea was to submit 2 different types of commands, the first being a service request (for lights etc), and the second being a control request (steering and throttle)

I am very bad at documenting things, so this is my effort to share my findings for the benefit of others.

###What you need to get this to work yourself

* This makes use of the awesome C Library **PIGPIO**: http://abyz.co.uk/rpi/pigpio/
* For installation, follow his **make**, **make install** instructions found here: http://abyz.co.uk/rpi/pigpio/download.html

###Initial Findings

PIGPIO uses DMA to manage the pulse width modulation, now I am no expert on the subject so I won't make out to be one. But from what I understand it is as close to hardware PWM as you will get on a Raspberry Pi.

I haven't played with it allot, but it seems very promising. Making it much easier to control pulse width modulation than with the vanilla RPi.GPIO pulse width modulation. So far I have been able to get the RC car's steering servo to behave much less sporadically than it was before with the RPi.GPIO.

I was able to also create a light pulsing action. I plan to have a couple of lighting modes.
* Pulsing break lights
* Dim break lights, which light up when breaking
* Strobing headlights, in unison as well as independently
* Strobing all round the car. In patterns, as well as randomly
