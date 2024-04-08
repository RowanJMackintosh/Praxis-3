
import signal
import time

import bin
import database
import testServer
import map
import bin_data_reader

# This is set to true to use the for testing the client data that would be sent to the app
USE_DEBUG_SERVER = True   

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Saving database to json file.')
    database.Database.save()

testserver_instance = None
def initialise():
    global testserver_instance
    if USE_DEBUG_SERVER:
        testserver_instance = testServer.Test_Server()
        testserver_instance.start()


    # load in the database from the json file before we get started
    database.Database.load()

    # walk through and send the database of bins to the map app
    for bin in  database.Database.filter_by_latitude_longitude(-90, 90, -180, 180):
        time.sleep(5)
        print(f"bin{bin}")
        map.update(bin)


def main():
    # Set up the signal handler to allow us to dump the database on demand
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C at any time to save database state to json file. Program will not terminate.')

    initialise()
    
    # Main loop fetches bin updates, updates the database and send the updates to the app over the network
    while (True):
        # Do not want to spin on this too fast
        time.sleep(8)

        # fetch a bin update from the bin web thing and parse it into something we can use
        update_list = bin_data_reader.get_bin_updates()
        for update in update_list:
            # use the latitude and longitude from the update to find the bin that is the closest distance to 
            # this position and assume it is that bin. Maybe should check that the distance is not too reduculous?
            # update the database
            bin = database.Database.find_and_update_bin(update.lat, update.long, update.full, update.weight)

            if bin:
                map.update(bin)
            else:
                print(f"Could not find matching bin for latitude: {update.lat}, longitude: {update.long}. Discarding update!!")


        
if __name__ == "__main__":
    main()
