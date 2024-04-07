import time
from Adafruit_IO import Client
import os

prev_string = None
clear_file = 0
open("data_loader/readings.txt", 'w').close()

while True:
    time.sleep(10)
    
    client = Client("aragolaa", "aio_LfUu68p7cpa5GuH3rscznuLAFkVj")
    
    data_string = client.receive("information") 
    
    if prev_string != data_string:
        if os.path.exists("data_loader/readings.txt"):
            clear_file = (clear_file + 1)%30
            file = open("data_loader/readings.txt", "a")
            file.write(data_string.value + " | " + data_string.updated_at + "\n")
            file.close()
    
    if clear_file == 29:
        open("data_loader/readings.txt", 'w').close()