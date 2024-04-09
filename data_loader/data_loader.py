import time
from Adafruit_IO import Client #imports adafruit feed client
import os

client = Client("aragolaa", "aio_LfUu68p7cpa5GuH3rscznuLAFkVj") #initializes client to individual adafruit account
prev_string = client.receive("information") #receives data string from feed

clear_file = 0 #indicates how often to clear data string storage file

FILENAME = "data_loader/readings.txt" #name of data string storage file

open(FILENAME, 'w').close() #clears file of previous strings

while True:
    time.sleep(10)
    data_string = client.receive("information") #receiveds information
    
    if prev_string != data_string: #if new string is different from old data
        if os.path.exists(FILENAME):
            clear_file = (clear_file + 1)%30 #keeps count of number of strings in file
            with open(FILENAME, "a+") as file:
                file.write(data_string.value + " | " + data_string.updated_at + "\n") #writes data to text file
    prev_string = data_string
    if clear_file == 9:
        open(FILENAME, 'w').close() #clears file if it reaches a specified number of strings (in this case 10)
        
        