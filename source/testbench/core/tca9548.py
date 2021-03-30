#!/usr/bin/env python3

########################################################################
#   TCA9548A I2C Multiplexer                                           #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-14                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     multiplexer = TCA9548A()                                         #
#     or                                                               #
#     multiplexer = TCA9548A(0x70)      # address                      #
#     or                                                               #
#     multiplexer = TCA9548A(0x70,1)    # address & busnum             #
#     then                                                             #
#     multiplexer.select(1)       # Select channel 1                   #
#     multiplexer.get_channels()  # Get a list of active channels      #
#                                                                      #
#   See also:                                                          #
#   https://raspberrypi.stackexchange.com/questions/59043/how-to-read-from-multiplexer-with-python-i2c #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# I2C functionality
import smbus

##### MULTIPLEXER CLASS ################
class TCA9548A(object):
    # Constructor
    def __init__(self, address=0x70, busnum=1):
        self.__i2c_address = address
        self.__bus = smbus.SMBus(busnum)

    # Select output channel (0: deactivated; 1-8)
    def select(self, channel):
        # Check if given channel is valid
        if (channel<0) or (channel>8):
            return False
        # Get the correct bit pattern (only one channel active at a time)
        byte=0
        if channel>0:
            byte = 1<<(channel-1)
        # Try to select the given channel
        try:
            self.__bus.write_byte(self.__i2c_address, byte)
        except:
            return False
        else:
            return True

    # Read current setting
    def read(self):
        raw = 0
        try:
            raw = self.__bus.read_byte(self.__i2c_address)
        except:
            return False
        else:
            return raw
    
    # Get channel from raw reading
    def get_channels(self):
        raw = self.read()
        channels = []
        if raw:
            if raw&0b00000001:
                channels.append(1)
            if raw&0b00000010:
                channels.append(2)
            if raw&0b00000100:
                channels.append(3)
            if raw&0b00001000:
                channels.append(4)
            if raw&0b00010000:
                channels.append(5)
            if raw&0b00100000:
                channels.append(6)
            if raw&0b01000000:
                channels.append(7)
            if raw&0b10000000:
                channels.append(8)
        return channels
