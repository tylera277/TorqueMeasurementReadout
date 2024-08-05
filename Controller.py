from evdev import InputDevice, categorize, ecodes

import time
import os


class Controller:
	
	""" 
	
	"""
	
	def __init__(self, device_address=None):
		self.gamepad = None#InputDevice(device_address)
		
		self.left = 18
		self.right = 33
		self.down = 32
		self.up = 46
		self.a = 34
		self.b = 36
		self.y = 23
		self.x = 35
	
	def find_address_of_controller(self, display, check_this_place):
			# Check before controller is connected to Pi
		pre_connected_devices = os.listdir(check_this_place)
		print(pre_connected_devices)

		for time_increment in range(10,0,-1):
			display.update_display(f'Connect control!', \
								position_horizontal = 0,
								position_vertical = 1)
			display.update_display(f'{time_increment} seconds left...', \
								position_horizontal = 0,
								position_vertical = 2)
			time.sleep(1)

		post_connected_devices = os.listdir(check_this_place)
		print(post_connected_devices)
		display.clear_display()

		for device in post_connected_devices:
			if device not in pre_connected_devices:
				display.update_display(f'Found it {device}', \
									position_horizontal = 0,
									position_vertical = 2)
				time.sleep(3)
				break

		#print(check_this_place + device)
		return check_this_place + device
	
	
	def set_device_address(self, address):
		self.gamepad = InputDevice(address)
		
		
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
