#####
# @package INA219
# @brief   INA219 wattmeter
#
# Package containing the INA219 wattmeter class used on the ETB.
#
# @file     /etb/core/INA219.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/01 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @see      https://github.com/DFRobot/DFRobot_INA219
# @see      https://github.com/adafruit/Adafruit_CircuitPython_INA219/blob/master/adafruit_ina219.py
#
# @example  ina = INA219()                 # Get an instance with default I2C address (0x40)
# @example  volt = ina.get_bus_voltage_V() # Read the bus voltage in volts (V)
# @example  amps = ina.get_current_mA      # Read the current in milliampere (mA)
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus


##### GLOBAL VARIABLES #####
# Register addresses
INA219_REG_CONFIG         = 0x00
INA219_REG_VSHUNT         = 0x01
INA219_REG_VBUS           = 0x02
INA219_REG_POWER          = 0x03
INA219_REG_CURRENT        = 0x04
INA219_REG_CALIBRATION    = 0x05
# Reset-bit mask (RST)
INA219_RST                = 0x8000
# Bus voltage range (BRNG)
INA219_BRNG_16            = 0
INA219_BRNG_32            = 1
# PGA gain and range for the shunt voltage (PG)
INA219_PG_1               = 0
INA219_PG_2               = 1
INA219_PG_4               = 2
INA219_PG_8               = 3
# ADC resolution (BADC/SADC)
INA219_ADC_BITS_9         = 0
INA219_ADC_BITS_10        = 1
INA219_ADC_BITS_11        = 2
INA219_ADC_BITS_12        = 3
# ADC averaging (BADC/SADC)
INA219_ADC_SAMPLE_1       = 0
INA219_ADC_SAMPLE_2       = 1
INA219_ADC_SAMPLE_4       = 2
INA219_ADC_SAMPLE_8       = 3
INA219_ADC_SAMPLE_16      = 4
INA219_ADC_SAMPLE_32      = 5
INA219_ADC_SAMPLE_64      = 6
INA219_ADC_SAMPLE_128     = 7
# Operating mode (MODE)
INA219_MODE_PDOWN         = 0
INA219_MODE_S_TRIG        = 1
INA219_MODE_B_TRIG        = 2
INA219_MODE_SB_TRIG       = 3
INA219_MODE_ADC_OFF       = 4
INA219_MODE_S_CONT        = 5
INA219_MODE_B_CONT        = 6
INA219_MODE_SB_CONT       = 7


