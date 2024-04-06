import socket
import traceback

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 18080  # The port used by the server

def send_bin_update_to_map(bin_data):
    bin_data_as_bytes = str.encode(bin_data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except Exception as ex:
            print(f"Got a socket error trying to connect to the server at {HOST}/{PORT}")
            print(traceback.format_exc())

        try:
            s.sendall(bin_data_as_bytes)
        except Exception as ex:
            print(f"Got a socket error trying to send to the server at {HOST}/{PORT}")
            print(traceback.format_exc())
