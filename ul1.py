from gpiozero import DistanceSensor
from time import sleep

ultrasonic = DistanceSensor(echo=16, trigger=18)

while True:
	print(ultrasonic.distance)
	sleep(1)
