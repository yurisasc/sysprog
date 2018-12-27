from gpiozero import Robot
from gpiozero import LED


led = LED(17)
while True:
	led.on()
