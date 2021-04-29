#####
# @brief   JT103 thermistor
#
# Module containing the JT103 thermistor class.
#
# @file     /etb/sens/JT103.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/08 $
#
# @note     Uses the ADS1115 ADC module
#
# @example  jt = JT103(0)                 # Get an instance at ADC channel 0
# @example  temp = jt.read_temperature()  # Read the current temperature [°C]
#####


##### LIBRARIES #####
# Import log function from math
from math import log
# Add path to the ETB core modules
import sys
sys.path.insert(1, '../core/')
# Import the ADS1115 module
from ETB.core.ADS1115 import *


##### GLOBAL VARIABLES #####
# 103JT thermistor (10k@25°C)
JT103_BETA              = 3435
JT103_R_ROOM            = 10000
JT103_R_BALANCE         = 10000
JT103_TEMP_K2C          = 273.15
JT103_TEMP_ROOM         = (JT103_TEMP_K2C + 25)
## value correction:
# voltage range: 0..5V
# gain range: 0--4.096V
JT103_MAX_ADC           = 32767
JT103_GAIN_MAX          = 4.096
JT103_VSS_MAX           = 5.22      # RPi gives ~5.22V instead of 5V
JT103_MAX_ADC_CORRECT   = JT103_MAX_ADC * (JT103_VSS_MAX / JT103_GAIN_MAX)


#####
# @class    JT103
# @brief    JT103 thermistor
#
# Class for the JT103 thermistor.
class JT103(object):
    ###
    # The constructor.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         ADC input channel (default: channel 0)
    # @param[in]    address         Specific I2C address (default: 0x48)
    # @param[in]    busnum          Specific I2C bus number (default: 1)
    def __init__(self, channel=0, address=0x48, busnum=1):
        # @var __i2c_address
        # Object's ADC I2C address
        self.__i2c_address = address
        # @var __bus
        # Object's ADC I2C bus number
        self.__bus = smbus.SMBus(busnum)
        # @var __channel
        # Object's ADC input channel
        self.__channel = channel
        # @var __adc
        # ADC object
        self.__adc = ADS1115(address=address, busnum=busnum)


    ###
    # Read the raw ADC value.
    #
    # @param[in]    self            The object pointer.
    # @param[out]   Raw ADC value in case of success; otherwise False.
    def _get_raw_value(self):
        return self.__adc.read_channel(channel=self.__channel)


    ###
    # Convert ADC reading to temperature in degrees Celsius (°C)
    #
    # @param[in]    self            The object pointer.
    # @param[in]    raw             Raw ADC value.
    # @param[out]   Temperature value [°C] in case of success; otherwise False.
    def raw_to_degree(self, raw):
        # Calculate the thermistor's resistance
        R_thermistor = JT103_R_BALANCE / ((JT103_MAX_ADC_CORRECT / float(raw)) - 1.0)
        # Use the beta equation to get the temperature
        T_thermistor = ((JT103_BETA * JT103_TEMP_ROOM) / (JT103_BETA + (JT103_TEMP_ROOM * log(R_thermistor/JT103_R_ROOM)))) - JT103_TEMP_K2C
        # Return the temperature (in degree Celsius)
        return float(T_thermistor)


    ###
    # Read the resulting temperature value (degree Celsius).
    #
    # @param[in]    self            The object pointer.
    # @param[out]   Temperature value [°C] in case of success; otherwise False.
    def read_temperature(self):
        # Read the raw ADC value
        data = self._get_raw_value()
        # Check if the ADC returned a valid conversion result
        if data is not False:
            # Return the temperature (in degree Celsius)
            return self.raw_to_degree(data)
        else:
            return False
