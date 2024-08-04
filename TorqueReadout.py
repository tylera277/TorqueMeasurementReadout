
import RPi.GPIO as GPIO

import threading
import queue
import time

from Display import Display
from Controller import Controller
from Menu import Menu
from Torque import Torque


GPIO.setmode(GPIO.BOARD)

display = Display(0x27)
controller = Controller()
menu = Menu(display)
torque = Torque()



# -These queues will house their respective quantities after 
# their independent threads dump the info into them during execution
# - Main idea being that I dont want to miss a value because something
# else is executing, so dump it in these, and Ill process them sequentially
# so as to not miss anything sent from or entered by the user

controller_command_queue = queue.Queue()
torque_reading_queue = queue.Queue()

threads = []
controller_thread = threading.Thread(target=controller.read_button_input,args=(controller_command_queue,))
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
			print("torque readings:", torque_readings)
			
		if len(torque_readings) != 0:
			if controller_command_queue.qsize() != 0:
				menu.simple_average_screen(controller_command_queue.get(), torque_readings)	
			else:
				menu.simple_average_screen(None, torque_readings)
		
		time.sleep(0.5)
		
		
except KeyboardInterrupt:
	display.clear_display()
	print("User-executed termination! :(")

	
