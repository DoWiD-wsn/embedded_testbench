#!/usr/bin/env python3

########################################################################
#   JT103 Thermistor (via ADS1x15 ADC)                                 #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-14                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#       *) Need to check temperature calculation vs. adc value again!  #
#                                                                      #
#   Usage:                                                             #
#     thermistor = JT103()                                             #
#     or                                                               #
#     thermistor = JT103(0x48, 0)       # address & channel            #
#     or                                                               #
#     thermistor = JT103(0x48, 0, 1)    # address, channel & busnum    #
#     then                                                             #
#     tempC = thermistor.readTemp()                                    #
#                                                                      #
#   See also:                                                          #
#   https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115 #
#   http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-ADS1115/index.html #
#   https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# Import the ADS1x15 module.
import Adafruit_ADS1x15
# Import math functions
from math import log


##### JT103 CLASS ######################
class JT103(object):
    ### 103JT thermistor (10k@25°C) ###
    _JT103_BETA         = 3435
    _JT103_R_ROOM       = 10000
    _BALANCE_RESISTOR   = 10000
    _TEMP_K2C           = 273.15
    _TEMP_ROOM          = (_TEMP_K2C + 25)
    # value correction: voltage range: 0..5V - gain range: 0--4.096V
    _MAX_ADC            = 32767
    _GAIN_MAX           = 4.096
    _VSS_MAX            = 5.22        # Raspi gives ~5.22V instead of 5V
    _MAX_ADC_CORRECT    = _MAX_ADC * (_VSS_MAX / _GAIN_MAX)

    # Constructor
    def __init__(self, address=0x48, channel=0, busnum=1):
        self.__address = address
        self.__channel = channel
        self.__busnum = busnum
        self.__adc = Adafruit_ADS1x15.ADS1115(address=self.__address, busnum=self.__busnum)
        self.__adc.gain = 1

    # Read the raw sensor data
    def __read_raw(self) :
        # Open given system bus address
        data = False
        try:
            data = self.__adc.read_adc(self.__channel)
        except:
            return False
        else:
            return int(data)

    # Read the converted sensor data (degreeC)
    def read_temp(self):
        data = self.__read_raw()
        if data:
            # Calculate the thermistor's resistance
            R_thermistor = self._BALANCE_RESISTOR / ((self._MAX_ADC_CORRECT / float(data)) - 1.0)
            # Use the beta equation to get the temperature
            T_thermistor = ((self._JT103_BETA * self._TEMP_ROOM) / (self._JT103_BETA + (self._TEMP_ROOM * log(R_thermistor/self._JT103_R_ROOM)))) - self._TEMP_K2C
            # Return the temperature (in degree Celsius)
            return float(T_thermistor)
        else:
            return False
