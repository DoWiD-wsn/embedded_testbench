#####
# @brief   AVR-based frequency counter (FCNT)
#
# Module containing the AVR-based frequency counter (FCNT) class.
#
# @file     /etb/util/FCNT.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/08 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
#
# @example  fcnt = FCNT()                 # Get an instance with default I2C address (0x24)
# @example  ready = fcnt.is_ready()       # Check if measurement is ready
# @example  fmeas = fcnt.get_frequency()  # Get the latest frequency measurement
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus


##### GLOBAL VARIABLES #####
# Register addresses
FCNT_REG_CFG            = 0x00
FCNT_REG_LSB            = 0x01
FCNT_REG_MSB            = 0x02
FCNT_REG_XMSB           = 0x03
### Settings ###
# Reset (RST)
FCNT_CFG_RST_OFFSET     = 7
FCNT_CFG_RST_MASK       = 0x7F
# Ready-flag (RDY)
FCNT_CFG_RDY_OFFSET     = 6
FCNT_CFG_RDY_MASK       = 0xBF
# Sampling rate (SMP)
FCNT_CFG_SMP_OFFSET     = 4
FCNT_CFG_SMP_MASK       = 0xCF
FCNT_CFG_SMP = {
    1:  0x00,
    3:  0x01,
    5:  0x02,
    10: 0x03
}
# Resolution (RES)
FCNT_CFG_RES_OFFSET     = 2
FCNT_CFG_RES_MASK       = 0xF3
FCNT_CFG_RES = {
    'Hz':   0x01,
    'kHz':  0x02,
    'MHz':  0x03
}
# Channel selection (SEL)
FCNT_CFG_SEL_OFFSET     = 0
FCNT_CFG_SEL_MASK       = 0xFC
FCNT_CFG_SEL = {
    0:  0x00,
    1:  0x01,
    2:  0x02,
    3:  0x03
}


