
import signal
import time

import database
import testServer
import map

# This is set to true to use the for testing the client data that would be sent to the app
USE_DEBUG_SERVER = True   


def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Saving database jason to file.')
    database.Database.save()


def initialise():
    if USE_DEBUG_SERVER:
        testServer.Test_Server().start()


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
        # fetch a bin update from the bin web thing and parse it into something we can use

        ???

        # use the latitude and longitude from the update to find the bin that is the closest distance to 
        # this position and assume it is that bin. Maybe should check that the distance is not too reduculous?
        # update the database
        bin = database.Database.find_and_update_bin(latitude, longitude, full_state, weight)

        if bin:
            map.update(bin)
        else:
            print(f"Could not find matching bin for latitude: {latitude}, longitude: {longitude}. Discarding update!!")



if __name__ == "__main__":
    main()
