print("Connecting...")
from gpiozero import Robot
from gpiozero import LED
from firebase import firebase
import RPi.GPIO as GPIO
import time

firebase = firebase.FirebaseApplication('https://pirobot-70253.firebaseio.com', None)
robby = Robot(left=(7,8), right=(9,10))

GPIO_TRIGGER = 18
GPIO_ECHO = 16

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

COLLISION_RANGE = 75

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

def main():
	led = LED(17)
	print("Ready to receive input.")
	firebase.put('/command','node','stop')
	while(True):
		dist = distance()
		led.on()
		command = firebase.get('/command/node', None)
		if(dist < COLLISION_RANGE):
			if(command == 'stop'): robby.stop()
			else:
				print(dist)
				robby.left()
		else:
			if(command == 'stop'): robby.stop()
			elif(command == 'forward'): robby.forward()
			elif(command == 'right'): robby.right()
			elif(command == 'backward'): robby.backward()
			elif(command == 'left'): robby.left()

try:
	main()
except KeyboardInterrupt:
	GPIO.cleanup()
