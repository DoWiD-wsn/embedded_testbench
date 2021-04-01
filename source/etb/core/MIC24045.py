#####
# @package MIC24045
# @brief   MIC24045 DC/DC converter
#
# Package containing the MIC24045 DC/DC converter class used on the ETB.
#
# @file     /etb/core/MIC24045.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/01 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @note     The MIC24045 only reacts when VIN is available
#
# @example  mic = MIC24045(5)             # Get an instance with default I2C address (0x50) and GPIO5 as enable pin
# @example  value = mic.get_register_from_voltage(3.3) # Get the register value corresponding to an voltage of 3.3V
# @example  mic.set_output_voltage(value) # Set the output voltage to the previously calculated decimal value
# @example  vout = mic.get_voltage_V()    # Get the current voltage in Volts (V)
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus
# GPIO functionality (imported as GPIO)
import RPi.GPIO as GPIO
# for GPIO numbering, choose BCM mode
GPIO.setmode(GPIO.BCM)


##### GLOBAL VARIABLES #####
# Register addresses
MIC24045_REG_STATUS = 0x00
MIC24045_REG_SET1   = 0x01
MIC24045_REG_SET2   = 0x02
MIC24045_REG_VOUT   = 0x03
MIC24045_REG_CMD    = 0x04
# Current limit (ILIM; in SET1)
MIC24045_ILIM_2     = 0
MIC24045_ILIM_3     = 1
MIC24045_ILIM_4     = 2
MIC24045_ILIM_5     = 3
# Operating frequency (FREQ; in SET1)
MIC24045_FREQ_310   = 0
MIC24045_FREQ_400   = 1
MIC24045_FREQ_500   = 2
MIC24045_FREQ_570   = 3
MIC24045_FREQ_660   = 4
MIC24045_FREQ_780   = 5
MIC24045_FREQ_970   = 6
MIC24045_FREQ_1200  = 7
# Start-up-delay [ms] (SUD; in SET2)
MIC24045_SUD_0      = 0
MIC24045_SUD_0_5    = 1
MIC24045_SUD_1      = 2
MIC24045_SUD_2      = 3
MIC24045_SUD_4      = 4
MIC24045_SUD_6      = 5
MIC24045_SUD_8      = 6
MIC24045_SUD_10     = 7
# Margin (MRG; in SET2)
MIC24045_MRG_0      = 0
MIC24045_MRG_NEG    = 1
MIC24045_MRG_POS    = 2
MIC24045_MRG_POS    = 3
# Soft-start slop [V/ms] (SS; in SET2)
MIC24045_SS_016     = 0
MIC24045_SS_038     = 1
MIC24045_SS_076     = 2
MIC24045_SS_150     = 3