#####
# @class    INA219
# @brief    INA219 wattmeter class
#
# Class for the INA219 wattmeter used on the ETB.
class INA219(object):
    ###
    # The constructor.
    #
    # @param[in] self The object pointer.
    # @param[in] address specific I2C address (default: 0x40)
    # @param[in] busnum specific I2C bus number (default: 1)
    def __init__(self, address=0x40, busnum=1):
        # @var __i2c_address
        # Objects own I2C address
        self.__i2c_address = address
        # @var __bus
        # Objects own I2C bus number
        self.__bus = smbus.SMBus(busnum)
        # @var _current_lsb
        # Objects own current value for LSB (mA)
        self._current_lsb = 0
        # @var _power_lsb
        # Objects own power value for LSB (W)
        self._power_lsb = 0
        # @var _cal_value
        # Objects own calibration value
        self._cal_value = 0
        
        # Calibrate for 16V maximum bus voltage and 400mA maximum current
        self.calibrate_16V_400mA()


    ###
    # Calibrate for max 16V 400mA measurements.
    #
    # @param[in] self The object pointer.
    def calibrate_16V_400mA(self):
        # Current LSB = 50uA per bit
        self._current_lsb = 0.05
        # Power LSB = 1mW per bit
        self._power_lsb = 0.001
        # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 8192
        self._cal_value = 8192
        # Write the configuration registers accordingly
        self.set_cal_register(self._cal_value)
        self.set_bus_RNG(INA219_BRNG_16)
        self.set_PGA(INA219_PG_1)
        self.set_bus_ADC(INA219_ADC_BITS_12, INA219_ADC_SAMPLE_1)
        self.set_shunt_ADC(INA219_ADC_BITS_12, INA219_ADC_SAMPLE_1)
        self.set_mode(INA219_MODE_SB_CONT)


    ###
    # Calibrate for max 16V 5A measurements.
    #
    # @param[in] self The object pointer.
    def begin_16V_5A(self):
        ## Current LSB = 152.4uA per bit
        self._current_lsb = 0.1524
        # Power LSB = 3.048mW per bit
        self._power_lsb = 0.003048
        # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 13434
        self._cal_value = 13434
        # Write the configuration registers accordingly
        self.set_cal_register(self._cal_value)
        self.set_bus_RNG(INA219_BRNG_16)
        self.set_PGA(INA219_PG_4)
        self.set_bus_ADC(INA219_ADC_BITS_12, INA219_ADC_SAMPLE_1)
        self.set_shunt_ADC(INA219_ADC_BITS_12, INA219_ADC_SAMPLE_1)
        self.set_mode(INA219_MODE_SB_CONT)


    ###
    # Read a 16-bit I2C register value from the INA (raw).
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[out] List of bytes in case of success; otherwise False.
    def read_register_raw(self, register):
        return self.__bus.read_i2c_block_data(self.__i2c_address, register) 


    ###
    # Read a 16-bit I2C register value from the INA.
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[out] 16-bit register value in case of success; otherwise False.
    def read_ina_register(self, register):
        buf = []
        buf = self.read_register_raw(register)
        if (buf[0] & 0x80):
            return - 0x10000 + ((buf[0] << 8) | (buf[1]))
        else:
            return (buf[0] << 8) | (buf[1])


    # Write a 16-bit value to an I2C register of the INA.
    #
    # @param[in] self The object pointer.
    # @param[in] register Register address.
    # @param[in] value Register value to be written.
    # @param[out] True in case of success; otherwise False.
    def write_register(self, register, value):
        self.__bus.write_i2c_block_data(self.__i2c_address, register, [(value & 0xFF00) >> 8, value & 0x00FF])


    # Request a reset of the INA.
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def reset(self):
        # Set the RST bit in the configuration register
        self.write_register(INA219_REG_CONFIG, INA219_RST)


    ###
    # Read the bus voltage in volts (V).
    #
    # @param[in] self The object pointer.
    # @param[out] Bus voltage in volts (V) in case of success; otherwise False.
    def get_bus_voltage_V(self):
        return float(self.read_ina_register(INA219_REG_VBUS) >> 1) * 0.001


    ###
    # Read the shunt voltage in volts (V).
    #
    # @param[in] self The object pointer.
    # @param[out] Shunt voltage in volts (V) in case of success; otherwise False.
    def get_shunt_voltage_V(self):
        return float(self.read_ina_register(INA219_REG_VSHUNT)) * 0.001


    ###
    # Read the current in milliamps (mA).
    #
    # @param[in] self The object pointer.
    # @param[out] Calibrated current in milliamps (mA) in case of success; otherwise False.
    def get_current_mA(self):
        return float(self.read_ina_register(INA219_REG_CURRENT)) * self._current_lsb


    ###
    # Read the power register in watts (W).
    #
    # @param[in] self The object pointer.
    # @param[out] Calibrated power in watts (W) in case of success; otherwise False.
    def get_power_W(self):
        return float(self.read_ina_register(INA219_REG_POWER)) * self._power_lsb


    ###
    # Read the power register in milliwatts (mW).
    #
    # @param[in] self The object pointer.
    # @param[out] Calibrated power in milliwatts (mW) in case of success; otherwise False.
    def get_power_mW(self):
        return float(self.read_ina_register(INA219_REG_POWER)) * (self._power_lsb*1000)


    ###
    # Set the calibration register.
    #
    # @param[in] self The object pointer.
    # @param[in] value Calibration register value.
    # @param[out] True in case of success; otherwise False.
    def set_cal_register(self, value):
        self.write_register(INA219_REG_CALIBRATION, value)


    ###
    # Set the bus voltage range (BRNG).
    #
    # @param[in] self The object pointer.
    # @param[in] brng BRNG register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_bus_RNG(self, brng):
        # Check the given value
        if (brng<INA219_BRNG_16) or (brng>INA219_BRNG_32):
            return
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xDFFF) | (brng<<13)
        # Write new register value
        self.write_register(INA219_REG_CONFIG, conf)


    ###
    # Set the shunt voltage PGA gain and range (PG).
    #
    # @param[in] self The object pointer.
    # @param[in] pg PG register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_PGA(self, pg):
        # Check the given value
        if (pg<INA219_PG_1) or (pg>INA219_PG_8):
            return
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xE7FF) | (pg<<11)
        # Write new register value
        self.write_register(INA219_REG_CONFIG, conf)

    
    ###
    # Set the Bus ADC Resolution/Averaging (BADC).
    #
    # @param[in] self The object pointer.
    # @param[in] resolution ADC resolution register value (use pre-defined values!).
    # @param[in] averaging ADC averaging register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_bus_ADC(self, bits, sample):
        # Check the given value
        if (bits<INA219_ADC_BITS_9) or (bits>INA219_ADC_BITS_12):
            return
        if (sample<INA219_ADC_SAMPLE_1) or (sample>INA219_ADC_SAMPLE_128):
            return
        # Get new ADC configuration
        value = 0
        if(bits < INA219_ADC_BITS_12):
            value = bits
        else:
            value = 0x80 | sample
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xF87F) | (value<<7)
        # Write new register value
        self.write_register(INA219_REG_CONFIG, conf)


    ###
    # Set the Shunt ADC Resolution/Averaging (SADC).
    #
    # @param[in] self The object pointer.
    # @param[in] resolution ADC resolution register value (use pre-defined values!).
    # @param[in] averaging ADC averaging register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_shunt_ADC(self, bits, sample):
        # Check the given value
        if (bits<INA219_ADC_BITS_9) or (bits>INA219_ADC_BITS_12):
            return
        if (sample<INA219_ADC_SAMPLE_1) or (sample>INA219_ADC_SAMPLE_128):
            return
        # Get new ADC configuration
        value = 0
        if(bits < INA219_ADC_BITS_12):
            value = bits
        else:
            value = 0x80 | sample
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xFF87) | (value<<3)
        # Write new register value
        self.write_register(INA219_REG_CONFIG, conf)

    
    ###
    # Set the operating mode (MODE).
    #
    # @param[in] self The object pointer.
    # @param[in] mode MODE register value (use pre-defined values!).
    # @param[out] True in case of success; otherwise False.
    def set_mode(self, mode):
        # Check the given value
        if (mode<INA219_MODE_PDOWN) or (mode>INA219_MODE_SB_CONT):
            return
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xFFF8) | mode
        # Write new register value
        self.write_register(INA219_REG_CONFIG, conf)
