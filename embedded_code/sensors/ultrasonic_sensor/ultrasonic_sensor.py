import board
import digitalio
import time
from sensors.ultrasonic_sensor import adafruit_hcsr04

class Ultrasonic_Sensor:

    def __init__(self, trigger_pin, echo_pin):
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin)

    def get_data(self):
        return self.sonar.distance