#####
# @class    FCNT
# @brief    AVR-based frequency counter (FCNT)
#
# Class for the AVR-based frequency counter (FCNT).
class FCNT(object):
    ###
    # The constructor.
    #
    # @param[in] self The object pointer.
    # @param[in] address specific I2C address (default: 0x24)
    # @param[in] busnum specific I2C bus number (default: 1)
    def __init__(self, address=0x24, busnum=1):
        # @var __i2c_address
        # Object's own I2C address
        self.__i2c_address = address
        # @var __bus
        # Object's own I2C bus number
        self.__bus = smbus.SMBus(busnum)
    
    
    ###
    # Read an unsigned byte (8-bit) from the specified I2C register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[out] Unsigned byte value in case of success; otherwise False.
    def _i2c_read_U8(self, register):
        # Read value from the specified register
        return (self.__bus.read_byte_data(self.__i2c_address, register) & 0xFF)


    ###
    # Write a byte (8-bit) to the specified I2C register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[in] value The byte value to be written.
    # @param[out] True in case of success; otherwise False.
    def _i2c_write_8(self, register, value):
        # Write the given value to the specified register
        self.__bus.write_byte_data(self.__i2c_address, register, (value&0xFF))



    ###
    # Read the configuration register value flags.
    #
    # @param[in] self The object pointer.
    # @param[out] Configuration register flags in case of success; otherwise False.
    def read_config(self):
        # Read the status register
        ret = self._i2c_read_U8(FCNT_REG_CFG)
        if not ret:
            return False
        # Extract the flags
        RDY = (ret & FCNT_CFG_RDY_MASK) >> FCNT_CFG_RDY_OFFSET
        SMP = (ret & FCNT_CFG_SMP_MASK) >> FCNT_CFG_SMP_OFFSET
        RES = (ret & FCNT_CFG_RES_MASK) >> FCNT_CFG_RES_OFFSET
        SEL = (ret & FCNT_CFG_SEL_MASK) >> FCNT_CFG_SEL_OFFSET
        # Return the flag values
        return (RDY,SMP,RES,SEL)


    ###
    # Read the ready flag.
    #
    # @param[in] self The object pointer.
    # @param[out] Ready flag in case of success; otherwise False.
    def get_ready_flag(self):
        # Read the configuration registers
        reg = self.read_config()
        if(reg):
            # Return the ready flag
            return reg[0]
        else:
            return False


    ###
    # Read the sampling configuration.
    #
    # @param[in] self The object pointer.
    # @param[out] Sampling configuration in case of success; otherwise False.
    def get_sampling(self):
        # Read the configuration registers
        reg = self.read_config()
        if(reg):
            # Return the sampling configuration
            return reg[1]
        else:
            return False

    ###
    # Read the resolution configuration.
    #
    # @param[in] self The object pointer.
    # @param[out] Resolution configuration in case of success; otherwise False.
    def get_resolution(self):
        # Read the configuration registers
        reg = self.read_config()
        if(reg):
            # Return the resolution configuration
            return reg[2]
        else:
            return False


    ###
    # Read the channel selection.
    #
    # @param[in] self The object pointer.
    # @param[out] Channel selection in case of success; otherwise False.
    def get_channel(self):
        # Read the configuration registers
        reg = self.read_config()
        if(reg):
            # Return the channel selection
            return reg[3]
        else:
            return False


    ###
    # Check if the ready flag is set.
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def is_ready(self):
        ret = self.get_ready_flag()
        if(ret):
            return True
        else:
            return False


    ###
    # Read the LSB register value.
    #
    # @param[in] self The object pointer.
    # @param[out] LSB register value in case of success; otherwise False.
    def read_LSB(self):
        return self._i2c_read_U8(FCNT_REG_LSB)


    ###
    # Read the MSB register value.
    #
    # @param[in] self The object pointer.
    # @param[out] MSB register value in case of success; otherwise False.
    def read_MSB(self):
        return self._i2c_read_U8(FCNT_REG_MSB)


    ###
    # Read the XMSB register value.
    #
    # @param[in] self The object pointer.
    # @param[out] XMSB register value in case of success; otherwise False.
    def read_XMSB(self):
        return self._i2c_read_U8(FCNT_REG_XMSB)


    ###
    # Get the latest frequency reading.
    #
    # @param[in] self The object pointer.
    # @param[out] Latest frequency reading in case of success; otherwise False.
    def get_frequency(self):
        # Check if measurement is ready
        if not self.is_ready():
            return False
        # Get the current resolution
        res = self.get_resolution()
        if not res:
            return False
        # Number of bytes to read depend on resolution
        lsb  = 0
        msb  = 0
        xmsb = 0
        # For Hz resolution read XMSB
        if (res == FCNT_CFG_RES['Hz']):
            xmsb = self.read_XMSB()
        # For Hz or kHz resolution read MSB
        if (res == FCNT_CFG_RES['Hz']) or (res == FCNT_CFG_RES['kHz']):
            msb = self.read_MSB()
        # In any case read LSB
        lsb = self.read_LSB()
        # Aggregate and return result
        return ((xmsb<<16) | (msb<<8) | lsb)


    ###
    # Set the input channel.
    #
    # @param[in] self The object pointer.
    # @param[in] ch The input channel to be used.
    # @param[out] True in case of success; otherwise False.
    def set_channel(self,ch):
        # Check the channel parameter
        if ch not in FCNT_CFG_SEL:
            raise ValueError('Valid channels are: 0, 1, 2, and 3')
        # Get current CFG register value
        ret = self._i2c_read_U8(FCNT_REG_CFG)
        # Check return status
        if not ret:
            return False
        # Get the new CFG register value
        value = (ret & FCNT_CFG_SEL_MASK) | (FCNT_CFG_SEL[ch]<<FCNT_CFG_SEL_OFFSET)
        # Write new value to CFG register
        return self._i2c_write_8(FCNT_REG_CFG,value)
    

    ###
    # Set the measurement resolution.
    #
    # @param[in] self The object pointer.
    # @param[in] res The measurement resolution to be used.
    # @param[out] True in case of success; otherwise False.
    def set_resolution(self,res):
        # Check the resolution parameter
        if res not in FCNT_CFG_RES:
            raise ValueError('Valid resolution are: \'Hz\', \'kHz\', and \'MHz\'')
        # Read current CFG register value
        ret = self._i2c_read_U8(FCNT_REG_CFG)
        # Check return status
        if not ret:
            return False
        # Get the new CFG register value
        value = (ret & FCNT_CFG_RES_MASK) | (FCNT_CFG_RES[res]<<FCNT_CFG_RES_OFFSET)
        # Write new value to CFG register
        return self._i2c_write_8(FCNT_REG_CFG,value)
    

    ###
    # Set the sampling rate.
    #
    # @param[in] self The object pointer.
    # @param[in] smp The sampling rate to be used.
    # @param[out] True in case of success; otherwise False.
    def set_sampling(self,smp):
        # Check the sampling parameter
        if smp not in FCNT_CFG_SMP:
            raise ValueError('Valid resolution are: 1, 3, 5, and 10')
        # Read current CFG register value
        ret = self._i2c_read_U8(FCNT_REG_CFG)
        # Check return status
        if not ret:
            return False
        # Get the new CFG register value
        value = (ret & FCNT_CFG_SMP_MASK) | (FCNT_CFG_SMP[smp]<<FCNT_CFG_SMP_OFFSET)
        # Write new value to CFG register
        return self._i2c_write_8(FCNT_REG_CFG,value)


    ###
    # Request a reset.
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def reset(self):
        # Read current CFG register value
        ret = self._i2c_read_U8(FCNT_REG_CFG)
        # Check return status
        if not ret:
            return False
        # Get the new CFG register value
        value = (ret & FCNT_CFG_RST_MASK) | (1<<FCNT_CFG_RST_OFFSET)
        # Write new value to CFG register
        return self._i2c_write_8(FCNT_REG_CFG,value)
