"""
Utilities.py


Classes: 
	- Utilities: A class for carrying out various mathematical operations on 
	a list of strings

s
"""


class Utilities:
	"""
	Random functions that are miscellaneous to any main functionality
	group
	
	( the class of misfit functions :) )
	"""
	def __init__(self):
		pass
		
	def rounded_average_of_list_of_strings(self, decimal_places, list_of_strings):
		total_sum = 0
		
		for value in list_of_strings:
			total_sum += float(value)
		
		try:
			average = round(total_sum / len(list_of_strings), decimal_places)
		except ZeroDivisionError:
			average = 0
		
		return average
		
		
	def rounded_sum_of_list_of_strings(self, decimal_places, list_of_strings):
		total_sum = 0
		try:
			for value in list_of_strings:
				total_sum += float(value)
		except ValueError:
			print("You entered an invalid number format!")
			
		return round(total_sum, decimal_places)
