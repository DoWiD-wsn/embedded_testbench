#!/usr/bin/env python3

########################################################################
#   BME280 Environmental Sensor                                        #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-11-03                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     bme = BME280()                                                   #
#     or                                                               #
#     bme = BME280(0x76)        # address                              #
#     or                                                               #
#     bme = BME280(0x76, 1)     # address & busnum                     #
#     then                                                             #
#     bme.read_temperature()                                           #
#     bme.read_pressure()                                              #
#     bme.read_humidity()                                              #
#     bme.read_dewpoint()                                              #
#                                                                      #
#   Based on:                                                          #
#   https://github.com/adafruit/Adafruit_Python_BME280/                #
#   https://github.com/adafruit/Adafruit_Python_GPIO/                  #
#                                                                      #
#   See also:                                                          #
#   https://github.com/rm-hull/bme280                                  #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# sleep functionality
from time import sleep
# I2C functionality
import smbus


##### Register Values #####
### REGISTER ADDRESSES ###
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

### TEMPERATURE ###
BME280_REG_DIG_T1       = 0x88
BME280_REG_DIG_T2       = 0x8A
BME280_REG_DIG_T3       = 0x8C
### PRESSURE ###
BME280_REG_DIG_P1       = 0x8E
BME280_REG_DIG_P2       = 0x90
BME280_REG_DIG_P3       = 0x92
BME280_REG_DIG_P4       = 0x94
BME280_REG_DIG_P5       = 0x96
BME280_REG_DIG_P6       = 0x98
BME280_REG_DIG_P7       = 0x9A
BME280_REG_DIG_P8       = 0x9C
BME280_REG_DIG_P9       = 0x9E
### HUMIDITY ###
BME280_REG_DIG_H1       = 0xA1
BME280_REG_DIG_H2       = 0xE1
BME280_REG_DIG_H3       = 0xE3
BME280_REG_DIG_H4       = 0xE4
BME280_REG_DIG_H5       = 0xE5
BME280_REG_DIG_H6       = 0xE6
BME280_REG_DIG_H7       = 0xE7

##### SETTINGS #####
### SAMPLING MODES ###
BME280_SAMPLE_NONE      = 0
BME280_SAMPLE_1         = 1
BME280_SAMPLE_2         = 2
BME280_SAMPLE_4         = 3
BME280_SAMPLE_8         = 4
BME280_SAMPLE_16        = 5
### OPERATING MODES ###
BME280_MODE_SLEEP       = 0
BME280_MODE_FORCED      = 1
BME280_MODE_NORMAL      = 3
### STANDBY SETTINGS ###
BME280_STANDBY_0_5      = 0
BME280_STANDBY_62_5     = 1
BME280_STANDBY_125      = 2
BME280_STANDBY_250      = 3
BME280_STANDBY_500      = 4
BME280_STANDBY_1000     = 5
BME280_STANDBY_10       = 6
BME280_STANDBY_20       = 7
### FILTER SETTINGS ###
BME280_FILTER_OFF       = 0
BME280_FILTER_2         = 1
BME280_FILTER_4         = 2
BME280_FILTER_8         = 3
BME280_FILTER_16        = 4
### SPI SETTINGS ###
BME280_SPI_OFF          = 0
BME280_SPI_ON           = 1
### RESET ###
BME280_RESET_VALUE      = 0xB6


