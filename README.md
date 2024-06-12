# plant_project
The main purpose of this repository is to supply the code that allows communication between an Arduino(Uno) and a Raspberry Pi.  The intent is for the user to have access to this code to deploy their own projects with their own devices.  The web application currently allows for four different devices to be routed to different arduino's.  Though the ino file supplied is only set up with one pipe address.  To add more devices, new pipe_address will be necessary to set up communcation.  As this repo develops more, more flexible fuctionality will be added to make adding more devices more seamless.


## Raspberry Pi Set Up

### Connect the NRF module to the follow GPIO pins

 |  NRF |  RasPi               |
 |:----:|:--------------------:|
 | VCC  |   3.3V               |        
 | GND  |   GND                |
 | CSN  |   GPIO8  (SPI CE0)   |      
 | CE   |   GPIO17             |
 | MOSI |   GPIO10 (SPI MOSI)  |
 | SCK  |   GPIO11 (SPI SCLK)  |
 | MISO |   GPIO9  (SPI MISO)  |

## Arudino Set Up

### NRF Module

 |  NRF |  Arduino   |
 |:----:|:----------:|
 | VCC  |   3.3V     |        
 | GND  |   GND      |
 | CSN  |   dgtl 10  |      
 | CE   |   dgtl 9   |
 | MOSI |   dgtl 11  |
 | SCK  |   dgtl 13  |
 | MISO |   dgtl 12  |

### Relay Module

Connect the NO (normally open) port of the relay module to the power of the pump.  Connect the common port to 5v of Arduino.  Connect the VCC pin of the module to 5v of Arduino.  Connect the IN of the relay module to dgtl pin 7 of the arudino.  

NOTE: An addition capacitor was added between the VCC and GND of the module to smooth out any fluctuations in power and give a better signal between modules.
