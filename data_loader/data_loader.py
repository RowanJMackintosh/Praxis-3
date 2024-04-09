import time
from Adafruit_IO import Client
import os

client = Client("aragolaa", "aio_LfUu68p7cpa5GuH3rscznuLAFkVj")
prev_string = client.receive("information")
clear_file = 0
open("readings.txt", 'w').close()

while True:
    time.sleep(10)
    data_string = client.receive("information") 
    
    if prev_string != data_string:
        if os.path.exists("readings.txt"):
            clear_file = (clear_file + 1)%30
            with open("readings.txt", "a+") as file:
                file.write(data_string.value + " | " + data_string.updated_at + "\n")
    prev_string = data_string
    
    if clear_file == 9:
        open("readings.txt", 'w').close()