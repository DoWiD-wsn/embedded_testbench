#####
# @brief   SHTC3 temperature and humidity sensor
#
# Module containing the SHTC3 temperature and humidity sensor class.
#
# @file     /etb/sens/SHTC3.py
# @author   Dominik Widhalm
# @version  1.0 
# @date     2021-04-02
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @see      https://github.com/adafruit/Adafruit_CircuitPython_SHTC3/blob/main/adafruit_shtc3.py
#
# @example  shtc3 = SHTC3()                 # Get an instance with default I2C address (0x70)
# @example  temp = shtc3.read_temperature() # Read the current temperature [°C]
# @example  humi = shtc3.read_humidity()    # Read the current relative humidity [%]
# @example  (temp,humi) = shtc3.read_temperature_humidity()    # Read both
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus
# time (for sleep method)
import time


##### GLOBAL VARIABLES #####
### Sensor specific ###
# Delay after requesting the sensor to wake-up [ms] #
SHTC3_WAKEUP_DELAY                      = 1
# Delay for measurement poling [ms] #
SHTC3_POLLING_DELAY                     = 50
# CRC polynomial: P(x) = x^8 + x^5 + x^4 + 1 = 100110001 #
SHTC3_CRC_POLYNOMIAL                    = 0x131

### Measurement setting ###
# Measure RH before T (default: 0) #
SHTC3_RH_FIRST                          = 0

### I2C commands ###
# Read ID register #
SHTC3_COM_READID                        = 0xEFC8
# Soft reset #
SHTC3_COM_SOFT_RESET                    = 0x805D
# Sleep #
SHTC3_COM_SLEEP                         = 0xB098
# Wakeup #
SHTC3_COM_WAKEUP                        = 0x3517

### Measurement commands ###
# Measure T->RH with polling (normal mode) #
SHTC3_COM_MEAS_TRH_POL_NORM             = 0x7866
# Measure T->RH with clock stretching (normal mode) #
SHTC3_COM_MEAS_TRH_CST_NORM             = 0x7CA2
# Measure RH->T with polling (normal mode) #
SHTC3_COM_MEAS_RHT_POL_NORM             = 0x58E0
# Measure RH->T with clock stretching (normal mode) #
SHTC3_COM_MEAS_RHT_CST_NORM             = 0x5C24
# Measure T->RH with polling (low-power mode) #
SHTC3_COM_MEAS_TRH_POL_LPOW             = 0x609C
# Measure T->RH with clock stretching (low-power mode) #
SHTC3_COM_MEAS_TRH_CST_LPOW             = 0x6458
# Measure RH->T with polling (low-power mode) #
SHTC3_COM_MEAS_RHT_POL_LPOW             = 0x401A
# Measure RH->T with clock stretching (low-power mode) #
SHTC3_COM_MEAS_RHT_CST_LPOW             = 0x44DE

### Actual read command depends on settings ###
# Low-power mode #
if SHTC3_RH_FIRST:
    SHTC3_COM_MEAS_LPOW                 = SHTC3_COM_MEAS_RHT_POL_LPOW
else:
    SHTC3_COM_MEAS_LPOW                 = SHTC3_COM_MEAS_TRH_POL_LPOW
# Normal mode #
if SHTC3_RH_FIRST:
    SHTC3_COM_MEAS_NORM                 = SHTC3_COM_MEAS_RHT_POL_NORM
else:
    SHTC3_COM_MEAS_NORM                 = SHTC3_COM_MEAS_TRH_POL_NORM


