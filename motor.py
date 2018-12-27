from firebase import firebase
from gpiozero import Robot
from gpiozero import LED

robby = Robot(left=(7,8), right=(9,10))
firebase = firebase.FirebaseApplication('https://pirobot-70253.firebaseio.com', None)

def main():
	led = LED(17)
	firebase.put('/command','node','stop')
	while(True):
		led.on()
		command = firebase.get('/command/node', None)
		if(command == 'stop'): robby.stop()
		elif(command == 'forward'): robby.forward()
		elif(command == 'backward'): robby.backward()
		elif(command == 'left'): robby.left()
		elif(command == 'right'): robby.right()

main()
