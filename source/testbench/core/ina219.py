#!/usr/bin/env python3

########################################################################
#   INA219 Wattmeter                                                   #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-15                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     ina = INA219()                                                   #
#     or                                                               #
#     ina = INA219(0x40)        # address                              #
#     or                                                               #
#     ina = INA219(0x40,1)      # address & busnum                     #
#     then                                                             #
#     ina.begin()               # Check and basic configuration        #
#     mic.getChannels()   # Get a list of active channels      #
#                                                                      #
#   See also:                                                          #
#   https://github.com/DFRobot/DFRobot_INA219                          #
#   https://github.com/adafruit/Adafruit_CircuitPython_INA219/blob/master/adafruit_ina219.py #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# I2C functionality
import smbus

##### MIC24045 CLASS ###################
class INA219(object):
    ##### Register Values #####
    ### REGISTER ADDRESSES ###
    INA219_REG_CONFIG               = 0x00      # R/W
    INA219_REG_VSHUNT               = 0x01      # R
    INA219_REG_VBUS                 = 0x02      # R
    INA219_REG_POWER                = 0x03      # R
    INA219_REG_CURRENT              = 0x04      # R
    INA219_REG_CALIBRATION          = 0x05      # R/W
    ### CONFIG ###
    # RST #
    INA219_CONFIG_RESET             = 0x8000
    # BRNG #
    INA219_CONFIG_BRNG_16           = 0
    INA219_CONFIG_BRNG_32           = 1
    # PGA #
    INA219_CONFIG_PGA_1             = 0
    INA219_CONFIG_PGA_2             = 1
    INA219_CONFIG_PGA_4             = 2
    INA219_CONFIG_PGA_8             = 3
    # ADC (Bus / Shunt) #
    INA219_CONFIG_ADC_BITS_9        = 0
    INA219_CONFIG_ADC_BITS_10       = 1
    INA219_CONFIG_ADC_BITS_11       = 2
    INA219_CONFIG_ADC_BITS_12       = 3
    #
    INA219_CONFIG_ADC_SAMPLE_1      = 0
    INA219_CONFIG_ADC_SAMPLE_2      = 1
    INA219_CONFIG_ADC_SAMPLE_4      = 2
    INA219_CONFIG_ADC_SAMPLE_8      = 3
    INA219_CONFIG_ADC_SAMPLE_16     = 4
    INA219_CONFIG_ADC_SAMPLE_32     = 5
    INA219_CONFIG_ADC_SAMPLE_64     = 6
    INA219_CONFIG_ADC_SAMPLE_128    = 7
    # MODE #
    INA219_CONFIG_MODE_PDOWN        = 0
    INA219_CONFIG_MODE_S_TRIG       = 1
    INA219_CONFIG_MODE_B_TRIG       = 2
    INA219_CONFIG_MODE_SB_TRIG      = 3
    INA219_CONFIG_MODE_ADC_OFF      = 4
    INA219_CONFIG_MODE_S_CONT       = 5
    INA219_CONFIG_MODE_B_CONT       = 6
    INA219_CONFIG_MODE_SB_CONT      = 7
    
    # Constructor
    def __init__(self, address=0x40, busnum=1):
        self.__i2c_address = address
        self.__bus = smbus.SMBus(busnum)

    # Check if device at given address exists
    def scan(self):
        try:
            self.__bus.read_byte(self.__i2c_address)
            return True
        except:
            return False


    ##### INITIALIZATION (mode of operation) #####

    # Initialize for max 32V 2A measurement
    def begin_32V_2A(self):
        # Check if device is available
        if not self.scan():
            return False
        else:
            # Set the default values
            self._current_lsb = 0.1         # Current LSB = 100uA per bit
            self._power_lsb = 0.002         # Power LSB = 2mW per bit
            # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 4096
            self._cal_value = 4096
            
            # Write the configuration registers
            self.set_cal_register(self._cal_value)
            self.set_bus_RNG(self.INA219_CONFIG_BRNG_32)
            self.set_PGA(self.INA219_CONFIG_PGA_8)
            self.set_bus_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_shunt_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_mode(self.INA219_CONFIG_MODE_SB_CONT)
            return True

    # Initialize for max 32V 1A measurement
    def begin_32V_1A(self):
        # Check if device is available
        if not self.scan():
            return False
        else:
            # Set the default values
            self._current_lsb = 0.04        # Current LSB = 40uA per bit
            self._power_lsb = 0.0008        # Power LSB = 800uW per bit
            # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 10240
            self._cal_value = 10240
            
            # Write the configuration registers
            self.set_cal_register(self._cal_value)
            self.set_bus_RNG(self.INA219_CONFIG_BRNG_32)
            self.set_PGA(self.INA219_CONFIG_PGA_8)
            self.set_bus_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_shunt_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_mode(self.INA219_CONFIG_MODE_SB_CONT)
            return True

    # Initialize for max 16V 400mA measurement
    def begin_16V_400mA(self):
        # Check if device is available
        if not self.scan():
            return False
        else:
            # Set the default values
            self._current_lsb = 0.05        # Current LSB = 50uA per bit
            self._power_lsb = 0.001         # Power LSB = 1mW per bit
            # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 8192
            self._cal_value = 8192
            
            # Write the configuration registers
            self.set_cal_register(self._cal_value)
            self.set_bus_RNG(self.INA219_CONFIG_BRNG_16)
            self.set_PGA(self.INA219_CONFIG_PGA_1)
            self.set_bus_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_shunt_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_mode(self.INA219_CONFIG_MODE_SB_CONT)
            return True

    # Initialize for max 16V 5A measurement
    def begin_16V_5A(self):
        # Check if device is available
        if not self.scan():
            return False
        else:
            # Set the default values
            self._current_lsb = 0.1524      # Current LSB = 152.4uA per bit
            self._power_lsb = 0.003048      # Power LSB = 3.048mW per bit
            # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 13434
            self._cal_value = 13434
            
            # Write the configuration registers
            self.set_cal_register(self._cal_value)
            self.set_bus_RNG(self.INA219_CONFIG_BRNG_16)
            self.set_PGA(self.INA219_CONFIG_PGA_4)
            self.set_bus_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_shunt_ADC(self.INA219_CONFIG_ADC_BITS_12, self.INA219_CONFIG_ADC_SAMPLE_1)
            self.set_mode(self.INA219_CONFIG_MODE_SB_CONT)
            return True


    ##### I2C READ/WRITE #####

    # Write a value to a given register
    def write_register(self, register, value):
        self.__bus.write_i2c_block_data(self.__i2c_address, register, [(value & 0xFF00) >> 8, value & 0x00FF])

    # Read a register value
    def read_register(self, register):
        return self.__bus.read_i2c_block_data(self.__i2c_address, register) 

    # Read a 16-bit register value and combine the values
    def read_ina_register(self, reg):
        buf = []
        buf = self.read_register(reg)
        if (buf[0] & 0x80):
            return - 0x10000 + ((buf[0] << 8) | (buf[1]))
        else:
            return (buf[0] << 8) | (buf[1])


    ##### RESET ######

    # Reset the INA
    def reset(self):
        # Set the RST bit in the configuration register
        self.write_register(self.INA219_REG_CONFIG, self.INA219_CONFIG_RESET)


    ##### READ REGISTERS ######

    # Read the bus voltage in V
    def get_bus_voltage_V(self):
        return float(self.read_ina_register(self.INA219_REG_VBUS) >> 1) * 0.001

    # Read the shunt voltage in V
    def get_shunt_voltage_V(self):
        return float(self.read_ina_register(self.INA219_REG_VSHUNT)) * 0.001

    # Read the current in mA
    def get_current_mA(self):
        return float(self.read_ina_register(self.INA219_REG_CURRENT)) * self._current_lsb

    # Read the power consumption in W
    def get_power_W(self):
        return float(self.read_ina_register(self.INA219_REG_POWER)) * self._power_lsb

    # Read the power consumption in mW
    def get_power_mW(self):
        return float(self.read_ina_register(self.INA219_REG_POWER)) * (self._power_lsb*1000)


    ##### WRITE REGISTERS #####

    # Set the calibration register
    def set_cal_register(self, value):
        # Write the new value to the calibration register
        self.write_register(self.INA219_REG_CALIBRATION, value)

    # Set the bus voltage range
    def set_bus_RNG(self, brng):
        # Check the given value
        if (brng<self.INA219_CONFIG_BRNG_16) or (brng>self.INA219_CONFIG_BRNG_32):
            return
        # Read config register value
        reg = self.read_ina_register(self.INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xDFFF) | (brng<<13)
        # Write new register value
        self.write_register(self.INA219_REG_CONFIG, conf)

    # Set the shunt voltage PGA
    def set_PGA(self, bits):
        # Check the given value
        if (bits<self.INA219_CONFIG_PGA_1) or (bits>self.INA219_CONFIG_PGA_8):
            return
        # Read config register value
        reg = self.read_ina_register(self.INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xE7FF) | (bits<<11)
        # Write new register value
        self.write_register(self.INA219_REG_CONFIG, conf)
    
    # Set the bus ADC configuration
    def set_bus_ADC(self, bits, sample):
        # Check the given value
        if (bits<self.INA219_CONFIG_ADC_BITS_9) or (bits>self.INA219_CONFIG_ADC_BITS_12):
            return
        if (sample<self.INA219_CONFIG_ADC_SAMPLE_1) or (sample>self.INA219_CONFIG_ADC_SAMPLE_128):
            return
        # Get new ADC configuration
        value = 0
        if(bits < self.INA219_CONFIG_ADC_BITS_12):
            value = bits
        else:
            value = 0x80 | sample
        # Read config register value
        reg = self.read_ina_register(self.INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xF87F) | (value<<7)
        # Write new register value
        self.write_register(self.INA219_REG_CONFIG, conf)
    
    # Set the bus ADC configuration
    def set_shunt_ADC(self, bits, sample):
        # Check the given value
        if (bits<self.INA219_CONFIG_ADC_BITS_9) or (bits>self.INA219_CONFIG_ADC_BITS_12):
            return
        if (sample<self.INA219_CONFIG_ADC_SAMPLE_1) or (sample>self.INA219_CONFIG_ADC_SAMPLE_128):
            return
        # Get new ADC configuration
        value = 0
        if(bits < self.INA219_CONFIG_ADC_BITS_12):
            value = bits
        else:
            value = 0x80 | sample
        # Read config register value
        reg = self.read_ina_register(self.INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xFF87) | (value<<3)
        # Write new register value
        self.write_register(self.INA219_REG_CONFIG, conf)
    
    # Set the operating mode
    def set_mode(self, mode):
        # Check the given value
        if (mode<self.INA219_CONFIG_MODE_PDOWN) or (mode>self.INA219_CONFIG_MODE_SB_CONT):
            return
        # Read config register value
        reg = self.read_ina_register(self.INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xFFF8) | mode
        # Write new register value
        self.write_register(self.INA219_REG_CONFIG, conf)
