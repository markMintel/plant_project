# plant_project

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
