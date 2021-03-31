#####
# @package tca9548
# @brief   tca9548 I2C multiplexer
#
# Package containing the tca9548 multiplexer class used on the ETB.
#
# @file     /etb/core/tca9548.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/03/31 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @see      https://raspberrypi.stackexchange.com/questions/59043/how-to-read-from-multiplexer-with-python-i2c
#
# @example  multiplexer = tca9548()       # Get an instance with default I2C address
# @example  multiplexer = tca9548(0x70)   # Get an instance with specific I2C address and default bus
# @example  multiplexer = tca9548(0x70,1) # Get an instance with specific I2C address and specific number
#
# @example  multiplexer.select(1)         # Select channel 1 (SD0/SC0)
# @example  multiplexer.get_channels()    # Get a list of currently active channels
#####


##### LIBRARIES #####
# smbus (subclass of I2C functionality)
import smbus


#####
# @class    tca9548
# @brief    tca9548 I2C multiplexer
#
# Class for the tca9548 multiplexer used on the ETB.
class TCA9548A(object):
    ###
    # The constructor.
    #
    # @param[in] self The object pointer.
    # @param[in] address specific I2C address (default: 0x70)
    # @param[in] busnum specific I2C bus number (default: 1)
    def __init__(self, address=0x70, busnum=1):
        # @var __i2c_addres
        # Objects own I2C address
        self.__i2c_address = address
        # @var __bus
        # Objects own I2C bus number
        self.__bus = smbus.SMBus(busnum)

    ###
    # Activate an output channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel I2C channel to be activated (1-8); value 0 deactivates all channels;
    # @param[out] True in case of success; otherwise False.
    def select(self, channel):
        # Check if given channel is valid
        if (channel < 0) or (channel > 8):
            return False
        # Get the correct bit pattern (only one channel active at a time)
        byte = 0
        if (channel > 0):
            byte = 1<<(channel-1)
        # Try to select the given channel
        try:
            self.__bus.write_byte(self.__i2c_address, byte)
        except:
            return False
        else:
            return True

    ###
    # Read the current settings.
    #
    # @param[in] self The object pointer.
    # @param[out] Config byte value in case of success; otherwise False.
    def read(self):
        raw = 0
        try:
            raw = self.__bus.read_byte(self.__i2c_address)
        except:
            return False
        else:
            return raw
    
    ###
    # Read the currently active channel(s).
    #
    # @param[in] self The object pointer.
    # @param[out] List of currently active channels in case of success; otherwise False.
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
