#####
# @brief   BME280 environmental sensor
#
# Module containing the BME280 environmental sensor class.
#
# @file     /etb/sens/BME280.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/02 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @see      https://github.com/adafruit/Adafruit_Python_BME280/
# @see      https://github.com/rm-hull/bme280
#
# @example  bme = BME280()                # Get an instance with default I2C address (0x76)
# @example  temp = bme.read_temperature() # Read the current temperature [°C]
# @example  pres = bme.read_pressure()    # Read the current pressure [hPa]
# @example  humi = bme.read_humidity()    # Read the current relative humidity [%]
# @example  dewp = bme.read_dewpoint()    # Calculate the dewpoint [°C]
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus
# time (for sleep method)
import time


##### GLOBAL VARIABLES #####
# Register addresses
BME280_REG_CHIPID       = 0xD0
BME280_REG_RESET        = 0xE0
BME280_REG_CTRL_HUM     = 0xF2
BME280_REG_STATUS       = 0xF3
BME280_REG_CTRL_MEAS    = 0xF4
BME280_REG_CONFIG       = 0xF5
BME280_REG_P_MSB        = 0xF7
BME280_REG_P_LSB        = 0xF8
BME280_REG_P_XLSB       = 0xF9
BME280_REG_T_MSB        = 0xFA
BME280_REG_T_LSB        = 0xFB
BME280_REG_T_XLSB       = 0xFC
BME280_REG_H_MSB        = 0xFD
BME280_REG_H_LSB        = 0xFE
### Compensation Registers ###
# Temperature compensation registers
BME280_REG_DIG_T1       = 0x88  # unsigned short
BME280_REG_DIG_T2       = 0x8A  # signed short
BME280_REG_DIG_T3       = 0x8C  # signed short
# Pressure compensation registers
BME280_REG_DIG_P1       = 0x8E  # unsigned short
BME280_REG_DIG_P2       = 0x90  # signed short
BME280_REG_DIG_P3       = 0x92  # signed short
BME280_REG_DIG_P4       = 0x94  # signed short
BME280_REG_DIG_P5       = 0x96  # signed short
BME280_REG_DIG_P6       = 0x98  # signed short
BME280_REG_DIG_P7       = 0x9A  # signed short
BME280_REG_DIG_P8       = 0x9C  # signed short
BME280_REG_DIG_P9       = 0x9E  # signed short
# Humidity compensation registers
BME280_REG_DIG_H1       = 0xA1  # unsigned short
BME280_REG_DIG_H2       = 0xE1  # signed short
BME280_REG_DIG_H3       = 0xE3  # unsigned short
BME280_REG_DIG_H4       = 0xE4  # signed short
BME280_REG_DIG_H5       = 0xE5  # signed short
BME280_REG_DIG_H6       = 0xE6  # signed short
BME280_REG_DIG_H7       = 0xE7  # signed short
### Settings ###
# Oversampling of data (osrs_X)
BME280_OSRS_T_OFFSET    = 5
BME280_OSRS_T_MASK      = 0x1F
BME280_OSRS_P_OFFSET    = 2
BME280_OSRS_P_MASK      = 0xE3
BME280_OSRS_H_OFFSET    = 0
BME280_OSRS_H_MASK      = 0xF8
BME280_OSRS = {
    0:      0x00,
    1:      0x01,
    2:      0x02,
    4:      0x03,
    8:      0x04,
    16:     0x05,
}
# Sensor mode (mode)
BME280_MODE_OFFSET      = 0
BME280_MODE_MASK        = 0xFC
BME280_MODE_SLEEP       = 0
BME280_MODE_FORCED      = 1
BME280_MODE_NORMAL      = 3
# Standby-time in normal mode (t_sb)
BME280_T_SB_OFFSET      = 5
BME280_T_SB_MASK        = 0x1F
BME280_T_SB = {
    0.5:    0x00,
    62.5:   0x01,
    125:    0x02,
    250:    0x03,
    500:    0x04,
    1000:   0x05,
    10:     0x06,
    20:     0x07
}
# Time constant of the IIR filter (filter)
BME280_FILTER_OFFSET    = 2
BME280_FILTER_MASK      = 0xE3
BME280_FILTER = {
    0:      0x00,
    2:      0x01,
    4:      0x02,
    8:      0x03,
    16:     0x04
}

# 3-wire SPI interface enable (spi3w_en)
BME280_SPI2W_EN_OFFSET  = 0
BME280_SPI2W_EN_MASK    = 0xFE
BME280_SPI2W_EN_OFF     = 0
BME280_SPI2W_EN_ON      = 1
### RESET ###
BME280_RESET_VALUE      = 0xB6


