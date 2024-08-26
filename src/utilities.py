"""
Utilities.py


Classes: 
	- Utilities

Function:
	- rounded_average_of_list_of_strings: finds the average of a list of
		numbers that are represented in strings
	- rounded_sum_of_list_of_strings: finds the sum of " "


"""


class Utilities:
	"""
	Random functions that are miscellaneous to any main functionality
	group
	
	( the class of misfit functions :) )
	"""
		
	def rounded_average_of_list_of_strings(self, decimal_places, list_of_strings):
		total_sum = 0
		
		for value in list_of_strings:
			try:
				total_sum += float(value)
			except ValueError:
				total_sum += 0
				
		try:
			average = round(total_sum / len(list_of_strings), decimal_places)
		except ZeroDivisionError:
			average = 0
		
		return average
		
		
	def rounded_sum_of_list_of_strings(self, decimal_places, list_of_strings):
		total_sum = 0
		for value in list_of_strings:
			try:
				total_sum += float(value)
			except ValueError:
				total_sum += 0
			
		return round(total_sum, decimal_places)
