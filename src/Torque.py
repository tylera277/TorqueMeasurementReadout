
"""
Torque.py

- This module handles the implementation details of getting the readings
set to it by the CDI torque device

Classes:
	- Torque

Functions:
	- remove_letters: used for removing letters (i.e. button presses)
		from the actual torque reading numbers that are read in
	- get_torque_reading: main function thats run in its own thread for
		taking in torque readings, and dumps the readings into a queue
	


"""


import time


class Torque:
		
	# -For removing letters in the input that are entered in the terminal
	# -Controller input show up as letters, so removing it so that the
	# only thing thats stored are float numbers and if they have a sign
	# with them
	def remove_letters(self, string):	
		"""
		Input:
			- string: raw string read in from the terminal input
		"""
		return ''.join(char for char in string if char.isdigit() or char == "." or char == "-")
	
	# Reading terminal input, removing letters, placing value into queue
	def get_torque_reading(self, queue, torque_pause_event, torque_stop_event):
		"""
		Input:
			- queue: where the torque readings are sent to for the outside
				to be able to access them
			- torque_pause_event: used to pause the thread when needed
			- torque_stop_event: used to irreversibly stop the thread
		"""
		while torque_stop_event.is_set():
			
			time.sleep(0.01)
			# During execution, user will never see this.
			# Mainly used for troubleshooting purposes in development.
			raw_input = input("Please enter torque:")
			
			if torque_pause_event.is_set():
				queue.put(self.remove_letters(raw_input))
			else:
				torque_pause_event.wait()
				
