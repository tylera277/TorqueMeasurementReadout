
import math

import numpy as np

from Utilities import Utilities


class Menu:
	""" 
	Houses the menu logic. So taking the torque readings and the 
	controller commands, has a bit of logic on how to fuse that all,
	then display that onto the LCD through the display object
	"""
	
	
	def __init__(self, display_object):
		self.display = display_object
		self.indicator_index = -1
		self.prev_button = None
	
	def simple_average_screen(self, button_name, torque_reading_list):
		
		self.display.clear_display()
										
										
				
		# Move torque value displayed up or down of list, if possible
		if button_name == "up" and self.indicator_index != 0:
			self.indicator_index -= 1
			
		elif button_name == "down" and self.indicator_index != (len(torque_reading_list)-1):
			self.indicator_index += 1
		
		# Delete *one* value from the current torque reading list
		elif button_name == "x":
			if len(torque_reading_list) != 0:
				del torque_reading_list[self.indicator_index]
				self.indicator_index -= 1
			
		
		# Delete *all* values from current torque reading list
		elif button_name == "y":
			torque_reading_list.clear()
			self.indicator_index = -1
		
		# Compute and show the average of the readings stored so far
		elif (button_name == "a" or self.prev_button == "a") and button_name != "b":
			torque_average = Utilities().rounded_average_of_list_of_strings(decimal_places=4,\
																			list_of_strings=torque_reading_list)
										
			
			self.display.update_display(string=f'Average={torque_average}',\
										position_horizontal = 0,
										position_vertical = 2)
			self.prev_button = "a"
		
		# Display only the current sum of the readings stored so far
		elif (button_name == "b" or self.prev_button == "b") and button_name != "a":
			torque_sum = Utilities().rounded_sum_of_list_of_strings(decimal_places = 4,\
																  list_of_strings=torque_reading_list)
			self.display.update_display(string=f'Sum={torque_sum}',\
										position_horizontal = 0,
										position_vertical = 2)
			self.prev_button = "b"
		
		
		
		if len(torque_reading_list) != 0:
			try:
				self.display.update_display(string=f'#{self.indicator_index+1}/{len(torque_reading_list)}: {round(float(torque_reading_list[self.indicator_index]),3)}',\
											position_horizontal = 0,
											position_vertical = 1)
			except ValueError:
				print("You didnt enter a valid format for a number!")
				
		else:
			self.display.update_display(string=f'#{0}/{0}: {0}',\
										position_horizontal = 0,
										position_vertical = 1)
											
											
		
		
	def increment_current_position_index(self):
		self.indicator_index += 1
			
