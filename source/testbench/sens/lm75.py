#!/usr/bin/env python3

########################################################################
#   LM75 Temperature Sensor                                            #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-12-12                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     lm = LM75()                                                      #
#     or                                                               #
#     lm = LM75(0x48)               # address                          #
#     or                                                               #
#     lm = LM75(0x48,1)             # address & busnum                 #
#     then                                                             #
#     lm.get_temperature()          # get the temperature reading      #
#     lm.get_config()               # get configuration register       #
#     lm.get_hyst()                 # get hysteresis [°C]              #
#     lm.get_os()                   # get overtemperature shutdown [°C]#
#     lm.set_config(0x00)           # set configuration register       #
#     lm.set_hyst(75.0)             # set hysteresis [°C]              #
#     lm.set_os(80.0)               # set overtemperature shutdown [°C]#
#                                                                      #
########################################################################


##### LIBRARIES ########################
# I2C functionality
import smbus


##### Register Values ##################
### REGISTER ADDRESSES ###
LM75_REG_TEMP           = 0x00
LM75_REG_CONF           = 0x01
LM75_REG_HYST           = 0x02
LM75_REG_OS             = 0x03
### CONFIGURATION ###
# shutdown #
LM75_CONF_SHUTDOWN      = 0
# comparator/interrupt
LM75_CONF_COMP          = 1
# OS polarity
LM75_CONF_POL           = 2
# fault queue
LM75_CONF_QUEUE         = 3
LM75_CONF_QUEUE_MASK    = 0x18
LM75_CONF_QUEUE_1       = 0
LM75_CONF_QUEUE_2       = 1
LM75_CONF_QUEUE_4       = 2
LM75_CONF_QUEUE_6       = 3


##### LM75 CLASS ###################
class LM75(object):
    # Constructor
    def __init__(self, address=0x48, busnum=1):
        self.__i2c_address = address
        self.__bus = smbus.SMBus(busnum)

    ##### I2C READ/WRITE #####

    # Read register value (byte)
    def read_register_byte(self, register):
        # Try to read the given register
        try:
            return self.__bus.read_byte_data(self.__i2c_address, register)
        except:
            return False

    # Read register value (word)
    def read_register_word(self, register):
        # Try to read the given register
        try:
            return self.__bus.read_word_data(self.__i2c_address, register)
        except:
            return False

    # Write a register value (byte)
    def write_register_byte(self, register, value):
        # Try to write the given register
        try:
            self.__bus.write_byte_data(self.__i2c_address, register, value)
            return True
        except:
            return False

    # Write a register value (word)
    def write_register_word(self, register, value):
        # Try to write the given register
        try:
            self.__bus.write_word_data(self.__i2c_address, register, value)
            return True
        except:
            return False


    ##### READ REGISTERS #####

    # Read the configuration register
    def get_config(self):
        # Read the config register
        ret = self.read_register_byte(LM75_REG_CONF)
        if not ret:
            return False
        # Return the values
        return ret

    # Read the configuration register flags extracted
    def get_config_flags(self):
        # Read the config register
        ret = self.get_config()
        if not ret:
            return False
        # Extract the single flags
        SHUTDOWN = 1 if (ret & (1 << LM75_CONF_SHUTDOWN)) else 0
        COMP     = 1 if (ret & (1 << LM75_CONF_COMP)) else 0
        POL      = 1 if (ret & (1 << LM75_CONF_POL)) else 0
        QUEUE    = (ret & LM75_CONF_QUEUE_MASK) >> LM75_CONF_QUEUE
        # Return the flag values
        return (SHUTDOWN,COMP,POL,QUEUE)

    # Get a temperature value from a given register
    def get_temp_value(self, reg):
        # Read the temperature register
        raw = self.read_register_word(reg) & 0xFFFF
        # Swap bytes
        raw = ((raw << 8) & 0xFF00) + (raw >> 8)
        # Check if number is negative
        if raw > 32767:
            raw -= 65536
        # Convert word to float
        return (raw / 32.0) / 8.0

    # Read the current temperature
    def get_temperature(self):
        # Read the temperature register
        return self.get_temp_value(LM75_REG_TEMP)

    # Read the hysteresis temperature
    def get_hyst(self):
        # Read the hysteresis register
        return self.get_temp_value(LM75_REG_HYST)

    # Read the overtemperature shutdown temperature
    def get_os(self):
        # Read the overtemperature shutdown register
        return self.get_temp_value(LM75_REG_OS)


    ##### WRITE REGISTERS #####

    # Set the configuration register
    def set_config(self,value):
        # Write the byte to the register
        ret = self.write_register_byte(LM75_REG_CONF, value)
        # Check return status
        if not ret:
            return False
        else:
            return True

    # Set the configuration register flags
    def set_config_flags(self,SHUTDOWN,COMP,POL,QUEUE):
        # Get the resulting configuration
        config = 0x00
        if SHUTDOWN==1:
            config = config | (1 << LM75_CONF_SHUTDOWN)
        if COMP==1:
            config = config | (1 << LM75_CONF_COMP)
        if POL==1:
            config = config | (1 << LM75_CONF_POL)
        if (QUEUE>=0) and (QUEUE<=3):
            config = config | (QUEUE << LM75_CONF_QUEUE)
        # Write the byte to the register
        ret = self.set_config(config)
        # Check return status
        if not ret:
            return False
        else:
            return True

    # Set the a temperature value to a given register
    def set_temp_value(self, temp, reg):
        # Convert float to word
        #word = self.float2reg(temp)
        word = 0                            # TODO: not working yet
        # Swap bytes
        word = ((word&0x00FF)<<8) | ((word&0xFF00)>>8)
        # Write the given value to the register
        ret = self.write_register_word(reg, word)
        # Check return status
        if not ret:
            return False
        else:
            return True

    # Set the hysteresis temperature
    def set_hyst(self,temp):
        # Write the word to the register
        return self.set_temp_value(temp, LM75_REG_HYST)

    # Set the overtemperature shutdown temperature
    def set_os(self,temp):
        # Write the word to the register
        return self.set_temp_value(temp, LM75_REG_OS)
