#!/usr/bin/env python3

########################################################################
#   AVR-based Frequency Counter                                        #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-11-30                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     fcnt = FREQCNT()                                                 #
#     or                                                               #
#     fcnt = FREQCNT(0x24)          # address                          #
#     or                                                               #
#     fcnt = FREQCNT(0x24,1)        # address & busnum                 #
#     then                                                             #
#     fcnt.set_channel(0)           # set the input channel            #
#     fcnt.set_resolution(0)        # set the measurement resolution   #
#     fcnt.set_sampling(0)          # set the sampling mode            #
#     ready = fcnt.is_ready()       # check if measurement is ready    #
#     fmeas = fcnt.get_frequency()  # get the latest frequency reading #
#     fcnt.reset()                  # reset the frequency counter      #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# I2C functionality
import smbus

##### FREQCNT CLASS ###################
class FREQCNT(object):
    ##### Register Values #####
    ### REGISTER ADDRESSES ###
    REG_CFG     = 0x00      # R/W
    REG_LSB     = 0x01      # R
    REG_MSB     = 0x02      # R
    REG_XMSB    = 0x03      # R
    ### CONFIG ###
    # RST #
    CFG_RST         = 7
    CFG_RST_MASK    = 0x80
    # RDY #
    CFG_RDY         = 6
    CFG_RDY_MASK    = 0x40
    # SAMPLING #
    CFG_SMP         = 4
    CFG_SMP_MASK    = 0x30
    CFG_SMP_1       = 0
    CFG_SMP_3       = 1
    CFG_SMP_5       = 2
    CFG_SMP_10      = 3
    # RESOLUTION #
    CFG_RES         = 2
    CFG_RES_MASK    = 0x0C
    CFG_RES_HZ      = 0
    CFG_RES_KHZ     = 1
    CFG_RES_MHZ     = 2
    # CHANNEL #
    CFG_SEL         = 0
    CFG_SEL_MASK    = 0x03
    CFG_SEL_CH0     = 0
    CFG_SEL_CH1     = 1
    CFG_SEL_CH2     = 2
    CFG_SEL_CH3     = 3
    
    # Constructor
    def __init__(self, address=0x24, busnum=1):
        self.__i2c_address = address
        self.__bus = smbus.SMBus(busnum)
    
    
    ##### I2C READ/WRITE #####
    
    # Read register value from MIC
    def read_register(self, register):
        # Try to read the given register
        try:
            ret = self.__bus.read_byte_data(self.__i2c_address, register)
            return ret
        except:
            return False

    # Write a register value of the MIC
    def write_register(self, register, value):
        # Try to write the given register
        try:
            self.__bus.write_byte_data(self.__i2c_address, register, value)
            return True
        except:
            return False


    ##### READ REGISTERS #####
    
    # Read the config register
    def read_register_config(self):
        # Read the status register
        ret = self.read_register(self.REG_CFG)
        if not ret:
            return False
        # Extract the single flags
        RDY = (ret & self.CFG_RDY_MASK) >> self.CFG_RDY
        SMP = (ret & self.CFG_SMP_MASK) >> self.CFG_SMP
        RES = (ret & self.CFG_RES_MASK) >> self.CFG_RES
        SEL = (ret & self.CFG_SEL_MASK) >> self.CFG_SEL
        # Return the flag values
        return (RDY,SMP,RES,SEL)

    # Read the ready flag from the config register
    def get_ready_flag(self):
        reg = self.read_register_config()
        if(reg):
            return reg[0]
        else:
            return False

    # Read the sampling from the config register
    def get_sampling(self):
        reg = self.read_register_config()
        if(reg):
            return reg[1]
        else:
            return False

    # Read the resolution from the config register
    def get_resolution(self):
        reg = self.read_register_config()
        if(reg):
            return reg[2]
        else:
            return False

    # Read the channel selection from the config register
    def get_channel(self):
        reg = self.read_register_config()
        if(reg):
            return reg[3]
        else:
            return False

    # Return true if the ready flag is set
    def is_ready(self):
        ret = self.get_ready_flag()
        if(ret):
            return True
        else:
            return False

    # Read the LSB register
    def read_register_lsb(self):
        # Read the status register
        ret = self.read_register(self.REG_LSB)
        if not ret:
            return False
        # Return the value
        return ret

    # Read the MSB register
    def read_register_msb(self):
        # Read the status register
        ret = self.read_register(self.REG_MSB)
        if not ret:
            return False
        # Return the value
        return ret

    # Read the XMSB register
    def read_register_xmsb(self):
        # Read the status register
        ret = self.read_register(self.REG_XMSB)
        if not ret:
            return False
        # Return the value
        return ret

    # Get the latest frequency reading
    def get_frequency(self):
        # First get the current resolution
        res = self.get_resolution()
        if not res:
            return False
        # Number of bytes to read depends on resolution
        lsb  = 0
        msb  = 0
        xmsb = 0
        # For Hz resolution read XMSB
        if res == self.CFG_RES_HZ:
            xmsb = self.read_register_xmsb()
        # For Hz or kHz resolution read MSB
        if (res == self.CFG_RES_HZ) or (res == self.CFG_RES_KHZ):
            msb = self.read_register_msb()
        # In any case read LSB
        lsb = self.read_register_lsb()
        # Aggregate and return result
        return ((xmsb<<16) | (msb<<8) | lsb)


    ##### WRITE REGISTERS #####
    
    # Set the input channel
    def set_channel(self,ch):
        # Check given parameter
        if (ch<0) or (ch>3):
            return False
        # Read current CFG register value
        ret = self.read_register(self.REG_CFG)
        # Check return status
        if not ret:
            return False
        val = (ret & ~self.CFG_SEL_MASK) | (ch<<self.CFG_SEL)
        # Write new value to CFG register
        return self.write_register(self.REG_CFG,val)
    
    # Set the measurement resolution
    def set_resolution(self,res):
        # Check given parameter
        if (res<0) or (res>2):
            return False
        # Read current CFG register value
        ret = self.read_register(self.REG_CFG)
        # Check return status
        if not ret:
            return False
        val = (ret & ~self.CFG_RES_MASK) | (res<<self.CFG_RES)
        # Write new value to CFG register
        return self.write_register(self.REG_CFG,val)
    
    # Set the sampling mode
    def set_sampling(self,smp):
        # Check given parameter
        if (smp<0) or (smp>3):
            return False
        # Read current CFG register value
        ret = self.read_register(self.REG_CFG)
        # Check return status
        if not ret:
            return False
        val = (ret & ~self.CFG_SMP_MASK) | (smp<<self.CFG_SMP)
        # Write new value to CFG register
        return self.write_register(self.REG_CFG,val)
    
    # Request a reset
    def reset(self):
        # Read current CFG register value
        ret = self.read_register(self.REG_CFG)
        # Check return status
        if not ret:
            return False
        val = (ret & ~self.CFG_RST_MASK) | (1<<self.CFG_RST)
        # Write new value to CFG register
        return self.write_register(self.REG_CFG,val)
