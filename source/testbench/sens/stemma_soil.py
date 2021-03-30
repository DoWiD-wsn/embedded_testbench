#!/usr/bin/env python3

########################################################################
#   STEMMA SOIL Sensor (Two Wire Interface)                            #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-14                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     stemma = STEMMA()                                                #
#     or                                                               #
#     stemma = STEMMA(0x36)     # address                              #
#     then                                                             #
#     tempC = stemma.readTemp()                                        #
#     tempC = stemma.readMoisture()                                    #
#                                                                      #
#   See also:                                                          #
#   https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test #
#   https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# I2C functionality
from board import SCL, SDA
import busio
# Import Adafruit's Seesaw library
from adafruit_seesaw.seesaw import Seesaw


##### STEMMA CLASS #####################
class STEMMA(object):
    # Constructor
    def __init__(self, address=0x36):
        self.__address = address
        self.__i2c = busio.I2C(SCL, SDA)
        self.__con = Seesaw(self.__i2c, addr=self.__address)

    # Read the temperature data (degreeC)
    def read_temp(self):
        data = None
        try:
            data = self.__con.get_temp()
        except:
            return None
        else:
            return float(data)

    # Read the moisture data (capacitance)
    def read_moisture(self):
        data = None
        try:
            data = self.__con.moisture_read()
        except:
            return None
        else:
            return int(data)
