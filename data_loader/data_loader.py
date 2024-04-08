import time
from Adafruit_IO import Client
import os

prev_string = None
#open("data_loader/readings.txt", 'w').close() not needed - the "a+" should create the file ifdoes not exist and you need that in the loop anyway

FILENAME = "data_loader/readings.txt"

while True:
    time.sleep(10)
    
    client = Client("aragolaa", "aio_LfUu68p7cpa5GuH3rscznuLAFkVj")
    
    data_string = client.receive("information") 
    
    # Not sure what this prev_string is about
    if prev_string != data_string:
        with open(FILENAME, "a+") as file:
            file.write(data_string.value + " | " + data_string.updated_at + "\n")
    
        
        