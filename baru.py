import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LEFT_FORWARD = 7
LEFT_BACKWARD = 8
RIGHT_FORWARD = 9
RIGHT_BACKWARD = 10
LED = 17

def setup():
	GPIO.setup(LEFT_FORWARD, GPIO.OUT)
	GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
	GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
	GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
	GPIO.setup(LED, GPIO.OUT)

def clear():
	GPIO.output(LEFT_FORWARD, GPIO.LOW)
	GPIO.output(LEFT_BACKWARD, GPIO.LOW)
	GPIO.output(RIGHT_FORWARD, GPIO.LOW)
	GPIO.output(RIGHT_BACKWARD, GPIO.LOW)

def robot_forward():
	clear()
	GPIO.output(LEFT_FORWARD, GPIO.HIGH)
	GPIO.output(RIGHT_FORWARD, GPIO.HIGH)

def led_on():
	GPIO.output(LED, GPIO.HIGH)

def led_off():
	GPIO.output(LED, GPIO.LOW)

setup()
led_on()
while(True):
	try:
		robot_forward()
	except KeyboardInterrupt:
		led_off()
		clear()
		GPIO.cleanup()
		quit()
