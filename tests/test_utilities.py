"""
test_utilities.py

Testing the functions that are utilized in the class,
very critical checks as measurements are being directly taken 
from what they print out to the user


Functions:
	- test_rounded_average_of_list_of_strings
	- test_rounded_sum_of_list_of_strings


"""



from src.Utilities import Utilities

util = Utilities()

# Test cases that are utilized
test_list_1 = ['1', '2', '3', '4', '5']
test_list_2 = ['0', '0', '0']
test_list_3 = ['1', '-1']

def test_rounded_average_of_list_of_strings():
    """
	Testing the rounded average function thats applied to a list of strings
    """
    assert util.rounded_average_of_list_of_strings(4, test_list_1) == 3
    assert util.rounded_average_of_list_of_strings(4, test_list_2) == 0
    assert util.rounded_average_of_list_of_strings(4, test_list_3) == 0

def test_rounded_sum_of_list_of_strings():
    """
	Testing the summing function with various cases
	"""
    assert util.rounded_sum_of_list_of_strings(4, test_list_1) == 15
    assert util.rounded_sum_of_list_of_strings(4, test_list_2) == 0
    assert util.rounded_sum_of_list_of_strings(4, test_list_3) == 0
