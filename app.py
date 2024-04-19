from flask import Flask 
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

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

send_address = [0xE8, 0xE8, 0xF0, 0xF0, 0xE1]
rec_address = [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]
pipes = [send_address,rec_address]

# Set up the radio.
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,17)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()

def transmit(message):
    message = list(message)
    receivedMessage = "TEMP"
    response = {
        "receivedMessage":"SUCCESS",
        "moisture": None
    }

    while len(message) < 32:
        message.append(0)

    while 'SUCCESS' not in receivedMessage:
        start = time.time()
        radio.write(message)
        radio.startListening()
        
        while not radio.available(0):
            time.sleep(1/100)
            if time.time() -start > 2:
                print('Timed out.')
                break
            
        receivedMessage =  []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print(f'Received: {receivedMessage}')
        print('Translating our received message into unicode characters...')
        string = ""

        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)
        
        print("Our received message decodes to: {}".format(string))


        receivedMessage = string
        radio.stopListening()
        time.sleep(1)
    
    if "." in receivedMessage:
        response["moisture"] = receivedMessage.split('.')[-1][0:3]

    return response




@app.route('/water')
def water():
    message = "TURNON"
    response = transmit(message)
    return "Your plant was watered!"

@app.route('/read')
def read():
    message = "GETREADING"
    response = transmit(message)
    print(response) 
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
