from evdev import InputDevice, categorize, ecodes

import time
import os


class Controller:
	
	""" 
	
	"""
	
	def __init__(self, device_address=None):
		self.gamepad = None#InputDevice(device_address)
		
		self.base_address = None
		
		self.left = 18
		self.right = 33
		self.down = 32
		self.up = 46
		self.a = 34
		self.b = 36
		self.y = 23
		self.x = 35
	
	def find_address_of_controller(self, display, check_this_place):
		self.base_address = check_this_place
		
		
			# Check before controller is connected to Pi
		pre_connected_devices = os.listdir(check_this_place)
		print(pre_connected_devices)

		for time_increment in range(20,0,-1):
			display.update_display(f'R bumper+start', \
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
		print(check_this_place+device)
		return check_this_place + device, True
	
	
	def set_device_address(self, address):
		self.gamepad = InputDevice(address)
		
	def reconnect_controller(self, controller_instance):
		"""
		-Used for reconnecting the controller after falling asleep.
		-Want the main program to continue running and be able to recover
		from it (i.e. user can reconnect and easily resume use)
		"""
		
		pre_connected_devices = os.listdir(self.base_address)
		
		while True:
			post_connected_devices = os.listdir(self.base_address)
			
			for device in post_connected_devices:
				if device not in pre_connected_devices:
					controller_instance.set_device_address(self.base_address + device)
					break
			time.sleep(0.1)
			
			
	def read_button_input(self, queue, controller_instance):
		""" 
		- Used for reading the controller button input
		- Meant to run on its own thread and dumping readings into a queue
		"""
		try:
			while True:
				time.sleep(0.01)			
				for event in self.gamepad.read_loop():
					if event.type == ecodes.EV_KEY:
						if event.value == 1:
							queue.put(self.get_button_name(event.code))
		except OSError:
			self.reconnect_controller(controller_instance)
			
			
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
