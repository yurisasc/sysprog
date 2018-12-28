print("Connecting...")
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_TRIGGER = 18
GPIO_ECHO = 16

LEFT_FORWARD = 7
LEFT_BACKWARD = 8
RIGHT_FORWARD = 9
RIGHT_BACKWARD = 10
LED = 17

COLLISION_RANGE = 75

def setup():
	GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
	GPIO.setup(GPIO_ECHO, GPIO.IN)
	GPIO.setup(LEFT_FORWARD, GPIO.OUT)
	GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
	GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
	GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)

def clear():
	GPIO.output(LEFT_FORWARD, GPIO.LOW)
	GPIO.output(LEFT_BACKWARD, GPIO.LOW)
	GPIO.output(RIGHT_FORWARD, GPIO.LOW)
	GPIO.output(RIGHT_BACKWARD, GPIO.LOW)

def robot_forward():
	clear()
	GPIO.output(LEFT_FORWARD, GPIO.HIGH)
	GPIO.output(RIGHT_FORWARD, GPIO.HIGH)

def robot_backward():
	clear()
	GPIO.output(LEFT_BACKWARD, GPIO.HIGH)
	GPIO.output(RIGHT_BACKWARD, GPIO.HIGH)

def robot_left():
	clear()
	GPIO.output(LEFT_BACKWARD, GPIO.HIGH)
	GPIO.output(RIGHT_FORWARD, GPIO.HIGH)

def robot_right():
	clear()
	GPIO.output(LEFT_FORWARD, GPIO.HIGH)
	GPIO.output(RIGHT_BACKWARD, GPIO.HIGH)

def robot_stop():
	clear()

def led_on():
	GPIO.setup(LED, GPIO.OUT)
	GPIO.output(LED, GPIO.HIGH)

def led_off():
	GPIO.output(LED, GPIO.LOW)

def distance():
	GPIO.output(GPIO_TRIGGER, True)

	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()

	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	TimeElapsed = StopTime - StartTime
	distance = (TimeElapsed * 34300) / 2

	return distance

led_on()
from firebase import firebase

try:
	setup()
	print("Ready to receive input.")
	fb = firebase.FirebaseApplication('https://pirobot-70253.firebaseio.com', None)
	fb.put('/command','node','stop')
	while(True):
		dist = distance()
		command = fb.get('/command/node', None)
		if(dist < COLLISION_RANGE):
			if(command == 'stop'): robot_stop()
			else:
				print(dist)
				robot_left()
		else:
			if(command == 'stop'): robot_stop()
			elif(command == 'forward'): robot_forward()
			elif(command == 'right'): robot_right()
			elif(command == 'backward'): robot_backward()
			elif(command == 'left'): robot_left()

except KeyboardInterrupt:
	led_off()
	clear()
	GPIO.cleanup()
	quit()
