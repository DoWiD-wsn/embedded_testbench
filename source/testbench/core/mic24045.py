#!/usr/bin/env python3

########################################################################
#   MIC24045 DC/DC Converter                                           #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-14                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) The MIC24045 only reacts when VIN is available (VCC not use)#
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     mic = MIC24045(5)             # GPIO enable                      #
#     or                                                               #
#     mic = MIC24045(5, 0x50)       # GPIO enable & address            #
#     or                                                               #
#     mic = MIC24045(5, 0x50,1)     # GPIO enable, address busnum      #
#     then                                                             #
#     mic.select(1)       # Select channel 1                           #
#     mic.getChannels()   # Get a list of active channels              #
#                                                                      #
#   See also:                                                          #
#   https://pypi.org/project/RPi.GPIO/                                 #
#   https://pypi.org/project/smbus2/                                   #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# math functionality
from math import floor
# I2C functionality
import smbus
# GPIO functionality
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

##### MIC24045 CLASS ###################
class MIC24045(object):
    ##### Register Values #####
    ### REGISTER ADDRESSES ###
    MIC24045_REG_STATUS     = 0x00
    MIC24045_REG_SET1       = 0x01
    MIC24045_REG_SET2       = 0x02
    MIC24045_REG_VOUT       = 0x03
    MIC24045_REG_CMD        = 0x04
    ### SETTING1 ###
    # ILIM #
    MIC24045_SET1_ILIM_2    = 0
    MIC24045_SET1_ILIM_3    = 1
    MIC24045_SET1_ILIM_4    = 2
    MIC24045_SET1_ILIM_5    = 3
    # FREQ #
    MIC24045_SET1_FREQ_310  = 0
    MIC24045_SET1_FREQ_400  = 1
    MIC24045_SET1_FREQ_500  = 2
    MIC24045_SET1_FREQ_570  = 3
    MIC24045_SET1_FREQ_660  = 4
    MIC24045_SET1_FREQ_780  = 5
    MIC24045_SET1_FREQ_970  = 6
    MIC24045_SET1_FREQ_1200 = 7
    ### SETTING2 ###
    # SUD [ms] #
    MIC24045_SET2_SUD_0     = 0
    MIC24045_SET2_SUD_0_5   = 1
    MIC24045_SET2_SUD_1     = 2
    MIC24045_SET2_SUD_2     = 3
    MIC24045_SET2_SUD_4     = 4
    MIC24045_SET2_SUD_6     = 5
    MIC24045_SET2_SUD_8     = 6
    MIC24045_SET2_SUD_10    = 7
    # MRG #
    MIC24045_SET2_MRG_0     = 0
    MIC24045_SET2_MRG_NEG   = 1
    MIC24045_SET2_MRG_POS   = 2
    MIC24045_SET2_MRG_POS   = 3
    # SS [V/ms] #
    MIC24045_SET2_SS_016    = 0
    MIC24045_SET2_SS_038    = 1
    MIC24045_SET2_SS_076    = 2
    MIC24045_SET2_SS_150    = 3
    
    # Constructor
    def __init__(self, gpio, address=0x50, busnum=1):
        self.__i2c_address = address
        self.__bus = smbus.SMBus(busnum)
        self.__gpio = gpio
        # Set enable pin aus output
        GPIO.setup(self.__gpio, GPIO.OUT)
        self.disable()
        # Basic configuration
        self.clear_fault_flag()
        self.set_current_limit(self.MIC24045_SET1_ILIM_2)
        self.set_frequency(self.MIC24045_SET1_FREQ_500)
        self.set_startup_delay(self.MIC24045_SET2_SUD_0)
        self.set_voltage_margins(self.MIC24045_SET2_MRG_0)
        self.set_soft_start_slope(self.MIC24045_SET2_SS_016)


    ##### ENABLE/DISABLE ######
    
    # Enable MIC
    def enable(self):
        # Set enable pin to HIGH
        GPIO.output(self.__gpio, GPIO.HIGH)

    # Disable MIC
    def disable(self):
        # Set enable pin to LOW
        GPIO.output(self.__gpio, GPIO.LOW)


    ##### I2C READ/WRITE #####
    
    # Read register value from MIC
    def read_register(self, register):
        # Try to read the given register
        try:
            self.__bus.write_byte(self.__i2c_address, register)
            ret = self.__bus.read_byte(self.__i2c_address)
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
    
    # Read the status register
    def read_register_status(self):
        # Read the status register
        ret = self.read_register(self.MIC24045_REG_STATUS)
        if not ret:
            return False
        # Extract the single flags
        OCF    = 1 if (ret & 0x80) else 0
        ThSDF  = 1 if (ret & 0x40) else 0
        ThWrnF = 1 if (ret & 0x20) else 0
        EnS    = 1 if (ret & 0x08) else 0
        PGS    = 1 if (ret & 0x01) else 0
        # Return the flag values
        return (OCF,ThSDF,ThWrnF,EnS,PGS)

    # Read the setting 1 register
    def read_register_setting1(self):
        # Read the setting 1 register
        ret = self.read_register(self.MIC24045_REG_SET1)
        if not ret:
            return False
        # Extract the single flags
        ILIM    = (ret & 0xC0) >> 6
        FREQ    = (ret & 0x38) >> 3
        # Return the flag values
        return (ILIM,FREQ)

    # Read the setting 2 register
    def read_register_setting2(self):
        # Read the setting 2 register
        ret = self.read_register(self.MIC24045_REG_SET2)
        if not ret:
            return False
        # Extract the single flags
        SUD     = (ret & 0x70) >> 4
        MRG     = (ret & 0x0C) >> 2
        SS      = (ret & 0x03)
        # Return the flag values
        return (SUD,MRG,SS)

    # Read the VOUT register
    def read_register_vout(self):
        # Read and return the VOUT register
        return self.read_register(self.MIC24045_REG_VOUT)

    # Read the command register
    def read_register_command(self):
        # Read the Command register
        ret = self.read_register(self.MIC24045_REG_CMD)
        if not ret:
            return False
        CIFF   = 1 if (ret & 0x01) else 0
        # Return the value
        return CIFF
    
    def is_enabled(self):
        # Read the status register
        ret = self.read_register(self.MIC24045_REG_STATUS)
        if not ret:
            return False
        # Check EnS flag
        if (ret & 0x08):
            return True
        else:
            return False
    
    def is_power_good(self):
        # Read the status register
        ret = self.read_register(self.MIC24045_REG_STATUS)
        if not ret:
            return False
        # Check PGS flag
        if (ret & 0x01):
            return True
        else:
            return False


    ##### WRITE REGISTERS #####
    
    # Clear the fault flags
    def clear_fault_flag(self):
        # Write CIFF to clear all fault flags
        ret = self.write_register(self.MIC24045_REG_CMD, 0x01)
        # Check return status
        if not ret:
            return False
        else:
            return True

    # Set the current limit
    def set_current_limit(self,ilim):
        # Check given parameter
        if (ilim<0) or (ilim>3):
            return False
        # Read current SETTING 1 register value
        ret = self.read_register(self.MIC24045_REG_SET1)
        # Check return status
        if not ret:
            return False
        msg = (ret & 0x3F) | (ilim<<6)
        # Write ILIM value to SETTING 1 register
        return self.write_register(self.MIC24045_REG_SET1, msg)

    # Set the operating frequency
    def set_frequency(self,freq):
        # Check given parameter
        if (freq<0) or (freq>7):
            return False
        # Read current SETTING 1 register value
        ret = self.read_register(self.MIC24045_REG_SET1)
        # Check return status
        if not ret:
            return False
        msg = (ret & 0xC7) | (freq<<3)
        # Write FREQ value to SETTING 1 register
        return self.write_register(self.MIC24045_REG_SET1, msg)

    # Set the start-up delay
    def set_startup_delay(self,delay):
        # Check given parameter
        if (delay<0) or (delay>7):
            return False
        # Read current SETTING 2 register value
        ret = self.read_register(self.MIC24045_REG_SET2)
        # Check return status
        if not ret:
            return False
        msg = (ret & 0x8F) | (delay<<4)
        # Write SUD value to SETTING 2 register
        return self.write_register(self.MIC24045_REG_SET2, msg)

    # Set the voltage margins
    def set_voltage_margins(self,margin):
        # Check given parameter
        if (margin<0) or (margin>3):
            return False
        # Read current SETTING 2 register value
        ret = self.read_register(self.MIC24045_REG_SET2)
        # Check return status
        if not ret:
            return False
        msg = (ret & 0xF3) | (margin<<2)
        # Write MRG value to SETTING 2 register
        return self.write_register(self.MIC24045_REG_SET2, msg)

    # Set the soft start-slope
    def set_soft_start_slope(self,slope):
        # Check given parameter
        if (slope<0) or (slope>3):
            return False
        # Read current SETTING 2 register value
        ret = self.read_register(self.MIC24045_REG_SET2)
        # Check return status
        if not ret:
            return False
        msg = (ret & 0xFC) | slope
        # Write SS value to SETTING 2 register
        return self.write_register(self.MIC24045_REG_SET2, msg)

    # Set the output voltage VOUT
    def set_output_voltage(self,value):
        # Check given parameter
        value = value & 0xFF
        # Write value to VOUT register
        return self.write_register(self.MIC24045_REG_VOUT, value)


    ##### MISC #####
    # Increment the output voltage VOUT
    def inc_output_voltage(self):
        # Read current VOUT register value
        ret = self.read_register(self.MIC24045_REG_VOUT)
        # Check return status
        if not ret:
            return False
        # Check if value you be incremented
        if ret<0xFF:
            ret = ret + 1
        else:
            return False
        # Write value to VOUT register
        return self.write_register(self.MIC24045_REG_VOUT, ret)

    # Decrement the output voltage VOUT
    def dec_output_voltage(self):
        # Read current VOUT register value
        ret = self.read_register(self.MIC24045_REG_VOUT)
        # Check return status
        if not ret:
            return False
        # Check if value you be decremented
        if ret>0x00:
            ret = ret - 1
        else:
            return False
        # Write value to VOUT register
        return self.write_register(self.MIC24045_REG_VOUT, ret)

    # Get the output voltage in volts
    def get_voltage_V(self):
        # Read the VOUT register
        ret = self.read_registerVOUT()
        if not ret:
            return False
        # Calculate the output voltage
        vout = 0
        if reg<129:
            # 5mV step sizes
            vout = (reg * 0.005) + 0.640
        elif reg<196:
            # 10mV step sizes
            vout = ((reg-129) * 0.01) + 1.29
        elif reg<245:
            # 30mV step sizes
            vout = ((reg-196) * 0.03) + 1.98
        else:
            # 50mV step sizes
            vout = ((reg-245) * 0.05) + 4.75
        # Return the value
        return vout

    # Get the output voltage in millivolts
    def get_voltage_mV(self):
        # Get the voltage in volts
        vout = self.get_voltage_V()
        if not vout:
            return False
        else:
            return (vout*1000)

    # Convert a decimal register value to an actual voltage
    def get_voltage_from_register(self,reg):
        # Check given register value
        if (reg<0) or (reg>0xFF):
            return False
        # Calculate the output voltage
        vout = 0
        if reg<129:
            # 5mV step sizes
            vout = (reg * 0.005) + 0.640
        elif reg<196:
            # 10mV step sizes
            vout = ((reg-129) * 0.01) + 1.29
        elif reg<245:
            # 30mV step sizes
            vout = ((reg-196) * 0.03) + 1.98
        else:
            # 50mV step sizes
            vout = ((reg-245) * 0.05) + 4.75
        # Return the value
        return vout

    # Convert a decimal register value to an actual voltage
    def get_register_from_voltage(self,vout):
        reg = 0
        if vout<0.64:
            # Invalid #
            return False
        if vout<1.28:
            # 5mV step sizes
            reg = floor((vout-0.64) / 0.005)
        elif vout<1.29:
            # Margin between 5mV and 10mV -> set to lower boundary
            reg = 128
        elif vout<1.95:
            # 10mV step sizes
            reg = floor((vout-1.29) / 0.01)+129
        elif vout<1.98:
            # Margin between 10mV and 30mV -> set to lower boundary
            reg = 195
        elif vout<3.42:
            # 30mV step sizes
            reg = floor((vout-1.98) / 0.03)+196
        elif vout<4.75:
            # Margin between 30mV and 50mV -> set to lower boundary
            reg = 244
        elif vout<=5.25:
            # 50mV step sizes
            reg = floor((vout-4.75) / 0.05)+245
        else:
            # Invalid #
            return False
        # Return the value
        return reg
