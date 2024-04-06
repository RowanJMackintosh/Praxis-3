import network
import threading
import socket

class Test_Server:
    '''
    This test server is just to test the client side before trying to connect to the app.
    It just listens for client connections and prints whatever it got from the client.
    '''

    def __init__(self):
        self.port = network.PORT
        self.host = "127.0.0.1"


    def start(self):
        threading.Thread(target=self.test_server).start()


    def test_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket :
            serverSocket.bind((self.host, self.port)) # Setup the socket 
            
            print(f"Test_server: listening for client connection at: {self.host}/{self.port}")
            serverSocket.listen()                   # listen for incomming client connections

            while True:
                clientConnection, clientAddress = serverSocket.accept()

                with clientConnection:
                    while True:
                        # receive the data sent from the client. At most 1024 bytes will be read. That should be enough for a bin update.
                        data = clientConnection.recv(1024)

                        # If there is no "data" the client closed the connection
                        if not data:
                            break
                        data_str = data.decode()

                        print(f"Test Server message data: {data}")
