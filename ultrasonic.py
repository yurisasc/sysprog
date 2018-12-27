from gpiozero import Robot
import RPi.GPIO as GPIO
import time

GPIO_TRIGGER = 18
GPIO_ECHO = 16

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

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
	weight = 0.3
	new_distance = (distance * weight) + (distance * (1-weight))

	return new_distance

if __name__ == '__main__':
	try:
		while True:
			dist = distance()
			print("Measured Distance = %.1f cm" % dist)
			time.sleep(1)
			robot.forward()
	except KeyboardInterrupt:
		print("Measurement Stopped by User")
		GPIO.cleanup()
