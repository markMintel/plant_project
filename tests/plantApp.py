import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

# This is a testing script to confirm communication between the RPi and
# Arduino using the NRF24 module.  SPI must be enabled in raspi-config.  
# The following GPIO connections are made:
#
#   NRF  |  RasPi
# -----------------------------
#   VCC  |   3.3V                       
#   GND  |   GND        
#   CSN  |   GPIO8  (SPI CE0)         
#   CE   |   GPIO17  
#   MOSI |   GPIO10 (SPI MOSI)
#   SCK  |   GPIO11 (SPI SCLK)
#   MISO |   GPIO9  (SPI MISO)  

# This script sends a message out.  Once the message is received by the Arduino
# it responds with a 'Hello World' response which will be seen in the terminal
# output.

class PlantSignal:

    def __init__(self, id, message):
        self.id = id
        self.message = message
        self.radio_active = False
        self.commands = ["TURNON", "TURNOFF", "GETREADING"]

        GPIO.setmode(GPIO.BCM)

        send_address = [0xE8, 0xE8, 0xF0, 0xF0, 0xE1]
        rec_address = [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]
        self.pipes = [send_address,rec_address]

        self.setupRadio_()


    def setupRadio_(self, CE_pin=17, payloadSize=32, channel=0x76):
        # Set up the radio.
        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio_active = True
        self.radio.begin(0, CE_pin)
        self.radio.setPayloadSize(payloadSize)
        self.radio.setChannel(channel)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_MIN)
        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()
        self.radio.openWritingPipe(self.pipes[0])
        self.radio.openReadingPipe(1, self.pipes[1])
        self.radio.printDetails()
    
    # def radioListen_(self):
    #     if self.radio_active:
    #         self.radio.startListening()
    #     else:
    #         print("The radio is inactive")
    
    def radioSend_(self, message):

        message = list(message)

        while len(message) < 32:
            message.append(0)


        if self.radio_active:
            timeout = True

            while timeout:
                timeout = False
                start = time.time()
                self.radio.write(message)
                self.radio.startListening()

                while not self.radio.available(0):
                    time.sleep(1/100)
                    if time.time() - start > 2:
                        timeout = True
                        print('Timed out.')
                        break
                    
                receivedMessage =  []
                self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
                print(f'Received: {receivedMessage}')

                string = ""
                for n in receivedMessage:
                    if (n >= 32 and n <= 126):
                        string += chr(n)
                
                self.arduinoResponse = string
                
                print("Our received message decodes to: {}".format(string))
                self.radio.stopListening()
                time.sleep(1)

    def waterPlant(self):
        print("Add plant watering instructions")

    def getReading(self):
        print("Add instructions to pull the reading data")

    
    