#####
# @class    SHTC
# @brief    SHTC3 temperature and humidity sensor
#
# Class for the SHTC3 temperature and humidity sensor.
class SHTC3(object):
    ###
    # The constructor.
    #
    # @param    self        The object pointer.
    # @param    address     Specific I2C address (default: 0x70)
    # @param    busnum      Specific I2C bus number (default: 1)
    def __init__(self, address=0x70, busnum=1):
        # @var __i2c_address
        # Object's own I2C address
        self.__i2c_address = address
        # @var __bus
        # Object's own I2C bus number
        self.__bus = smbus.SMBus(busnum)
        # Wake up the device in case it was sleeping
        self.sleep_disable()


    ###
    # Read 16-bit from the SHTC3 sensor and perform CRC check.
    #
    # @param    self        The object pointer.
    # @return   16-bit value in case of success; False otherwise
    ###
    def read16_crc(self):
        # Read two data bytes and one checksum byte
        data = [0, 0]
        data[0]  = self.__bus.read_byte(self.__i2c_address)
        data[1]  = self.__bus.read_byte(self.__i2c_address)
        checksum = self.__bus.read_byte(self.__i2c_address)
        # Verify checksum
        if self.check_crc(data, 2, checksum) is False:
            return False
        # Combine the two bytes and return the 16-bit value
        return (data[0] << 8) | data[1]


    ###
    # Perform a CRC check.
    #
    # @param    self        The object pointer.
    # @param    data        Input data to be checked
    # @param    cnt         Number of bytes to be checked
    # @param    checksum    Received CRC checksum
    # @return   True in case of success; False otherwise
    ###
    def check_crc(self, data, cnt, checksum):
        # Calculated checksum initial value
        crc = 0xFF;
        # Calculate CRC with given polynomial
        for i in range(cnt):
            crc ^= data[i]
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ SHTC3_CRC_POLYNOMIAL
                else:
                    crc = crc << 1
        # Take the bottom 8 bits
        crc &= 0xFF
        # Verify checksum
        if (crc != checksum):
            return False
        else:
            return True


    ###
    # Soft-reset the sensor.
    #
    # @param    self        The object pointer.
    # @return   True in case of success; False otherwise
    ###
    def reset(self):
        # Write soft-reset command
        self.__bus.write_byte_data(self.__i2c_address,(SHTC3_COM_SOFT_RESET>>8),(SHTC3_COM_SOFT_RESET&0xFF))
        # Return True
        return True


    ###
    # Read the SHTC3 sensor's ID.
    #
    # @param    self        The object pointer.
    # @return   ID in case of success; False otherwise
    ###
    def read_id(self):
        # Write ID read command
        self.__bus.write_byte_data(self.__i2c_address,(SHTC3_COM_READID>>8),(SHTC3_COM_READID&0xFF))
        # Read two bytes and perform CRC check
        value = self.read16_crc()
        if value is False:
            return False
        else:
            return value


    ###
    # Request the SHTC3 sensor to sleep.
    # 
    # @param    self        The object pointer.
    # @return   True in case of success; False otherwise
    ###
    def sleep_enable(self):
        # Write soft-reset command
        self.__bus.write_byte_data(self.__i2c_address,(SHTC3_COM_SLEEP>>8),(SHTC3_COM_SLEEP&0xFF))
        # Return True
        return True


    ###
    # Request the SHTC3 sensor to wake-up.
    #
    # @param    self        The object pointer.
    # @return   True in case of success; False otherwise
    ###
    def sleep_disable(self):
        # Write soft-reset command
        self.__bus.write_byte_data(self.__i2c_address,(SHTC3_COM_WAKEUP>>8),(SHTC3_COM_WAKEUP&0xFF))
        # Return True
        return True


    ###
    # Convert a raw temperature to degrees Celsius.
    # T = -45 + 175 * raw / 2^16
    #
    # @param    self        The object pointer.
    # @param    raw         Raw temperature reading
    # @return   Resulting temperature in degrees Celsius
    ###
    def raw2temperature(self, raw):
      # Calculate resulting temperature [°C]
      return (175.0 * (float(raw) / 65536.0) - 45.0)


    ###
    # Convert a raw humidity to percent relative humidity.
    # RH = raw / 2^16 * 100
    #
    # @param    self        The object pointer.
    # @param    raw         Raw humidity reading
    # @return   Resulting humidity in percent relative humidity
    ###
    def raw2humidity(self, raw):
      # Calculate resulting relative humidity [%RH]
      return (100.0 * (float(raw) / 65536.0))


    ###
    # Read both temperature and humidity from the sensor.
    #
    # @param    dev             Pointer to the device structure
    # @param    lp_en           Enable low-power mode (1..enabled/0..disabled)
    # @return   Values read in case of success; False otherwise
    ###
    def read_temperature_humidity(self, lp_en):
        # Measurement command depends on mode setting
        cmd_meas = lp_en if SHTC3_COM_MEAS_LPOW else SHTC3_COM_MEAS_NORM
        # Write read command
        self.__bus.write_byte_data(self.__i2c_address,(cmd_meas>>8),(cmd_meas&0xFF))
        # Wait for the measurement to be ready
        time.sleep(SHTC3_POLLING_DELAY/1000)
        # Read the measurements
        temp_raw = 0
        humid_raw = 0
        if SHTC3_RH_FIRST:
            # Read two humidty bytes and perform CRC check
            humid_raw = self.read16_crc()
            # Read two temperature bytes and perform CRC check
            temp_raw = self.read16_crc()
        else:
            # Read two temperature bytes and perform CRC check
            temp_raw = self.read16_crc()
            # Read two humidty bytes and perform CRC check
            humid_raw = self.read16_crc()
        # Check if CRC was successful
        if (temp_raw is False) or (humid_raw is False):
            return False
        # Calculate temperature in °C and humidity in %RH
        temperature = self.raw2temperature(temp_raw)
        humidity = self.raw2humidity(humid_raw)
        # Return values
        return (temperature, humidity)


    ###
    # Read the temperature in degree Celsius (°C) from the sensor.
    # 
    # @param    dev             Pointer to the device structure
    # @param    lp_en           Enable low-power mode (1..enabled/0..disabled)
    # @return   Value read in case of success; False otherwise
    ###
    def read_temperature(self, lp_en):
        # Call reading function
        (temperature, humidity) = self.get_temperature_humidity(lp_en)
        # Return the temperature
        return temperature


    ###
    # Read the relative humidity (%RH) from the sensor.
    # 
    # @param    dev             Pointer to the device structure
    # @param    lp_en           Enable low-power mode (1..enabled/0..disabled)
    # @return   Value read in case of success; False otherwise
    ###
    def read_humidity(self, lp_en):
        # Call reading function
        (temperature, humidity) = self.get_temperature_humidity(lp_en)
        # Return the humidity
        return humidity
