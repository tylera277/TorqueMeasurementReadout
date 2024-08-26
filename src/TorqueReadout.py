
"""
TorqueReadout.py

- This is the central command of the program. All things called for the 
	unit come/start from here.

 Completed: 25 Aug 2024
 - Tyler Allen

"""


import threading
import queue
import time

import RPi.GPIO as GPIO


from Display import Display
from Controller import Controller
from menu import Menu
from Torque import Torque

# Initial conditions or variables I preset
GPIO.setmode(GPIO.BOARD)
base_address = "/dev/input/"
status = False
have_controller_address = False
found_controller_address = False
torque_readings = []  # List which will house all the torque readings that are entered




# Instances of the classes I will be using
display = Display(0x27)
menu = Menu(display)
torque = Torque()
controller = Controller(base_address)

display.clear_display()

# Getting the address at which the controller connects to the pi with.
# Keep rerunning till it finds something new added.
# It always shows up in the same directory, just under a different name,
# so I can cheat with giving it an address to start the search in
while not have_controller_address:
	controller_address, have_controller_address = \
		controller.find_address_of_controller(display, base_address)


# Setting the address that was found to be the controller
controller.set_device_address(controller_address)


# Telling the user that the unit can start being used now
display.clear_display()
display.update_display('Insert torque:', \
						position_horizontal = 0,
						position_vertical = 2)



# -These queues will house their respective quantities after 
# their independent threads dump the info into them during execution
# - Main idea being that I dont want to miss a value because something
# else is executing, so dump it in these, and Ill process them sequentially
# so as to not miss anything sent from or entered by the user
torque_reading_queue = queue.Queue()
controller_command_queue = queue.Queue()

# These events are how i'll communicate with the thread outside of it.
# So when it detects the controller has disconnected, it will set a 
# flag out here and thnn I can handle it. Once handled, resume thread
# execution
controller_pause_event = threading.Event()
controller_stop_event = threading.Event()
torque_pause_event = threading.Event()
torque_stop_event = threading.Event()


controller_pause_event.set()
controller_stop_event.set()
torque_pause_event.set()
torque_stop_event.set()




threads = []
controller_thread = \
	threading.Thread(target=controller.read_button_input,args=(controller_command_queue, controller_pause_event, controller_stop_event))
controller_thread.daemon = True
controller_thread.start()

torque_thread = threading.Thread(target=torque.get_torque_reading,args=(torque_reading_queue, torque_pause_event, torque_stop_event))
torque_thread.daemon = True
torque_thread.start()


try:
	while True:
		
		
		# If the controller disconnected from pi, run this
		if not controller_pause_event.is_set():
			
			# Dont take anymore torque readings while the unit is 
			# in the process of reconnecting
			torque_pause_event.clear()
			
		
			# Give instructions to the user on how to reconnect
			display.clear_display()
			display.update_display("R_bumper+start", \
								position_horizontal = 0,
								position_vertical = 1)
			display.update_display("to resume...", \
								position_horizontal = 0,
								position_vertical = 2)
								
								
								
			# Checking if it sees controller reconnect
			# Runs indefinitely till it finds something that connects
			while not found_controller_address:
				controller_address, found_controller_address = \
					controller.find_address_of_controller(display, base_address)
			
			# Reset the status flag so it can run next time controller
			# disconnects
			status = False
			try:
				controller.set_device_address(controller_address)
			except PermissionError:
				#Disregard permission error
				pass
				
				
			display.clear_display()
			display.update_display("Reconnected!", \
								position_horizontal = 0,
								position_vertical = 1)
			time.sleep(2)
			display.clear_display()
			
			# Set the events so threads can get out of the wait state and
			# start collecting data again
			controller_pause_event.set()
			torque_pause_event.set()
			
			
			# Force update the display so user can tell when its back
			# up and running
			menu.simple_average_screen(None, torque_readings, force_update=True)
			
			
		# If no new torque readings have been received,
		# you dont have to update the screen with any new numbers
		if torque_reading_queue.qsize() != 0:
			torque_readings.append(torque_reading_queue.get())
			menu.increment_current_position_index()
		
		
		# If there are no stored torque readings, then dont do anything		
		if len(torque_readings) != 0:
			
			# -If a button has been pressed AND there are stored readings,
			# then update the display and change the contents of display
			# -If no button has been pressed AND there are stored readings,
			# then just display the readings
			if controller_command_queue.qsize() != 0:
				menu.simple_average_screen(controller_command_queue.get(), torque_readings, force_update=False)	
			else:
				menu.simple_average_screen(None, torque_readings)
		
		# Needed so that not too many resources are taken up during 
		# execution
		time.sleep(0.01)
			
# If user exits:
# 	-clear the display
#	-set the stop event conditions for the threads
except KeyboardInterrupt:
	display.clear_display()
	stop_event.set()
	controller_thread.join()
	torque_thread.join()
	
