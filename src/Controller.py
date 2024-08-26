
"""
Controller.py

 -This module handles all the matters related to getting readings from 
 the controllers button presses.

Classes:
	- Controller

Functions:
	- find_address_of_controller: Used for finding the controller's
		address at various points during the programs execution
	- set_device_address: set, for that specific instance of the class,
		the Controller object with its proper address
	- close_device: used for closing the controller device object
		(not used frequently)
	- read_button_input: function which is ran on its own in a thread,
		gets button press readings and dumps them into a queue
	- get_button_name: connecting raw button number and buttons name string
	
"""






from evdev import InputDevice, categorize, ecodes

import time
import os
import threading

class Controller:

	
	def __init__(self, base_address):
		self.gamepad = None#InputDevice(device_address)
		self.base_address = base_address
		
		self.left = 18
		self.right = 33
		self.down = 32
		self.up = 46
		self.a = 34
		self.b = 36
		self.y = 23
		self.x = 35
	
	def find_address_of_controller(self, display, check_this_place):
		""" 
		Searches in an expected folder where the controller is assumed
		to have connected once the screen prompts the user
		- For R-Pi, it goes to the same folder, just logged under a 
		different event 
		"""
		
		# Check expected directory for initially connected devices
		# The pi will show up as a new even in here
		pre_connected_devices = os.listdir(check_this_place)
		
		
		# Prompt the user to connect the controller
		for time_increment in range(10,0,-1):
			display.update_display(f'R bumper+start', \
								position_horizontal = 0,
								position_vertical = 1)
								
			display.update_display(f'{time_increment} seconds left...', \
								position_horizontal = 0,
								position_vertical = 2)
			time.sleep(1)
			
		
		# After fixed time, it now rechecks the folder for a new folder
		# (the pi)
		post_connected_devices = os.listdir(check_this_place)
		display.clear_display()

		# Checks to see if it saw a new device added.
		# If so, tell the user that it has been found.
		for device in post_connected_devices:
				if device not in pre_connected_devices:
					
					display.update_display(f'Found it {device}', \
									position_horizontal = 0,
									position_vertical = 2)
					time.sleep(3)
					
					# Return location of the controller in the pi, and
					# a boolean stating something new was found
					return check_this_place + device, True
					
		# If nothing new was found, return nothing and false and this
		# code will be reran
		return None, False
		
	
	
	def set_device_address(self, address):
		""" Instantiate the InputDevice with a file address. """
		self.gamepad = InputDevice(address)
		
	def close_device(self):
		""" Close the InputDevice instance to clean it up, if needed."""
		self.gamepad.close()
		
	
	def reconnect_controller(self):
		"""
		-Used for reconnecting the controller after falling asleep.
		"""
		
		##############################################
		# Get list of connected devices at start,
		# sleep 2 seconds,
		# check again to see if anything was added.
		# If it was, thats the device we run with,
		# Else, return that nothing new was found and let the calling 
		# program rerun this code block again
		
		pre_connected_devices = os.listdir(self.base_address)
		
		time.sleep(2)						
		
		post_connected_devices = os.listdir(self.base_address)
			
		for device in post_connected_devices:
			if device not in pre_connected_devices:
				
				print(f'Found: {self.base_address + device}')
				return True
				break
		
		return False
		#################################################
			
	def read_button_input(self, button_queue, controller_pause_event, controller_stop_event):
		""" 
		Inputs:
			- button_queue: dump button presses that are read into a 
				this queue so thread can run properly
			- controller_pause_event: event thats used to communicate
				with the main control program telling when to pause
			- controller_stop_event: event thats used to indicate
				when to kill/stop the thread from running irreversibly
		"""
		
		
		# If the events are set, which means no flags/halt conditions,
		# run.
		while controller_stop_event.is_set():
		
			if controller_pause_event.is_set():
				
				try:
					time.sleep(0.01)			
					for event in self.gamepad.read_loop():
						if event.type == ecodes.EV_KEY:
							if event.value == 1:
								button_queue.put(self.get_button_name(event.code))
								
				# This is detects when the controller is disconnected.
				# Catches it and sets a flag for the main program to know				
				except OSError as oe:
					controller_pause_event.clear()
			else:
				# If controller thread was paused, wait here till its
				# re set, and thread can start running again
				controller_pause_event.wait()
		
			
			
	def get_button_name(self, code):
		""" 
		Input the event code that was read from the controller,
			see what it was set to at the beginning of the file,
			then return a string to then be utilized down the line.
		"""
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
