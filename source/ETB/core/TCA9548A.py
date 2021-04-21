#####
# @brief   TCA9548A I2C multiplexer
#
# Module containing the TCA9548A multiplexer class used on the ETB.
#
# @file     /etb/core/TCA9548A.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/01 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @see      https://raspberrypi.stackexchange.com/questions/59043/how-to-read-from-multiplexer-with-python-i2c
#
# @example  multiplexer = TCA9548A()      # Get an instance with default I2C address (0x70)
# @example  multiplexer.select(1)         # Select channel 1 (SD0/SC0)
# @example  multiplexer.get_channels()    # Get a list of currently active channels
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus


#####
# @class    TCA9548A
# @brief    TCA9548A I2C multiplexer class
#
# Class for the TCA9548A multiplexer used on the ETB.
class TCA9548A(object):
    ###
    # The constructor.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    address         Specific I2C address (default: 0x70)
    # @param[in]    busnum          Specific I2C bus number (default: 1)
    def __init__(self, address=0x70, busnum=1):
        # @var __i2c_address
        # Object's own I2C address
        self.__i2c_address = address
        # @var __bus
        # Object's own I2C bus number
        self.__bus = smbus.SMBus(busnum)

    ###
    # Activate an output channel.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         I2C channel to be activated (1-8); value 0 deactivates all channels;
    # @return       True in case of success; otherwise False.
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
    # Read the current settings (8-bit).
    #
    # @param[in]    self            The object pointer.
    # @return       Config byte value in case of success; otherwise False.
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
    # @param[in]    self            The object pointer.
    # @return       List of currently active channels in case of success; otherwise False.
    def get_channels(self):
        raw = self.read()
        # Check return value
        if raw is False:
            return False
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
