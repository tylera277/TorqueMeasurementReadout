
import RPi.GPIO as GPIO

import threading
import queue
import time

#time.sleep(20)

from Display import Display
from Controller import Controller
from Menu import Menu
from Torque import Torque

GPIO.setmode(GPIO.BOARD)

display = Display(0x27)
menu = Menu(display)
torque = Torque()
controller = Controller()


display.clear_display()
# Getting the address at which the controller connects to the pi at
controller_address, have_controller_address = controller.find_address_of_controller(display, "/dev/input/")

#controller_address = "/dev/input/event2"
# Setting the found address to the controller
controller.set_device_address(controller_address)

# Telling the user that the unit can start being used now
display.clear_display()
display.update_display(f'Insert torque:', \
						position_horizontal = 0,
						position_vertical = 2)



# -These queues will house their respective quantities after 
# their independent threads dump the info into them during execution
# - Main idea being that I dont want to miss a value because something
# else is executing, so dump it in these, and Ill process them sequentially
# so as to not miss anything sent from or entered by the user

controller_command_queue = queue.Queue()
torque_reading_queue = queue.Queue()

threads = []
controller_thread = threading.Thread(target=controller.read_button_input,args=(controller_command_queue, controller))
controller_thread.daemon = True
controller_thread.start()

torque_thread = threading.Thread(target=torque.get_torque_reading,args=(torque_reading_queue,))
torque_thread.daemon = True
torque_thread.start()


# List which will house all the torque readings that are entered
torque_readings = []


try:
	while True:
		if torque_reading_queue.qsize() != 0:
			torque_readings.append(torque_reading_queue.get())
			menu.increment_current_position_index()
				
		if len(torque_readings) != 0:
			if controller_command_queue.qsize() != 0:
				menu.simple_average_screen(controller_command_queue.get(), torque_readings)	
			else:
				menu.simple_average_screen(None, torque_readings)
			
		time.sleep(0.01)
			
		
except KeyboardInterrupt:
	display.clear_display()
	print("User-executed termination! :(")

	
