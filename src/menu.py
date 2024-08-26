"""
menu.py

- This module handles the implementation details of outputting the torque readings
and updating the display per user controller commands

Classes:
	- Menu

Functions:
	- simple_average_screen: I put all the details for this particular screen layout 
	in one function inside the menu class in case I want to make new ones in the future.
		-- the logic is a bit messy. Not very clean or nice looking at 
		moment
	- increment_current_position_index: an int indicating how many numbers
		have been added to the reading list


"""


import math
import numpy as np
from utilities import Utilities


class Menu:
	""" 
	Houses the menu logic. So taking the torque readings and the 
	controller commands, has a bit of logic on how to fuse that all,
	then display that onto the LCD through the display object
	"""
	
	
	def __init__(self, display_object):
		self.display = display_object
		self.indicator_index = -1
		self.prev_button = "a"
		self.prev_length = 0
	
	def simple_average_screen(self, button_name, torque_reading_list, force_update=False):
		
		# Move torque value displayed up or down of list, if possible
		if button_name == "up" and self.indicator_index > 0:
			self.indicator_index -= 1
			
		if button_name == "down" and self.indicator_index != (len(torque_reading_list)-1):
			self.indicator_index += 1
		
		# Delete *one* value from the current torque reading list
		if button_name == "x":
			print(torque_reading_list)
			if len(torque_reading_list) != 0:
				print("index=", self.indicator_index, ", ", len(torque_reading_list))
				if self.indicator_index == 0 and len(torque_reading_list) != 1:
					del torque_reading_list[self.indicator_index]
					self.indicator_index = 0
				else:
					#print("pre:", torque_reading_list)
					del torque_reading_list[self.indicator_index]
					self.indicator_index -= 1
			
		
		# Delete *all* values from current torque reading list
		if button_name == "y":
			torque_reading_list.clear()
			self.indicator_index = -1
		
		
		
		
		# Compute and show the average of the readings stored so far
		if (button_name == "a" or self.prev_button == "a") and button_name != "b":
			torque_average = Utilities().rounded_average_of_list_of_strings(decimal_places=5,\
																			list_of_strings=torque_reading_list)

			if len(torque_reading_list) != self.prev_length or self.prev_button == "b":	
				self.display.clear_display_line(2)														
				self.display.update_display(string=f'Mean={torque_average}',\
										position_horizontal = 0,
										position_vertical = 2)
			self.prev_button = "a"
		
		# Display only the current sum of the readings stored so far
		if (button_name == "b" or self.prev_button == "b") and button_name != "a":
			torque_sum = Utilities().rounded_sum_of_list_of_strings(decimal_places = 5,\
																  list_of_strings=torque_reading_list)
																  
			if len(torque_reading_list) != self.prev_length or self.prev_button == "a":		
				self.display.clear_display_line(2)	
				self.display.update_display(string=f'Sum={torque_sum}',\
										position_horizontal = 0,
										position_vertical = 2)
			self.prev_button = "b"
		
		
		if len(torque_reading_list) != 0:
			try:
				if (button_name == "up" or button_name =="down") or len(torque_reading_list) != self.prev_length or force_update==True:
					self.display.clear_display_line(1)
					self.display.update_display(string=f'#{self.indicator_index+1}/{len(torque_reading_list)}: {round(float(torque_reading_list[self.indicator_index]),3)}',\
											position_horizontal = 0,
											position_vertical = 1)
			except ValueError:
				pass
				#print("You didnt enter a valid format for a number!")
			except IndexError:
				self.indicator_index = 0
				
		#elif button_name != None or len(torque_reading_list) != self.prev_length:
		else:
			self.display.clear_display_line(1)
			self.display.update_display(string=f'#{0}/{0}: {0}',\
										position_horizontal = 0,
										position_vertical = 1)
											
											
		self.prev_length = len(torque_reading_list)
		
	def increment_current_position_index(self):
		self.indicator_index += 1
			
