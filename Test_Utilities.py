

from Utilities import Utilities

util = Utilities()

test_list_1 = ["1", '2', '3', '4', '5']
test_list_2 = ['0', '0', '0']
test_list_3 = ['1', '-1']
 

def test_rounded_average_of_list_of_strings():
											   
	assert util.rounded_average_of_list_of_strings(4, test_list_1) == 3, "average of 1,2,3,4,5 should be 3"
	assert util.rounded_average_of_list_of_strings(4, test_list_2) == 0, "average of 0 should be 0"
	assert util.rounded_average_of_list_of_strings(4, test_list_3) == 0, "average of equal pos and neg # should be 0"
	print("All average tests passed!")
	
def test_rounded_sum_of_list_of_strings():
	assert util.rounded_sum_of_list_of_strings(4, test_list_1) == 15, "sum of 1,2,3,4,5 should be 15"
	assert util.rounded_sum_of_list_of_strings(4, test_list_2) == 0, "sum of 0 should be 0"
	assert util.rounded_sum_of_list_of_strings(4, test_list_3) == 0, "sum of equal pos and neg # should be 0"
	print("All sum tests passed!")
	
test_rounded_average_of_list_of_strings()
test_rounded_sum_of_list_of_strings()
