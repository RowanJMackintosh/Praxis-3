#This file is to receive the data from sensors and use to determine if bin is full
import bin
import map
import database

max_weight = 90 #place actual max weight here

def full_status(weight):
    if weight >= 0.7*max_weight:
        return True
    return False


file = open("filename", "r") #fill in the name of the file
#do i need to move this file within the loop cause it must be constantly changing?
while True:
    temp = []

    # Get next line from file
    line = file.readline()
    temp = line.split(',')
    US1 = temp[0]
    US2 = temp[1]
    load = temp[2]
    lat = temp[3]
    long = temp[4]
    database.cls.find_and_update_bin(database.cls, lat, long, full_status(load), load) #do i need to make my own find and replace function
    map.update()
    
 
    # if line is empty
    # end of file is reached
    if not line:
        break
 
file.close()



