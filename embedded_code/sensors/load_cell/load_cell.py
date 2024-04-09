import board
import time
from sensors.load_cell.hx711 import hx711_gpio as hx711 #imports load cell object

class LOAD_CELL:
    def __init__(self, data_pin, clk_pin, tare): 
        self.hx = hx711.HX711_GPIO(data_pin, clk_pin, tare=tare) #initalizes load cell object
        self.scale = 1 #scale calibrates the load cell output to the desired units

    def calibrate(self, known_weight): #calibration code

        print("Place known weight on scale...") #uses known weight to set scale value
        time.sleep(10)
        for i in range(0, 20):
            reading = self.hx.read(100)
            print(reading)
        print("Reading obtained")
        self.scale = reading/known_weight


    def get_data(self): #outputs weight data
        reading = self.hx.read(10)
        return reading/self.scale 


