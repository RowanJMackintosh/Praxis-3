import board
import digitalio
import time
from sensors.ultrasonic_sensor import adafruit_hcsr04

class Ultrasonic_Sensor: #ultrasonic sensor object

    def __init__(self, trigger_pin, echo_pin): #initializes object with trigger and echo pins
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin) 
        self.saved_measurements = [] #saves a set of previous measurements to help identify outliers (this is not used in the current iteration of the code)
        self.normal_distance = 0 #saves the "default" measurement for an empty bin
    
    def set_normal_distance(self):
        self.normal_distance = self.get_data() #sets the first measurement of the ultrasonic sensors as the default distance
        print(self.normal_distance)

    def get_data(self): #triggers and records ultrasonic sensor output
        dist = self.sonar.distance 
        self.saved_measurements.append(dist)
        if len(self.saved_measurements) >= 10:
            self.saved_measurements = (self.saved_measurements[1:11])
        return self.saved_measurements[-1] #returns distance
        
        
    def get_full_status(self): #outputs boolean (1 or 0) 
        self.get_data() #records measurement
        if (self.normal_distance - self.saved_measurements[-1]) > 2: #outputs that bin is full if the measurement is significantly less than the default value
            return 1
        else:
            return 0
