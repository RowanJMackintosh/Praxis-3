import time
from sensors.gps_module.L76 import l76x
import math
import adafruit_hashlib as hashlib
from sensors.gps_module.L76.micropyGPS.micropyGPS import MicropyGPS

class GNSS_Module:
    def __init__(self, UARTx, BAUDRATE):
        self.gnss_l76b = l76x.L76X(uartx=UARTx,_baudrate = BAUDRATE)
        self.gnss_l76b.l76x_exit_backup_mode()
        self.parser = MicropyGPS(location_formatting='dd')

        self.latitude = 0
        self.longitude = 0

    def get_data(self):
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


# define the UART number and its baudrate , when UARTx is 1 please solder the UART1 0R resistor on Pico-GPS-L76B board
# UARTx = 1
'''UARTx = 0

# define the rp2040 uart baudrate , the default baudrate is 9600 of L76B
BAUDRATE = 9600

# make an object of gnss device , the default uart is UART0 and its baudrate is 9600bps
gnss_l76b=l76x.L76X(uartx=UARTx,_baudrate = BAUDRATE)

# exit the backup mode when start
gnss_l76b.l76x_exit_backup_mode()

# enable/disable sync PPS when NMEA output
optional:
SET_SYNC_PPS_NMEA_ON
SET_SYNC_PPS_NMEA_OFF

gnss_l76b.l76x_send_command(gnss_l76b.SET_SYNC_PPS_NMEA_ON)


# make an object of NMEA0183 sentence parser
"""
Setup GPS Object Status Flags, Internal Data Registers, etc
local_offset (int): Timzone Difference to UTC
location_formatting (str): Style For Presenting Longitude/Latitude:
                           Decimal Degree Minute (ddm) - 40° 26.767′ N
                           Degrees Minutes Seconds (dms) - 40° 26′ 46″ N
                           Decimal Degrees (dd) - 40.446° N
"""
parser = MicropyGPS(location_formatting='dd')

sentence = ''
full_string = ''
while True:
    if gnss_l76b is not None:
        sentence = chr(gnss_l76b.uart_receive_byte()[0])
        full_string += sentence
        counter = (counter + 1)/50
        sentence = parser.update(sentence)

        if sentence:
            #print(full_string)
            full_string = ''

            print('WGS84 Coordinate:Latitude(%c),Longitude(%c) %.9f,%.9f'%(parser.latitude[1],parser.longitude[1],parser.latitude[0],parser.longitude[0]))
            print('copy WGS84 coordinates and paste it on Google map web https://www.google.com/maps')

            print('UTC Timestamp:%d:%d:%d'%(parser.timestamp[0],parser.timestamp[1],parser.timestamp[2]))

            print('Fix Status:', parser.fix_stat)

            print('Altitude:%d m'%(parser.altitude))
            print('Height Above Geoid:', parser.geoid_height)
            print('Horizontal Dilution of Precision:', parser.hdop)
            print('Satellites in Use by Receiver:', parser.satellites_in_use)
            print('')
'''
