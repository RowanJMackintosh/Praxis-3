import time
from Adafruit_IO import Client
import os


def load_data_to_file(filename):
    open(filename, 'w').close()
    client = Client("aragolaa", "aio_LfUu68p7cpa5GuH3rscznuLAFkVj")

    data_string = client.receive("information") 
    if os.path.exists(filename):
        clear_file = (clear_file + 1)%30
        with open(filename, "a+") as file:
            file.write(data_string.value + " | " + data_string.updated_at + "\n")
            
        time.sleep(10)
        
        