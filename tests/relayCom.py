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


# Setting up GPIO value type
GPIO.setmode(GPIO.BCM)

# Set up addresses for the transeivers as an array of bytes
# First is a send address, the second is a receive address
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1],[0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

# Set up the radio.
radio = NRF24(GPIO, spidev.SpiDev())

#Begin the radio, pass in the CSN value --> CSN pin GPIO8
# Pass inn the CE value which is GPIO 17
radio.begin(0,17)

# Set the payload size to 32 bytes(maximum)
radio.setPayloadSize(32)

# Set channel, which is the channel you want to connect that Ard. receiver to
radio.setChannel(0x76)

# Set the data rate, slower=more secure
radio.setDataRate(NRF24.BR_1MBPS)

# Set the power level based on how far the devices are to one another
radio.setPALevel(NRF24.PA_MAX)

# Setting auto acknowledge
radio.setAutoAck(True)

# Setting dynamic payloads
radio.enableDynamicPayloads()

# When a message is sent out, you send back a confirmation that the message was recieved
radio.enableAckPayload()

# Open a writing pipe to allow messages to be sent to other device
radio.openWritingPipe(pipes[0])

# Open up the reading pipe, which is the second entry in the addresses
radio.openReadingPipe(1, pipes[1])

# Prints the details 
radio.printDetails()

# Listen for the message
#radio.startListening()

message = list("GETREADING")
while len(message) < 32:
    message.append(0)


# Sits and waits until a message is actually delivered
while True:
    start = time.time()
    radio.write(message)
    # print(f'Sent the message: {message}')
    radio.startListening()
    

    # Check if it has reccieved anything, if it hasn't, it goes back to sleep
    while not radio.available(0):
        time.sleep(1/100)
        if time.time() -start > 2:
            print('Timed out.')
            break
    # Breaks out of the loop when it gets something
        
    receivedMessage =  []

    # popuate variable with the message received
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print(f'Received: {receivedMessage}')

    # Data sent from radio is a byte, so they must be decoded to unicode values

    print('Translating our received message into unicode characters...')
    string = ""

    for n in receivedMessage:
        if (n >= 32 and n <= 126):
            string += chr(n)
    
    print("Our received message decodes to: {}".format(string))

    # Stops listening so it can send the next message
    radio.stopListening()
    time.sleep(1)    
                  