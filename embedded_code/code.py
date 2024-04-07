import board
import digitalio
import time

from sensors.ultrasonic_sensor import ultrasonic_sensor as us
from sensors.load_cell import load_cell as lc
from sensors.gps_module.gnss_module import GNSS_Module
from wifi.wifi_trans import wifi_setup, publish

us_1 = us.Ultrasonic_Sensor(board.D12, board.D11)
us_2 = us.Ultrasonic_Sensor(board.D10, board.D9)

#lc_1 = lc.LOAD_CELL(data_pin = digitalio.DigitalInOut(board.D5), clk_pin = digitalio.DigitalInOut(board.D4), tare = True)

gnss_1 = GNSS_Module(UARTx = 0, BAUDRATE = 9600)


io, wifi = wifi_setup()
while True:

   time.sleep(2)
   data_string = str(us_1.get_data()) + "," + str(us_2.get_data()) + "," + str(gnss_1.get_data())
   #data_string = str(gnss_1.get_data())
   print(data_string)
   publish(io, data_string, wifi)
