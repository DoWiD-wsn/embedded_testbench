#####
# @brief   INA219 wattmeter
#
# Module containing the INA219 wattmeter class used on the ETB.
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
INA219_BRNG_OFFSET        = 13
INA219_BRNG = {
    16:     0x00,
    32:     0x01
}
INA219_BRNG_DEFAULT        = 32
# PGA gain and range for the shunt voltage (PG)
INA219_PG_OFFSET          = 11
INA219_PG = {
    40:     0x00,
    80:     0x01,
    160:    0x02,
    320:    0x03
}
INA219_PG_DEFAULT         = 320
# ADC (BADC/SADC)
INA219_BADC_OFFSET        = 7
INA219_SADC_OFFSET        = 3
INA219_ADC_DEFAULT        = 0x0011
# ADC resolution
INA219_ADC_BITS = {
    9:      0x00,
    10:     0x01,
    11:     0x02,
    12:     0x03
}
# ADC averaging
INA219_ADC_SAMPLE = {
    1:      0x00,
    2:      0x01,
    4:      0x02,
    8:      0x03,
    16:     0x04,
    32:     0x05,
    64:     0x06,
    128:    0x07
}
# Operating mode (MODE)
INA219_MODE_PDOWN         = 0
INA219_MODE_S_TRIG        = 1
INA219_MODE_B_TRIG        = 2
INA219_MODE_SB_TRIG       = 3
INA219_MODE_ADC_OFF       = 4
INA219_MODE_S_CONT        = 5
INA219_MODE_B_CONT        = 6
INA219_MODE_SB_CONT       = 7
# Calibration (CAL)
INA219_CAL_400MA          = 0
INA219_CAL_5A             = 1


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
        # Object's own I2C address
        self.__i2c_address = address
        # @var __bus
        # Object's own I2C bus number
        self.__bus = smbus.SMBus(busnum)
        # @var _current_lsb
        # Object's own current value for LSB (mA)
        self._current_lsb = 0
        # @var _power_lsb
        # Object's own power value for LSB (W)
        self._power_lsb = 0
        # @var _cal_value
        # Object's own calibration value
        self._cal_value = 0


    ###
    # Calibrate for max 16V 400mA measurements.
    #
    # @param[in] self The object pointer.
    # @param[in] imax Maximum current (default: 400mA)
    def calibrate(self,imax=INA219_CAL_400MA):
        # Calibrate the INA accordingly
        if imax==INA219_CAL_400MA:
            self._calibrate_16V_400mA()
        elif imax==INA219_CAL_5A:
            self._calibrate_16V_5A()
        else:
            raise ValueError('Valid imax values are: 400mA and 5A')

    ###
    # Calibrate for max 16V 400mA measurements.
    #
    # @param[in] self The object pointer.
    def _calibrate_16V_400mA(self):
        # Current LSB = 50uA per bit
        self._current_lsb = 0.05
        # Power LSB = 1mW per bit
        self._power_lsb = 0.001
        # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 8192
        self._cal_value = 8192
        # Write the configuration registers accordingly
        self.set_cal_register(self._cal_value)
        self.set_bus_RNG(16)
        self.set_PGA(40)
        self.set_bus_ADC(12,1)
        self.set_shunt_ADC(12,1)
        self.set_mode(INA219_MODE_SB_CONT)


    ###
    # Calibrate for max 16V 5A measurements.
    #
    # @param[in] self The object pointer.
    def _calibrate_16V_5A(self):
        ## Current LSB = 152.4uA per bit
        self._current_lsb = 0.1524
        # Power LSB = 3.048mW per bit
        self._power_lsb = 0.003048
        # cal_value = trunc(0.04096 / (Current_LSB * RSHUNT)) = 13434
        self._cal_value = 13434
        # Write the configuration registers accordingly
        self.set_cal_register(self._cal_value)
        self.set_bus_RNG(16)
        self.set_PGA(320)
        self.set_bus_ADC(12, 1)
        self.set_shunt_ADC(12, 1)
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
        # Convert to 16-bit signed value.
        value = (buf[0]<< 8) | buf[1]
        # Check for sign bit and turn into a negative value if set.
        if value & 0x8000 != 0:
            value -= 1 << 16
        return value


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
        if brng not in INA219_BRNG:
            raise ValueError('Valid BRNG values are:  16 and 32')
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xDFFF) | (INA219_BRNG[brng]<<INA219_BRNG_OFFSET)
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
        if pg not in INA219_PG:
            raise ValueError('Valid PG values are:  40, 80, 160, and 320 [mV]')
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xE7FF) | (INA219_PG[pg]<<INA219_PG_OFFSET)
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
        # Check the given values
        if bits not in INA219_ADC_BITS:
            raise ValueError('Valid resolution values are:  9, 10, 11, and 12')
        if sample not in INA219_ADC_SAMPLE:
            raise ValueError('Valid sample values are:  1, 2, 4, 8, 16, 32, 64, 128')
        # Get new ADC configuration
        value = 0
        if(bits < 12):
            value = INA219_ADC_BIT[bits]
        else:
            value = 0x80 | INA219_ADC_SAMPLE[sample]
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xF87F) | (value<<INA219_BADC_OFFSET)
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
        # Check the given values
        if bits not in INA219_ADC_BITS:
            raise ValueError('Valid resolution values are:  9, 10, 11, and 12')
        if sample not in INA219_ADC_SAMPLE:
            raise ValueError('Valid sample values are:  1, 2, 4, 8, 16, 32, 64, 128')
        # Get new ADC configuration
        value = 0
        if(bits < 12):
            value = INA219_ADC_BIT[bits]
        else:
            value = 0x80 | INA219_ADC_SAMPLE[sample]
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xF87F) | (value<<INA219_SADC_OFFSET)
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
            raise ValueError('Invalid mode value!')
        # Read config register value
        reg = self.read_ina_register(INA219_REG_CONFIG)
        # Prepare new register value
        conf = (reg & 0xFFF8) | mode
        # Write new register value
        self.write_register(INA219_REG_CONFIG, conf)
