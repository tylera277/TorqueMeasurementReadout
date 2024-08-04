

import time


class Torque:
	
	""" 
	Used on its own separate thread for reading the torque values that are 
	entered into the terminal
	"""
		
	# -For removing letters in the input that are entered in the terminal
	# -Controller input show up as letters, so removing it so that the
	# only thing thats stored are float numbers
	def remove_letters(self, string):	
		return ''.join(char for char in string if char.isdigit() or char == ".")
		
	
	# Reading terminal input, removing letters, placing value into queue
	def get_torque_reading(self, queue):
		while True:
			time.sleep(0.01)
			raw_input = input("Please enter torque:")
			queue.put(self.remove_letters(raw_input))

