from evdev import InputDevice, categorize, ecodes

import time


class Controller:
	
	""" 
	
	"""
	
	def __init__(self):
		self.gamepad = InputDevice("/dev/input/event4")
		
		self.left = 18
		self.right = 33
		self.down = 32
		self.up = 46
		self.a = 34
		self.b = 36
		self.y = 23
		self.x = 35
		
	def read_button_input(self, queue):
		
		while True:
			time.sleep(0.01)			
			for event in self.gamepad.read_loop():
				if event.type == ecodes.EV_KEY:
					if event.value == 1:
						queue.put(self.get_button_name(event.code))
					
	def get_button_name(self, code):
		if code == self.left:
			return 'left'
		if code == self.right:
			return 'right'
		if code == self.up:
			return 'up'
		if code == self.down:
			return 'down'
		if code == self.a:
			return 'a'
		if code == self.b:
			return 'b'
		if code == self.y:
			return 'y'
		if code == self.x:
			return 'x'
