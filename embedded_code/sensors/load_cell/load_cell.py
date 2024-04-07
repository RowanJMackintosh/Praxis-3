import board
import time
from sensors.load_cell.hx711 import hx711_gpio as hx711

class LOAD_CELL:
    def __init__(self, data_pin, clk_pin, tare):
        self.hx = hx711.HX711_GPIO(data_pin, clk_pin, tare=tare)
        self.scale = 1

    def calibrate(self, known_weight):

        print("Place known weight on scale...")
        time.sleep(10)
        for i in range(0, 20):
            reading = self.hx.read(100)
            print(reading)
        print("Reading obtained")
        self.scale = reading/known_weight


    def get_data(self):
        reading = self.hx.read(10)
        return reading/self.scale


