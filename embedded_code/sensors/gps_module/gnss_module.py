import time
from sensors.gps_module.L76 import l76x
import math
import adafruit_hashlib as hashlib
from sensors.gps_module.L76.micropyGPS.micropyGPS import MicropyGPS

class GNSS_Module:
    def __init__(self, UARTx, BAUDRATE): #initializes GPS module
        self.gnss_l76b = l76x.L76X(uartx=UARTx,_baudrate = BAUDRATE)
        self.gnss_l76b.l76x_exit_backup_mode()
        self.parser = MicropyGPS(location_formatting='dd') #parser object converts gps output (RMC sentences) to latitude and longitude data

        self.latitude = 0
        self.longitude = 0

    def get_data(self): #outputs latitude and longitude
        self.gnss_l76b.l76x_send_command(self.gnss_l76b.SET_SYNC_PPS_NMEA_ON)
        sentence = ''
        full_string = ''
        counter = 0

        while True:
            if self.gnss_l76b is not None:
                sentence = chr(self.gnss_l76b.uart_receive_byte()[0])
                full_string += sentence
                sentence = self.parser.update(sentence)
                if sentence:
                    return self.parser.latitude, self.parser.longitude