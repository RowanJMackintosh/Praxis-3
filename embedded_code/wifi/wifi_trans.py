import time
import board
import busio
from digitalio import DigitalInOut

from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
import adafruit_connection_manager
import adafruit_requests


import time
import board
import busio
from digitalio import DigitalInOut
#from sensors import ultrasonic_sensor as us1


# Define callback functions which will be called when certain events happen.
# pylint: disable=unused-argument
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    print("Connected to Adafruit IO! ")

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

# pylint: disable=unused-argument
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")

def on_USsensor_msg(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))
    # this might need to be removed
    #io.publish(data_string)


    #dist = int(message)
    #if dist > 70:
        ##io.publish("distance_alert", "Distance is greater than 70")

def wifi_setup():

# this setup stuff can be put into a function
# after wifi-setup, we should collect data from the US sesnor. If the US sensor value is over some value, then we can send to ada fruit.

# Get wifi details and more from a secrets.py file
    try:
        from wifi.secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    # Set up SPI pins
    esp32_cs = DigitalInOut(board.CS1)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)

    # Connect RP2040 to the WiFi module's ESP32 chip via SPI, then connect to WiFi
    spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

    # Connect to WiFi
    print("Connecting to WiFi...")
    wifi.connect()
    print("Connected!")

    # Initialize MQTT interface with the esp interface
    #MQTT.set_socket(socket, esp)

    pool = adafruit_connection_manager.get_radio_socketpool(esp)
    ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)

    # Initialize a new MQTT Client object
    mqtt_client = MQTT.MQTT(
        broker="io.adafruit.com",
        port=secrets["port"],
        username=secrets["aio_username"], # change to ur adafruit IO user
        password=secrets["aio_key"],
        socket_pool=pool,
        ssl_context=ssl_context, # change to ur key
    )

    # Initialize an Adafruit IO MQTT Client
    io = IO_MQTT(mqtt_client)

    # Connect the callback methods defined above to Adafruit IO
    io.on_connect = connected
    io.on_disconnect = disconnected
    io.on_subscribe = subscribe

    # Set up a callback for the led feed
    #io.add_feed_callback("ultrasonic", on_USsensor_msg)

    # Connect to Adafruit IO
    print("Connecting to Adafruit IO...")
    io.connect()

    return io, wifi

def publish(io, data_string, wifi):
    while True:
        # Poll for incoming messages
        try:
            io.publish("information", data_string)
            print("published baby")
            time.sleep(5)
            break
        except (ValueError, RuntimeError) as e:
            print("Failed to get data, retrying\n", e)
            wifi.reset() # this can possibly be removed
            io.reconnect()
        return data



''' io.loop()
            distance1 =  us_1.get_data()# depends on how US code written

            if distance1 > 70:
                print("Distance is greater than 70, sending message...")'''


