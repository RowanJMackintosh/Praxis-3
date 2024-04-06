from network import send_bin_update_to_map


def update(bin):
    
    # create the string to send to the map app
    bin_data = f"{bin.lat} {bin.long} {bin.weight} {bin.full}"

    # Send the data to the map app
    send_bin_update_to_map(bin_data)
