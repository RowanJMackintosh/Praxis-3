import time
from Adafruit_IO import Client
import os


def load_data_to_file():
    open("data_loader/readings.txt", 'w').close()
    client = Client("aragolaa", "aio_LfUu68p7cpa5GuH3rscznuLAFkVj")

    data_string = client.receive("information") 
    if os.path.exists("data_loader/readings.txt"):
        clear_file = (clear_file + 1)%30
        with open("data_loader/readings.txt", "a+") as file:
            file.write(data_string.value + " | " + data_string.updated_at + "\n")
            
        time.sleep(10)
        
        