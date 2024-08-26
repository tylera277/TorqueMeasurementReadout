

"""
Display.py

 -This module handles all the matters related to displaying things on the
	mini displays that im using for this project

Classes:
	- Display

Functions:
	- update_display: broad update which lets you write anywhere on
		the lcd screen which strings, while needed to indicate the exact
		location of where you want it to be printed
	- clear_display_line: clears only a single line at a time, allowing
		for more precise control over whats displayed and updated
	- clear_display: broad clearing that gets rid of all text on both
		lines automatically
	
"""

import I2C_LCD_driver

import RPi.GPIO as GPIO


class Display:
	
	""" 
	Housing the main functionality used in printing strings to the LCD
	at certain x and y positions, specified by the user
	"""
	
	def __init__(self, address1):
		self.mylcd = I2C_LCD_driver.lcd(address1)
		
		self.x_max = 18
		self.y_max = 2
		
	def update_display(self, string, position_horizontal, position_vertical):
		self.mylcd.lcd_display_string(f'{string}', position_vertical, position_horizontal)
	
	def clear_display_line(self, line_number):
		blank_line = " " * 20
		self.mylcd.lcd_display_string(blank_line, line_number)
		
	def clear_display(self):
		self.mylcd.lcd_clear()

