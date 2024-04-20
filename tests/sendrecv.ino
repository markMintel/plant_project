#include <RF24.h>
#include <RF24_config.h>
#include <nRF24L01.h>
#include <printf.h>

#include<SPI.h>

// Digital pins where the CE and CSN are hooked up
RF24 radio(9, 10);

void setup() {
  // Set up a way to check if data is being sent/recvd
  while (!Serial);
  Serial.begin(9600);

  // begin the radio, set amplification level
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);

  // set the channel, this must match the RPi channel
  radio.setChannel(0x76);

  // Open up a writing pipe
  radio.openWritingPipe(0xF0F0F0F0E1LL);

  // Open up a reading pipe
  const uint64_t pipe = 0xE8E8F0F0E1LL;
  radio.openReadingPipe(1,pipe);

  // enable dynamic payload
  radio.enableDynamicPayloads();

  //power up the radio
  radio.powerUp();

}

void loop() {
  // Listening for a message to be sent out form the raspberry pi 
  radio.startListening();
  Serial.println("Starting loop. Radio on.");
  char receivedMessage[32] = {0};
  if (radio.available()){
    radio.read(receivedMessage, sizeof(receivedMessage));
    Serial.println(receivedMessage);

    // The radio needs to stop listening if it is going to respond to the the incoming messsage
    Serial.println("Turning off the radio");
    radio.stopListening();

    String stringMessage(receivedMessage);

    if(stringMessage == "GETSTRING"){
      Serial.println("Looks like they want a string!");
      const char text[] = "Hello World!";
      radio.write(text, sizeof(text));
      Serial.println("We sent our message.");
    }
  }
  delay(100);
}