##### BME280 CLASS ###################
class BME280(object):
    # Constructor
    def __init__(self, address=0x76, busnum=1):
        # Set the sensor configuration 
        self._address = address
        self._bus = smbus.SMBus(busnum)
        # Load calibration values
        self._load_calibration()
        #  Disable SPI interface
        self.spi_disable()
        # Set the temperature sampling mode
        self.set_t_sample(BME280_SAMPLE_1)
        # Set the pressure sampling mode
        self.set_p_sample(BME280_SAMPLE_1)
        # Set the humidity sampling mode
        self.set_h_sample(BME280_SAMPLE_1)
        # Set the standby mode
        self.set_standby(BME280_STANDBY_250)
        # Set the filer mode
        self.set_filter(BME280_FILTER_OFF)
        # Set the mode of operation
        self.set_mode(BME280_MODE_NORMAL)
        # Set the initial t_fine value to 0.0
        self.t_fine = 0.0


    ##### I2C READ/WRITE #####

    # Write an 8-bit value to the specified register
    def write8(self, register, value):
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value)

    # Read a length number of bytes from the specified register (as bytearray)
    def readList(self, register, length):
        return self._bus.read_i2c_block_data(self._address, register, length)

    # Read an unsigned byte from the specified register
    def readU8(self, register):
        return (self._bus.read_byte_data(self._address, register) & 0xFF)

    # Read a signed byte from the specified register
    def readS8(self, register):
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    # Read an unsigned 16-bit value from the specified register
    def readU16(self, register, little_endian=True):
        result = self._bus.read_word_data(self._address,register) & 0xFFFF
        # Swap bytes if using big endian
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    # Read a signed 16-bit value from the specified register
    def readS16(self, register, little_endian=True):
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    # Read an unsigned 16-bit value from the specified register (little endian)
    def readU16LE(self, register):
        return self.readU16(register, little_endian=True)

    # Read a signed 16-bit value from the specified register (little endian)
    def readS16LE(self, register):
        return self.readS16(register, little_endian=True)


    ##### CONFIGURATION - READ #####

    # Read the chip ID
    def get_chipid(self):
        # Return the value from the sensor
        return self.readU8(BME280_REG_CHIPID)

    # Read the humidity-control register
    def get_ctrl_hum(self):
        # Return the value from the sensor
        return self.readU8(BME280_REG_CTRL_HUM)

    # Read the status register
    def get_status(self):
        # Return the value from the sensor
        return self.readU8(BME280_REG_STATUS)

    # Read the measurement control register
    def get_ctrl_meas(self):
        # Return the value from the sensor
        return self.readU8(BME280_REG_CTRL_MEAS)

    # Read the configuration register
    def get_config(self):
        # Return the value from the sensor
        return self.readU8(BME280_REG_CONFIG)


    ##### CONFIGURATION - WRITE #####

    # Perform a sensor reset
    def reset(self):
        # Write the value to the sensor
        self.write8(BME280_REG_RESET, BME280_RESET_VALUE)

    # Set the mode of operation
    def set_mode(self, value):
        # Set the value in the sensor configuration
        self.mode = value
        # Get the current register value
        reg = self.get_ctrl_meas()
        # Prepare new register value
        reg = (reg & 0xFC) | (value<<0)
        # Write the new value to the sensor
        self.write8(BME280_REG_CTRL_MEAS, reg)

    # Set the temperature sampling mode
    def set_t_sample(self, value):
        # Set the value in the sensor configuration
        self.t_sample = value
        # Get the current register value
        reg = self.get_ctrl_meas()
        # Prepare new register value
        reg = (reg & 0x1F) | (value<<5)
        # Write the new value to the sensor
        self.write8(BME280_REG_CTRL_MEAS, reg)

    # Set the pressure sampling mode
    def set_p_sample(self, value):
        # Set the value in the sensor configuration
        self.p_sample = value
        # Get the current register value
        reg = self.get_ctrl_meas()
        # Prepare new register value
        reg = (reg & 0xE3) | (value<<2)
        # Write the new value to the sensor
        self.write8(BME280_REG_CTRL_MEAS, reg)

    # Set the humidity sampling mode
    def set_h_sample(self, value):
        # Set the value in the sensor configuration
        self.h_sample = value
        # Get the current register value
        reg = self.get_ctrl_hum()
        # Prepare new register value
        reg = (reg & 0xF8) | value
        # Write the new value to the sensor
        self.write8(BME280_REG_CTRL_HUM, reg)

    # Set the standby mode
    def set_standby(self, value):
        # Set the value in the sensor configuration
        self.standby = value
        # Get the current register value
        reg = self.get_config()
        # Prepare new register value
        reg = (reg & 0x1F) | (value<<5)
        # Write the new value to the sensor
        self.write8(BME280_REG_CONFIG, reg)

    # Set the filter mode
    def set_filter(self, value):
        # Set the value in the sensor configuration
        self.filter = value
        # Get the current register value
        reg = self.get_config()
        # Prepare new register value
        reg = (reg & 0xE3) | (value<<2)
        # Write the new value to the sensor
        self.write8(BME280_REG_CONFIG, reg)

    # Enable the SPI interface
    def spi_enable(self):
        # Get the current register value
        reg = self.get_config()
        # Prepare new register value
        reg = (reg & 0xFE) | BME280_SPI_ON
        # Write the new value to the sensor
        self.write8(BME280_REG_CONFIG, reg)

    # Disable the SPI interface
    def spi_disable(self):
        # Get the current register value
        reg = self.get_config()
        # Prepare new register value
        reg = (reg & 0xFE) | BME280_SPI_OFF
        # Write the new value to the sensor
        self.write8(BME280_REG_CONFIG, reg)


    ##### SENSOR READINGS #####

    # Read the compensated temperature value (degree Celsius)
    def get_temperature(self):
        # Get the raw temperature reading
        raw = self.get_temperature_raw()
        # Calculate the compensated temperature value (see datasheet 8.2)
        var1 = ((((raw>>3) - (self.dig_T1<<1))) * (self.dig_T2)) >> 11
        var2 = (((((raw>>4) - (self.dig_T1)) * ((raw>>4) - (self.dig_T1))) >> 12) * (self.dig_T3)) >> 14
        # Calculate the fine resolution temperature value
        self.t_fine = var1 + var2
        # Calculate and return the resulting value
        return ((self.t_fine * 5 + 128) >> 8) / 100.0

    # Read the compensated pressure level (hectopascal)
    def get_pressure(self):
        # Get the raw temperature reading
        raw = self.get_pressure_raw()
        # Perform temperature measurement to update the t_fine value
        self.get_temperature()
        # Calculate the compensated pressure value (see datasheet 8.2)
        var1 = ((self.t_fine)>>1) - 64000
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
            p = (p << 1) / var1
        else:
            p = (p / var1) * 2
        p = int(p)
        var1 = ((self.dig_P9) * (((p>>3) * (p>>3))>>13))>>12
        var2 = ((p>>2) * self.dig_P8)>>13
        # Return the resulting pressure in hPa
        return (p + ((var1 + var2 + self.dig_P7) >> 4)) / 100.0

    # Read the compensated humidity value
    def get_humidity(self):
        # Get the raw humidity reading
        raw = self.get_humidity_raw()
        # Perform temperature measurement to update the t_fine value
        self.get_temperature()
        # Calculate the compensated humidity value (see datasheet)
        humidity = float(self.t_fine) - 76800.0
        humidity = (float(raw) - (float(self.dig_H4) * 64.0 + float(self.dig_H5) / 16384.0 * humidity)) * (float(self.dig_H2) / 65536.0 * (1.0 + float(self.dig_H6) / 67108864.0 * humidity * (1.0 + float(self.dig_H3) / 67108864.0 * humidity)))
        humidity = humidity * (1.0 - float(self.dig_H1) * humidity / 524288.0)
        # Check for value limits
        if humidity > 100:
            humidity = 100
        elif humidity < 0:
            humidity = 0
        # Return the resulting value
        return humidity

    # Return calculated dewpoint in C, only accurate at > 50% RH
    def get_dewpoint(self):
        # Read temperature value
        celsius = self.get_temperature()
        # Read humidity value
        humidity = self.get_humidity()
        # Return the dew-point
        return (celsius - ((100 - humidity) / 5))


    ##### CALIBRATION #####
    
    # Load the stored calibration values
    def _load_calibration(self):
        # temperature
        self.dig_T1 = self.readU16LE(BME280_REG_DIG_T1)
        self.dig_T2 = self.readS16LE(BME280_REG_DIG_T2)
        self.dig_T3 = self.readS16LE(BME280_REG_DIG_T3)
        # pressure
        self.dig_P1 = self.readU16LE(BME280_REG_DIG_P1)
        self.dig_P2 = self.readS16LE(BME280_REG_DIG_P2)
        self.dig_P3 = self.readS16LE(BME280_REG_DIG_P3)
        self.dig_P4 = self.readS16LE(BME280_REG_DIG_P4)
        self.dig_P5 = self.readS16LE(BME280_REG_DIG_P5)
        self.dig_P6 = self.readS16LE(BME280_REG_DIG_P6)
        self.dig_P7 = self.readS16LE(BME280_REG_DIG_P7)
        self.dig_P8 = self.readS16LE(BME280_REG_DIG_P8)
        self.dig_P9 = self.readS16LE(BME280_REG_DIG_P9)
        # humidity
        self.dig_H1 = self.readU8(BME280_REG_DIG_H1)
        self.dig_H2 = self.readS16LE(BME280_REG_DIG_H2)
        self.dig_H3 = self.readU8(BME280_REG_DIG_H3)
        self.dig_H6 = self.readS8(BME280_REG_DIG_H7)
        h4 = self.readS8(BME280_REG_DIG_H4)
        h4 = (h4 << 4)
        self.dig_H4 = h4 | (self.readU8(BME280_REG_DIG_H5) & 0x0F)
        h5 = self.readS8(BME280_REG_DIG_H6)
        h5 = (h5 << 4)
        self.dig_H5 = h5 | (
        self.readU8(BME280_REG_DIG_H5) >> 4 & 0x0F)


    ##### RAW READING #####
    
    # Check if the BME280 sensor readings are ready
    def wait_for_ready(self, timeout=500):
        # Wait for conversion to complete
        time_cnt=0
        while(self.readU8(BME280_REG_STATUS) & 0x08):
            # Wait for 2ms
            sleep(0.002)
            # Increment timeout counter
            time_cnt = time_cnt + 1
            # Check if timeout has been reached
            if time_cnt > timeout:
                return False
        return True
    
    # Read the raw (uncompensated) temperature value
    def get_temperature_raw(self, timeout=500):
        # Check if the sensor readings are ready
        if not self.wait_for_ready():
            return False
        # Read in temperature bytes
        MSB = self.readU8(BME280_REG_T_MSB)
        LSB = self.readU8(BME280_REG_T_LSB)
        XLSB = self.readU8(BME280_REG_T_XLSB)
        # Return the raw temperature value
        return (((MSB << 16) | (LSB << 8) | XLSB) >> 4)

    # Read the raw (uncompensated) pressure level
    def get_pressure_raw(self):
        # Check if the sensor readings are ready
        if not self.wait_for_ready():
            return False
        # Read in pressure bytes
        MSB = self.readU8(BME280_REG_P_MSB)
        LSB = self.readU8(BME280_REG_P_LSB)
        XLSB = self.readU8(BME280_REG_P_XLSB)
        # Return the raw pressure value
        return (((MSB << 16) | (LSB << 8) | XLSB) >> 4)

    # Read the raw (uncompensated) humidity value
    def get_humidity_raw(self):
        # Check if the sensor readings are ready
        if not self.wait_for_ready():
            return False
        # Read in humidity bytes
        MSB = self.readU8(BME280_REG_H_MSB)
        LSB = self.readU8(BME280_REG_H_LSB)
        # Return the raw humidity value
        return ((MSB << 8) | LSB)
