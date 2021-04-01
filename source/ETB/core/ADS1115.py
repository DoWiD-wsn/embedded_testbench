#####
# @package ADS1115
# @brief   ADS1115 16-bit ADC
#
# Package containing the ADS1115 16-bit ADC class used on the ETB.
#
# @file     /etb/core/ADS1115.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/01 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @see      https://github.com/adafruit/Adafruit_Python_ADS1x15
# @todo     Extend functionality (comparator, configuration, etc.)
#
# @example  adc = ADS1115()             # Get an instance with default I2C address (0x48)
# @example  ch1 = adc.read_channel(1)   # Read channel 1
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus
# time (for sleep method)
import time


##### GLOBAL VARIABLES #####
# Register addresses (16-bit registers)
ADS1115_REG_CONVERSION      = 0x00
ADS1115_REG_CONFIG          = 0x01
ADS1115_REG_LO_THRESH       = 0x02
ADS1115_REG_HI_THRESH       = 0x03
# Operational status or single-shot conversion start (OS)
ADS1115_OS_OFFSET           = 15
ADS1115_OS_START            = 0x8000
# Input multiplexer (MUX)
ADS1115_MUX_OFFSET          = 12
ADS1115_MUX = {
    0/1: 0x0000,
    0/3: 0x0001,
    1/3: 0x0002,
    2/3: 0x0003,
    0:   0x0004,
    1:   0x0005,
    2:   0x0006,
    3:   0x0007
}
ADS1115_MUX_DEFAULT         = ADS1115_MUX[0/1]
# Programmable gain amplifier configuration (PGA)
ADS1115_PGA_OFFSET          = 9
ADS1115_PGA = {
    2/3: 0x0000,
    1:   0x0001,
    2:   0x0002,
    4:   0x0003,
    8:   0x0004,
    16:  0x0005
}
ADS1115_PGA_DEFAULT         = ADS1115_PGA[2]
# Device operating mode (MODE)
ADS1115_MODE_OFFSET         = 8
ADS1115_MODE_CONTINUOUS     = 0x0000
ADS1115_MODE_SINGLE         = 0x0001
ADS1115_MODE_DEFAULT        = ADS1115_MODE_SINGLE
# Data rate (DR)
ADS1115_DR_OFFSET           = 5
ADS1115_DR = {
    8:    0x0000,
    16:   0x0001,
    32:   0x0002,
    64:   0x0003,
    128:  0x0004,
    250:  0x0005,
    475:  0x0006,
    860:  0x0007
}
ADS1115_DR_DEFAULT          = ADS1115_DR[128]
# Comparator mode (COMP_MODE)
ADS1115_COMP_MODE_OFFSET    = 4
ADS1115_COMP_MODE_DEFAULT   = 0x0000
ADS1115_COMP_MODE_WINDOW    = 0x0001
# Comparator polarity (COMP_POL)
ADS1115_COMP_POL_OFFSET     = 3
ADS1115_COMP_POL_LOW        = 0x0000
ADS1115_COMP_POL_HIGH       = 0x0001
ADS1115_COMP_POL_DEFAULT    = ADS1115_COMP_POL_LOW
# Latching comparator (COMP_LAT)
ADS1115_COMP_LAT_OFFSET     = 2
ADS1115_COMP_LAT_NON        = 0x0000
ADS1115_COMP_LAT_LATCHING   = 0x0001
ADS1115_COMP_LAT_DEFAULT    = ADS1115_COMP_LAT_NON
# Comparator queue and disable (COMP_QUE)
ADS1115_COMP_QUE_OFFSET     = 0
ADS1115_COMP_QUE = {
    1: 0x0000,
    2: 0x0001,
    4: 0x0002,
    0: 0x0003
}
ADS1115_COMP_QUE_DEFAULT    = ADS1115_COMP_QUE[0]


#####
# @class    ADS1115
# @brief    ADS1115 16-bit ADC
#
# Class for the ADS1115 16-bit ADC used on the ETB.
class ADS1115(object):
    ###
    # The constructor.
    #
    # @param[in] self The object pointer.
    # @param[in] address specific I2C address (default: 0x48)
    # @param[in] busnum specific I2C bus number (default: 1)
    def __init__(self, address=0x48, busnum=1):
        # @var __i2c_address
        # Objects own I2C address
        self.__i2c_address = address
        # @var __bus
        # Objects own I2C bus number
        self.__bus = smbus.SMBus(busnum)


    ###
    # Read a 16-bit I2C register value from the ADS (raw).
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[out] List of bytes in case of success; otherwise False.
    def read_register_raw(self, register):
        return self.__bus.read_i2c_block_data(self.__i2c_address, register) 


    ###
    # Read a 16-bit I2C register value from the ADS.
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[out] 16-bit register value in case of success; otherwise False.
    def read_ads_register(self, register):
        buf = []
        buf = self.read_register_raw(register)
        # Convert to 16-bit signed value.
        value = (buf[0]<< 8) | buf[1]
        # Check for sign bit and turn into a negative value if set.
        if value & 0x8000 != 0:
            value -= 1 << 16
        return value


    # Write a 16-bit value to an I2C register of the ADS.
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[in] value Register value to be written.
    # @param[out] True in case of success; otherwise False.
    def write_register(self, register, value):
        self.__bus.write_i2c_block_data(self.__i2c_address, register, [(value & 0xFF00) >> 8, value & 0x00FF])


    ###
    # Read a single ADC channel and return signed integer result.
    #
    # @param[in] self The object pointer.
    # @param[in] address specific I2C address (default: 0x48)
    # @param[in] busnum specific I2C bus number (default: 1)
    # @param[out] Signed conversion value in case of success; otherwise False.
    def read_channel(self, channel, gain=1, data_rate=ADS1115_DR_DEFAULT):
        # Set the mode to single shot
        config = ADS1115_MODE_SINGLE
        # Start a single conversion
        config |= ADS1115_OS_START
        # Check and set the mux value
        if channel not in ADS1115_MUX:
            raise ValueError('Valid channels are:  0/1, 0/3, 1/3, 2/3, 0, 1, 2, 3')
        config |= ADS1115_MUX[channel] << ADS1115_MUX_OFFSET
        # Check and set the gain value
        if gain not in ADS1115_PGA:
            raise ValueError('Valid gain values are: 2/3, 1, 2, 4, 8, 16')
        config |= ADS1115_PGA[gain] << ADS1115_PGA_OFFSET
        # Check and set the data rate value
        if data_rate not in ADS1115_DR:
            raise ValueError('Valid data rate values are: 8, 16, 32, 64, 128, 250, 475, 860')
        config |= ADS1115_DR[data_rate] << ADS1115_DR_OFFSET
        # Disable comparator mode
        config |= ADS1115_COMP_QUE_DEFAULT
        # Write configuration value to the ADS
        self.write_register(ADS1115_REG_CONVERSION,config):
        # Wait for the ADC sample to finish
        time.sleep(1.0/data_rate+0.0001)
        # Get the result from the ADS
        return self.read_ads_register(ADS1115_REG_CONVERSION)
