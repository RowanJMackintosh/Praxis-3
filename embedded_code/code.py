import board
import digitalio
import time

from sensors.ultrasonic_sensor import ultrasonic_sensor as us 
from sensors.load_cell import load_cell as lc
from sensors.gps_module.gnss_module import GNSS_Module
from wifi.wifi_trans import wifi_setup, publish

us_2 = us.Ultrasonic_Sensor(board.D12, board.D11) #initializes ultrasonic sensors
us_1 = us.Ultrasonic_Sensor(board.D10, board.D9) 

lc_1 = lc.LOAD_CELL(data_pin = digitalio.DigitalInOut(board.D5), clk_pin = digitalio.DigitalInOut(board.D4), tare = False) #initializes and tares load cell
 
gnss_1 = GNSS_Module(UARTx = 0, BAUDRATE = 9600) #initializes GPS module
    

io, wifi = wifi_setup() #initializes wifi transmission

us_1.set_normal_distance() #ultrasonic sensors are initialized with a "default distance", which is the dimensions of the bin that they are placed in
us_2.set_normal_distance()

while True:
    
   time.sleep(2)
   stat_1 = us_1.get_full_status() #boolean value indicating whether sensor 1 is blocked
   stat_2 = us_2.get_full_status() #boolean value indicating whether sensor 2 is blocked
   data_string = str(stat_1) + "," + str(stat_2) + "," + str(lc_1.get_data()) + "," + str(gnss_1.get_data()) #combined data string with ultrasonic, load cell, and gps data
   print(data_string) 
   publish(io, data_string, wifi) #publishes data to adafruit online feed