#####
# @class    BME280
# @brief    BME280 environmental sensor
#
# Class for the BME280 environmental sensor.
class BME280(object):
    ###
    # The constructor.
    #
    # @param[in]    self        The object pointer.
    # @param[in]    address     Specific I2C address (default: 0x76)
    # @param[in]    busnum      Specific I2C bus number (default: 1)
    def __init__(self, address=0x76, busnum=1):
        # @var __i2c_address
        # Object's own I2C address
        self.__i2c_address = address
        # @var __bus
        # Object's own I2C bus number
        self.__bus = smbus.SMBus(busnum)
        # @var __t_fine
        # Object's own fine resolution temperature value (initially 0.0)
        self.__t_fine = 0.0

        # Load calibration values
        self._load_calibration()
        #  Disable SPI interface
        self.spi_disable()
        # Set the temperature sampling mode
        self.set_t_sample(1)
        # Set the pressure sampling mode
        self.set_p_sample(1)
        # Set the humidity sampling mode
        self.set_h_sample(1)
        # Set the standby mode
        self.set_standby(250)
        # Set the filer mode
        self.set_filter(0)
        # Set the mode of operation
        self.set_mode(BME280_MODE_NORMAL)


    ###
    # Write a byte (8-bit) to the specified I2C register.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    register        The I2C register address.
    # @param[in]    value           The byte value to be written.
    # @return       True in case of success; otherwise False.
    def _i2c_write_8(self, register, value):
        # Write the given value to the specified register
        return self.__bus.write_byte_data(self.__i2c_address, register, (value&0xFF))


    ###
    # Read an unsigned byte (8-bit) from the specified I2C register.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    register        The I2C register address.
    # @return       True in case of success; otherwise False.
    def _i2c_read_U8(self, register):
        # Read value from the specified register
        return (self.__bus.read_byte_data(self.__i2c_address, register) & 0xFF)


    ###
    # Read a signed byte (8-bit) from the specified I2C register.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    register        The I2C register address.
    # @return       Signed byte value in case of success; otherwise False.
    def _i2c_read_S8(self, register):
        # First, read value as unsigned byte
        result = self._i2c_read_U8(register)
        # Check return value
        if result is False:
            return False
        # Check for sign bit and turn into a negative value if set.
        if result & 0x80 != 0:
            result -= 1 << 8
        return result


    ###
    # Read an unsigned word (16-bit) from the specified I2C register.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    register        The I2C register address.
    # @param[in]    little_endian   Endianess of the value (true if little)
    # @return       Unsigned word value in case of success; otherwise False.
    def _i2c_read_U16(self, register, little_endian=True):
        # Read word value from the I2C register
        result = self.__bus.read_word_data(self.__i2c_address,register) & 0xFFFF
        # Check return value
        if result is False:
            return False
        # Swap bytes if using big endian
        if little_endian is False:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result


    ###
    # Read an unsigned word (16-bit; little endian) from the specified I2C register.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    register        The I2C register address.
    # @return       Unsigned word value in case of success; otherwise False.
    def _i2c_read_U16LE(self, register):
        return self._i2c_read_U16(register, little_endian=True)


    ###
    # Read a signed word (16-bit) from the specified I2C register.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    register        The I2C register address.
    # @param[in]    little_endian   Endianess of the value (true if little)
    # @return       Signed word value in case of success; otherwise False.
    def _i2c_read_S16(self, register, little_endian=True):
        # First, read the value as unsigned word
        result = self._i2c_read_U16(register, little_endian)
        # Check return value
        if result is False:
            return False
        # Check for sign bit and turn into a negative value if set.
        if result & 0x8000 != 0:
            result -= 1 << 16
        return result


    ###
    # Read a signed word (16-bit; little endian) from the specified I2C register.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    register        The I2C register address.
    # @return       Signed word value in case of success; otherwise False.
    def _i2c_read_S16LE(self, register):
        return self._i2c_read_S16(register, little_endian=True)


    ###
    # Read the chip ID.
    #
    # @param[in]    self            The object pointer.
    # @return       Chip ID in case of success; otherwise False.
    def get_chipid(self):
        return self._i2c_read_U8(BME280_REG_CHIPID)


    ###
    # Read the humidity control register.
    #
    # @param[in]    self            The object pointer.
    # @return       Humidity control register value in case of success; otherwise False.
    def get_ctrl_hum(self):
        return self._i2c_read_U8(BME280_REG_CTRL_HUM)


    ###
    # Read the status register.
    #
    # @param[in]    self            The object pointer.
    # @return       Status register value in case of success; otherwise False.
    def get_status(self):
        return self._i2c_read_U8(BME280_REG_STATUS)

    ###
    # Read the measurement control register.
    #
    # @param[in]    self            The object pointer.
    # @return       Measurement control register value in case of success; otherwise False.
    def get_ctrl_meas(self):
        return self._i2c_read_U8(BME280_REG_CTRL_MEAS)


    ###
    # Read the configuration register.
    #
    # @param[in]    self            The object pointer.
    # @return       Configuration register value in case of success; otherwise False.
    def get_config(self):
        return self._i2c_read_U8(BME280_REG_CONFIG)


    ###
    # Request a sensor reset.
    #
    # @param[in]    self            The object pointer.
    # @return       True in case of success; otherwise False.
    def reset(self):
        return self._i2c_write_8(BME280_REG_RESET, BME280_RESET_VALUE)


    ###
    # Set the sensor's mode of operation.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    mode            Mode of operation.
    # @return       True in case of success; otherwise False.
    def set_mode(self, mode):
        # Check the given value
        if (mode<BME280_MODE_SLEEP) or (mode>BME280_MODE_NORMAL):
            return False
        # Get the current register value
        reg = self.get_ctrl_meas()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_MODE_MASK) | (mode<<BME280_MODE_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CTRL_MEAS, reg)


    ###
    # Set the temperature sampling mode.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    sample          Temperature sampling mode.
    # @return       True in case of success; otherwise False.
    def set_t_sample(self, sample):
        # Check given parameter
        if sample not in BME280_OSRS:
            raise ValueError('Valid OSRS values are: 0, 1, 2, 4, 8, 16')
        # Get the current register value
        reg = self.get_ctrl_meas()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_OSRS_T_MASK) | (BME280_OSRS[sample]<<BME280_OSRS_T_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CTRL_MEAS, reg)


    ###
    # Set the pressure sampling mode.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    sample          Pressure sampling mode.
    # @return       True in case of success; otherwise False.
    def set_p_sample(self, sample):
        # Check given parameter
        if sample not in BME280_OSRS:
            raise ValueError('Valid OSRS values are: 0, 1, 2, 4, 8, 16')
        # Get the current register value
        reg = self.get_ctrl_meas()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_OSRS_P_MASK) | (BME280_OSRS[sample]<<BME280_OSRS_P_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CTRL_MEAS, reg)


    ###
    # Set the humidity sampling mode.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    sample          Humidity sampling mode.
    # @return       True in case of success; otherwise False.
    def set_h_sample(self, sample):
        # Check given parameter
        if sample not in BME280_OSRS:
            raise ValueError('Valid OSRS values are: 0, 1, 2, 4, 8, 16')
        # Get the current register value
        reg = self.get_ctrl_hum()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_OSRS_H_MASK) | (BME280_OSRS[sample]<<BME280_OSRS_H_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CTRL_HUM, reg)


    ###
    # Set the standby mode.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    stby            Standby mode.
    # @return       True in case of success; otherwise False.
    def set_standby(self, stby):
        # Check given parameter
        if stby not in BME280_T_SB:
            raise ValueError('Valid T_SB values are: 0.5, 10, 20, 62.5, 125, 250, 500, 1000')
        # Get the current register value
        reg = self.get_config()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_T_SB_MASK) | (BME280_T_SB[stby]<<BME280_T_SB_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CONFIG, reg)


    ###
    # Set the filter mode.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    filter_m        Filter mode.
    # @return       True in case of success; otherwise False.
    def set_filter(self, filter_m):
        # Check given parameter
        if filter_m not in BME280_FILTER:
            raise ValueError('Valid filter values are: 0 (off), 2, 4, 8, 16')
        # Get the current register value
        reg = self.get_config()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_FILTER_MASK) | (BME280_FILTER[filter_m]<<BME280_FILTER_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CONFIG, reg)


    ###
    # Enable the 3-wire SPI interface.
    #
    # @param[in]    self            The object pointer.
    # @return       True in case of success; otherwise False.
    def spi_enable(self):
        # Get the current register value
        reg = self.get_config()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_SPI2W_EN_MASK) | (BME280_SPI2W_EN_ON<<BME280_SPI2W_EN_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CONFIG, reg)


    ###
    # Disable the 3-wire SPI interface.
    #
    # @param[in]    self            The object pointer.
    # @return       True in case of success; otherwise False.
    def spi_disable(self):
        # Get the current register value
        reg = self.get_config()
        # Check return value
        if reg is False:
            return False
        # Prepare new register value
        reg = (reg & BME280_SPI2W_EN_MASK) | (BME280_SPI2W_EN_OFF<<BME280_SPI2W_EN_OFFSET)
        # Write the new value to the sensor
        return self._i2c_write_8(BME280_REG_CONFIG, reg)


    ###
    # Load the calibration values stored on the sensor.
    #
    # @param[in]    self            The object pointer.
    def _load_calibration(self):
        # temperature
        self.dig_T1 = self._i2c_read_U16LE(BME280_REG_DIG_T1)
        self.dig_T2 = self._i2c_read_S16LE(BME280_REG_DIG_T2)
        self.dig_T3 = self._i2c_read_S16LE(BME280_REG_DIG_T3)
        # pressure
        self.dig_P1 = self._i2c_read_U16LE(BME280_REG_DIG_P1)
        self.dig_P2 = self._i2c_read_S16LE(BME280_REG_DIG_P2)
        self.dig_P3 = self._i2c_read_S16LE(BME280_REG_DIG_P3)
        self.dig_P4 = self._i2c_read_S16LE(BME280_REG_DIG_P4)
        self.dig_P5 = self._i2c_read_S16LE(BME280_REG_DIG_P5)
        self.dig_P6 = self._i2c_read_S16LE(BME280_REG_DIG_P6)
        self.dig_P7 = self._i2c_read_S16LE(BME280_REG_DIG_P7)
        self.dig_P8 = self._i2c_read_S16LE(BME280_REG_DIG_P8)
        self.dig_P9 = self._i2c_read_S16LE(BME280_REG_DIG_P9)
        # humidity
        self.dig_H1 = self._i2c_read_U8(BME280_REG_DIG_H1)
        self.dig_H2 = self._i2c_read_S16LE(BME280_REG_DIG_H2)
        self.dig_H3 = self._i2c_read_U8(BME280_REG_DIG_H3)
        self.dig_H6 = self._i2c_read_S8(BME280_REG_DIG_H7)
        self.dig_H4 = (self._i2c_read_S8(BME280_REG_DIG_H4)<<4) | (self._i2c_read_U8(BME280_REG_DIG_H5) & 0x0F)
        self.dig_H5 = (self._i2c_read_S8(BME280_REG_DIG_H6)<<4) | (self._i2c_read_U8(BME280_REG_DIG_H5)>>4 & 0x0F)


    ###
    # Check if the sensor readings are ready.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    timeout         Timeout for waiting [ms].
    # @return       True in case of success; otherwise False.
    def wait_for_ready(self, timeout=500):
        # Time-passed counter
        passed = 0
        # Wait for conversion to complete
        while(self._i2c_read_U8(BME280_REG_STATUS) & 0x08):
            # check if timeout has already been reached
            if passed >= timeout:
                # Timeout
                return False
            # Wait for 5ms
            time.sleep(0.005)
            # increment timeout counter by 5ms
            passed += 5
        return True


    ###
    # Read the raw (uncompensated) temperature value.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    timeout         Timeout for waiting [ms].
    # @return       Raw temperature value in case of success; otherwise False.
    def _get_raw_temperature(self, timeout=500):
        # Check if the sensor readings are ready
        if self.wait_for_ready(timeout) is False:
            return False
        # Read the temperature bytes
        msb = self._i2c_read_U8(BME280_REG_T_MSB)
        lsb = self._i2c_read_U8(BME280_REG_T_LSB)
        xlsb = self._i2c_read_U8(BME280_REG_T_XLSB)
        # Check return values
        if (msb is False) or (lsb is False) or (xlsb is False):
            return False
        # Return the raw temperature value
        return (((msb << 16) | (lsb << 8) | xlsb) >> 4)

    ###
    # Read the raw (uncompensated) pressure value.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    timeout         Timeout for waiting [ms].
    # @return       Raw pressure value in case of success; otherwise False.
    def _get_raw_pressure(self):
        # Check if the sensor readings are ready
        if self.wait_for_ready(timeout) is False:
            return False
        # Read the pressure bytes
        msb = self._i2c_read_U8(BME280_REG_P_MSB)
        lsb = self._i2c_read_U8(BME280_REG_P_LSB)
        xlsb = self._i2c_read_U8(BME280_REG_P_XLSB)
        # Check return values
        if (msb is False) or (lsb is False) or (xlsb is False):
            return False
        # Return the raw pressure value
        return (((msb << 16) | (lsb << 8) | xlsb) >> 4)


    ###
    # Read the raw (uncompensated) humidity value.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    timeout         Timeout for waiting [ms].
    # @return       Raw humidity value in case of success; otherwise False.
    def _get_raw_humidity(self):
        # Check if the sensor readings are ready
        if self.wait_for_ready(timeout) is False:
            return False
        # Read the humidity bytes
        msb = self._i2c_read_U8(BME280_REG_H_MSB)
        lsb = self._i2c_read_U8(BME280_REG_H_LSB)
        # Check return values
        if (msb is False) or (lsb is False):
            return False
        # Return the raw humidity value
        return ((msb << 8) | lsb)


    ###
    # Read the compensated temperature value (degree Celsius).
    #
    # @param[in]    self            The object pointer.
    # @return       Temperature value [°C] in case of success; otherwise False.
    def read_temperature(self):
        # Get the raw temperature reading
        raw = self._get_raw_temperature()
        # Check return value
        if raw is False:
            return False
        # Calculate the compensated temperature value (see datasheet 8.2)
        var1 = ((((raw>>3) - (self.dig_T1<<1))) * (self.dig_T2)) >> 11
        var2 = (((((raw>>4) - (self.dig_T1)) * ((raw>>4) - (self.dig_T1))) >> 12) * (self.dig_T3)) >> 14
        # Calculate the fine resolution temperature value
        self.__t_fine = var1 + var2
        # Calculate and return the compensated value
        return ((self.__t_fine * 5 + 128) >> 8) / 100.0


    ###
    # Read the compensated pressure value (hectopascal).
    #
    # @param[in]    self            The object pointer.
    # @return       Pressure value [hPa] in case of success; otherwise False.
    def read_pressure(self):
        # Get the raw temperature reading
        raw = self._get_raw_pressure()
        # Check return value
        if raw is False:
            return False
        # Check if the fine resolution temperature value is not set yet
        if (self.__t_fine==0.0):
            # Perform temperature measurement to update the __t_fine value
            self.get_temperature()
        # Calculate the compensated pressure value (see datasheet 8.2)
        var1 = ((self.__t_fine)>>1) - 64000
        var2 = (((var1>>2) * (var1>>2)) >> 11 ) * (self.dig_P6)
        var2 = var2 + ((var1*(self.dig_P5))<<1)
        var2 = (var2>>2) + ((self.dig_P4)<<16)
        var1 = (((self.dig_P3 * (((var1>>2) * (var1>>2)) >> 13 )) >> 3) + (((self.dig_P2) * var1) >> 1)) >> 18
        var1 = ((((32768+var1)) * (self.dig_P1)) >> 15)
        # Avoid division by zero
        if var1==0:
            return False 
        p = (((1048576-raw) - (var2>>12))) * 3125
        if p<0x80000000:
            p = int((p << 1) / var1)
        else:
            p = int((p / var1) * 2)
        var1 = ((self.dig_P9) * (((p>>3) * (p>>3))>>13))>>12
        var2 = ((p>>2) * self.dig_P8)>>13
        # Return the resulting pressure in hPa
        return (p + ((var1 + var2 + self.dig_P7) >> 4)) / 100.0


    ###
    # Read the compensated humidity value (% RH).
    #
    # @param[in]    self            The object pointer.
    # @return       Humidity value [% RH] in case of success; otherwise False.
    def read_humidity(self):
        # Get the raw humidity reading
        raw = self._get_raw_humidity()
        # Check return value
        if raw is False:
            return False
        # Check if the fine resolution temperature value is not set yet
        if (self.__t_fine==0.0):
            # Perform temperature measurement to update the __t_fine value
            self.get_temperature()
        # Calculate the compensated humidity value (see datasheet)
        humidity = float(self.__t_fine) - 76800.0
        humidity = (float(raw) - (float(self.dig_H4) * 64.0 + float(self.dig_H5) / 16384.0 * humidity)) * (float(self.dig_H2) / 65536.0 * (1.0 + float(self.dig_H6) / 67108864.0 * humidity * (1.0 + float(self.dig_H3) / 67108864.0 * humidity)))
        humidity = humidity * (1.0 - float(self.dig_H1) * humidity / 524288.0)
        # Limit the value
        if humidity > 100:
            humidity = 100
        elif humidity < 0:
            humidity = 0
        # Return the resulting value
        return humidity


    ###
    # Calculate the dewpoint in °C (only accurate at >50% RH).
    #
    # @param[in]    self            The object pointer.
    # @return       Dewpoint value [°C] in case of success; otherwise False.
    def read_dewpoint(self):
        # Read temperature value
        celsius = self.get_temperature()
        # Read humidity value
        humidity = self.get_humidity()
        # Check return value
        if (celsius is False) or (humidity is False):
            return False
        # Return the dew-point
        return (celsius - ((100 - humidity) / 5))