#####
# @class    MIC24045
# @brief    MIC24045 DC/DC converter class
#
# Class for the MIC24045 DC/DC converte used on the ETB.
class MIC24045(object):
    ###
    # The constructor.
    #
    # @param[in] self The object pointer.
    # @param[in] gpio GPIO pin for the enable signal (in BCM numbering)
    # @param[in] address specific I2C address (default: 0x70)
    # @param[in] busnum specific I2C bus number (default: 1)
    def __init__(self, gpio, address=0x50, busnum=1):
        # @var __i2c_address
        # Objects own I2C address
        self.__i2c_address = address
        # @var __bus
        # Objects own I2C bus number
        self.__bus = smbus.SMBus(busnum)
        # @var __gpio
        # Objects own enable GPIO pin (BCM)
        self.__gpio = gpio

        # Set enable pin to output
        GPIO.setup(self.__gpio, GPIO.OUT)
        # Initially, disable the MIC
        self.disable()
        # Clear the fault flag
        self.clear_fault_flag()
        # Set the current limit to 3A (because of the INA219 limits)
        self.set_current_limit(MIC24045_ILIM_3)
        # Set the operating frequency to 500kHz
        self.set_frequency(MIC24045_FREQ_500)
        # Set the start-up delay to 0ms
        self.set_startup_delay(MIC24045_SUD_0)
        # Set the voltage margin to 0%
        self.set_voltage_margins(MIC24045_MRG_0)
        # Set the soft-start slope to its lowest value (0.16 V/ms)
        self.set_soft_start_slope(MIC24045_SS_016)


    ###
    # Enable the MIC DC/DC converter.
    #
    # @param[in] self The object pointer.
    def enable(self):
        # Set enable GPIO pin to HIGH
        GPIO.output(self.__gpio, GPIO.HIGH)


    ###
    # Disable the MIC DC/DC converter.
    #
    # @param[in] self The object pointer.
    def disable(self):
        # Set enable GPIO pin to LOW
        GPIO.output(self.__gpio, GPIO.LOW)


    ###
    # Read an 8-bit I2C register value from the MIC.
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[out] 8-bit register value in case of success; otherwise False.
    def read_register(self, register):
        # Try to read the given register
        try:
            # Write the register address value
            self.__bus.write_byte(self.__i2c_address, register)
            # Read a byte from this address
            ret = self.__bus.read_byte(self.__i2c_address)
            return ret
        except:
            return False

    
    # Write an 8-bit value to an I2C register of the MIC.
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[in] value Register value to be written.
    # @param[out] True in case of success; otherwise False.
    def write_register(self, register, value):
        # Try to write the given register
        try:
            # Write the byte to the register address
            self.__bus.write_byte_data(self.__i2c_address, register, value)
            return True
        except:
            return False


    ###
    # Read the status register value from the MIC.
    #
    # @param[in] self The object pointer.
    # @param[out] Status register flags in case of success; otherwise False.
    def read_register_status(self):
        # Read the status register
        ret = self.read_register(MIC24045_REG_STATUS)
        # Check if reading was successful
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


    ###
    # Read the setting 1 register value from the MIC.
    #
    # @param[in] self The object pointer.
    # @param[out] Setting 1 register flags in case of success; otherwise False.
    def read_register_setting1(self):
        # Read the setting 1 register
        ret = self.read_register(MIC24045_REG_SET1)
        # Check if reading was successful
        if not ret:
            return False
        # Extract the single flags
        ILIM    = (ret & 0xC0) >> 6
        FREQ    = (ret & 0x38) >> 3
        # Return the flag values
        return (ILIM,FREQ)


    ###
    # Read the setting 2 register value from the MIC.
    #
    # @param[in] self The object pointer.
    # @param[out] Setting 2 register flags in case of success; otherwise False.
    def read_register_setting2(self):
        # Read the setting 2 register
        ret = self.read_register(MIC24045_REG_SET2)
        # Check if reading was successful
        if not ret:
            return False
        # Extract the single flags
        SUD     = (ret & 0x70) >> 4
        MRG     = (ret & 0x0C) >> 2
        SS      = (ret & 0x03)
        # Return the flag values
        return (SUD,MRG,SS)


    ###
    # Read the VOUT register value from the MIC.
    #
    # @param[in] self The object pointer.
    # @param[out] VOUT register value in case of success; otherwise False.
    def read_register_vout(self):
        # Read and return the VOUT register
        return self.read_register(MIC24045_REG_VOUT)


    ###
    # Read the command register value from the MIC.
    #
    # @param[in] self The object pointer.
    # @param[out] CIFF flag in case of success; otherwise False.
    def read_register_command(self):
        # Read the Command register
        ret = self.read_register(MIC24045_REG_CMD)
        # Check if reading was successful
        if not ret:
            return False
        # Extract the flag
        CIFF   = 1 if (ret & 0x01) else 0
        # Return the value
        return CIFF

    ###
    # Check if the MIC is enabled (do not trust the GPIO pin ;) ).
    #
    # @param[in] self The object pointer.
    # @param[out] True if enabled; otherwise False.
    def is_enabled(self):
        # Read the status register
        ret = self.read_register(MIC24045_REG_STATUS)
        # Check if reading was successful
        if not ret:
            return False
        # Check EnS flag
        if (ret & 0x08):
            return True
        else:
            return False

    ###
    # Check the power-good flag.
    #
    # @param[in] self The object pointer.
    # @param[out] True if PGS is set; otherwise False.
    def is_power_good(self):
        # Read the status register
        ret = self.read_register(MIC24045_REG_STATUS)
        # Check if reading was successful
        if not ret:
            return False
        # Check PGS flag
        if (ret & 0x01):
            return True
        else:
            return False


    ###
    # Clear the fault flags.
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def clear_fault_flag(self):
        # Write CIFF to clear all fault flags
        ret = self.write_register(MIC24045_REG_CMD, 0x01)
        # Check return status
        if not ret:
            return False
        else:
            return True


    ###
    # Set the current limit.
    #
    # @param[in] self The object pointer.
    # @param[in] ilim ILIM register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_current_limit(self,ilim):
        # Check given parameter
        if (ilim<0) or (ilim>3):
            return False
        # Read current SETTING 1 register value
        ret = self.read_register(MIC24045_REG_SET1)
        # Check return status
        if not ret:
            return False
        # Prepare the correct register value
        msg = (ret & 0x3F) | (ilim<<6)
        # Write ILIM value to SETTING 1 register
        return self.write_register(MIC24045_REG_SET1, msg)


    ###
    # Set the operating frequency.
    #
    # @param[in] self The object pointer.
    # @param[in] freq FREQ register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_frequency(self,freq):
        # Check given parameter
        if (freq<0) or (freq>7):
            return False
        # Read current SETTING 1 register value
        ret = self.read_register(MIC24045_REG_SET1)
        # Check return status
        if not ret:
            return False
        # Prepare the correct register value
        msg = (ret & 0xC7) | (freq<<3)
        # Write FREQ value to SETTING 1 register
        return self.write_register(MIC24045_REG_SET1, msg)


    ###
    # Set the start-up delay.
    #
    # @param[in] self The object pointer.
    # @param[in] delay SUD register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_startup_delay(self,delay):
        # Check given parameter
        if (delay<0) or (delay>7):
            return False
        # Read current SETTING 2 register value
        ret = self.read_register(MIC24045_REG_SET2)
        # Check return status
        if not ret:
            return False
        # Prepare the correct register value
        msg = (ret & 0x8F) | (delay<<4)
        # Write SUD value to SETTING 2 register
        return self.write_register(MIC24045_REG_SET2, msg)


    ###
    # Set the voltage margins.
    #
    # @param[in] self The object pointer.
    # @param[in] margin MRG register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_voltage_margins(self,margin):
        # Check given parameter
        if (margin<0) or (margin>3):
            return False
        # Read current SETTING 2 register value
        ret = self.read_register(MIC24045_REG_SET2)
        # Check return status
        if not ret:
            return False
        # Prepare the correct register value
        msg = (ret & 0xF3) | (margin<<2)
        # Write MRG value to SETTING 2 register
        return self.write_register(MIC24045_REG_SET2, msg)


    ###
    # Set the soft-start slope.
    #
    # @param[in] self The object pointer.
    # @param[in] slope SS register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_soft_start_slope(self,slope):
        # Check given parameter
        if (slope<0) or (slope>3):
            return False
        # Read current SETTING 2 register value
        ret = self.read_register(MIC24045_REG_SET2)
        # Check return status
        if not ret:
            return False
        # Prepare the correct register value
        msg = (ret & 0xFC) | slope
        # Write SS value to SETTING 2 register
        return self.write_register(MIC24045_REG_SET2, msg)


    ###
    # Set the output voltage VOUT.
    #
    # @param[in] self The object pointer.
    # @param[in] value VOUT value.
    # @param[out] True in case of success; otherwise False.
    def set_output_voltage(self,value):
        # Use only lower 8-bit (in case more is given)
        value = value & 0xFF
        # Write value to VOUT register
        return self.write_register(MIC24045_REG_VOUT, value)



    ###
    # Increment the output voltage VOUT by one step (5/10/30/50 mV).
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def inc_output_voltage(self):
        # Read current VOUT register value
        ret = self.read_register(MIC24045_REG_VOUT)
        # Check return status
        if not ret:
            return False
        # Check if value can be incremented
        if ret<0xFF:
            ret = ret + 1
        else:
            return False
        # Write new value to VOUT register
        return self.write_register(MIC24045_REG_VOUT, ret)


    ###
    # Decrement the output voltage VOUT by one step (5/10/30/50 mV).
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def dec_output_voltage(self):
        # Read current VOUT register value
        ret = self.read_register(MIC24045_REG_VOUT)
        # Check return status
        if not ret:
            return False
        # Check if value can be decremented
        if ret>0x00:
            ret = ret - 1
        else:
            return False
        # Write new value to VOUT register
        return self.write_register(MIC24045_REG_VOUT, ret)


    ###
    # Get the output voltage in volts (V).
    #
    # @param[in] self The object pointer.
    # @param[out] VOUT voltage in volts (V) in case of success; otherwise False.
    def get_voltage_V(self):
        # Read the VOUT register value
        ret = self.read_register_vout()
        # Check return status
        if not ret:
            return False
        # Calculate the corresponding output voltage
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


    ###
    # Get the output voltage in millivolts (mV).
    #
    # @param[in] self The object pointer.
    # @param[out] VOUT voltage in millivolts (mV) in case of success; otherwise False.
    def get_voltage_mV(self):
        # Get the voltage in volts
        vout = self.get_voltage_V()
        # Check return status
        if not vout:
            return False
        else:
            # Convert V to mV
            return (vout*1000)


    ###
    # Convert a decimal register value to an actual voltage in volts (V).
    #
    # @param[in] self The object pointer.
    # @param[out] Corresponding voltage in volts (V); otherwise False.
    def get_voltage_from_register(self,reg):
        # Check given register value
        if (reg<0) or (reg>0xFF):
            return False
        # Calculate the output voltage in volts (V)
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


    ###
    # Convert a voltage in volts to an actual decimal register value.
    #
    # @param[in] self The object pointer.
    # @param[out] Corresponding decimal register value; otherwise False.
    def get_register_from_voltage(self,vout):
        reg = 0
        if vout<0.64:
            # Invalid
            return False
        if vout<1.28:
            # 5mV step sizes
            reg = int((vout-0.64) / 0.005)
        elif vout<1.29:
            # Margin between 5mV and 10mV
            reg = 128
        elif vout<1.95:
            # 10mV step sizes
            reg = int((vout-1.29) / 0.01)+129
        elif vout<1.98:
            # Margin between 10mV and 30mV
            reg = 195
        elif vout<3.42:
            # 30mV step sizes
            reg = int((vout-1.98) / 0.03)+196
        elif vout<4.75:
            # Margin between 30mV and 50mV
            reg = 244
        elif vout<=5.25:
            # 50mV step sizes
            reg = int((vout-4.75) / 0.05)+245
        else:
            # Invalid
            return False
        # Return the value
        return reg
