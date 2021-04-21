#####
# @brief   LM75 temperature sensor
#
# Module containing the LM75 temperature sensor class.
#
# @file     /etb/sens/LM75.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/08 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
#
# @example  lm75 = LM75()                  # Get an instance with default I2C address (0x48)
# @example  temp = lm75.read_temperature() # Read the current temperature [°C]
#####


##### LIBRARIES #####
# smbus (provides subset of I2C functionality)
import smbus


##### GLOBAL VARIABLES #####
# Register addresses
LM75_REG_TEMP           = 0x00
LM75_REG_CONF           = 0x01
LM75_REG_HYST           = 0x02
LM75_REG_OS             = 0x03
### Configuration ###
# Shutdown
LM75_CONF_SHDN_OFFSET   = 0
# Comparator/interrupt
LM75_CONF_COMP_OFFSET   = 1
# OS polarity
LM75_CONF_POL_OFFSET    = 2
# Fault queue
LM75_CONF_QUEUE_OFFSET  = 3
LM75_CONF_QUEUE_MASK    = 0x18
LM75_CONF_QUEUE = {
    1:  0x00,
    2:  0x01,
    4:  0x02,
    6:  0x03
}


#####
# @class    LM75
# @brief    LM75 temperature sensor
#
# Class for the LM75 temperature sensor.
class LM75(object):
    ###
    # The constructor.
    #
    # @param[in] self The object pointer.
    # @param[in] address specific I2C address (default: 0x48)
    # @param[in] busnum specific I2C bus number (default: 1)
    def __init__(self, address=0x48, busnum=1):
        # @var __i2c_address
        # Objects own I2C address
        self.__i2c_address = address
        # @var __bus
        # Objects own I2C bus number
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
    # Read an unsigned word (16-bit) from the specified I2C register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[in] little_endian Endianess of the value (true if little)
    # @param[out] Unsigned word value in case of success; otherwise False.
    def _i2c_read_U16(self, register, little_endian=True):
        # Read word value from the I2C register
        result = self.__bus.read_word_data(self.__i2c_address,register) & 0xFFFF
        # Swap bytes if using big endian
        if little_endian is False:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result


    ###
    # Read a signed word (16-bit) from the specified I2C register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[in] little_endian Endianess of the value (true if little)
    # @param[out] Signed word value in case of success; otherwise False.
    def _i2c_read_S16(self, register, little_endian=True):
        # First, read the value as unsigned word
        result = self._i2c_read_U16(register, little_endian)
        # Check for sign bit and turn into a negative value if set.
        if result & 0x8000 != 0:
            result -= 1 << 16
        return result


    ###
    # Read a signed word (16-bit; big endian) from the specified I2C register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[out] Signed word value in case of success; otherwise False.
    def _i2c_read_S16BE(self, register):
        return self._i2c_read_S16(register, little_endian=False)


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
    # Write a word (16-bit) to the specified I2C register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[in] value The byte value to be written.
    # @param[in] little_endian Endianess of the value (true if little)
    # @param[out] True in case of success; otherwise False.
    def _i2c_write_16(self, register, value, little_endian=True):
        # Swap bytes if using big endian
        if little_endian is False:
            value = ((value << 8) & 0xFF00) + (value >> 8)
        # Write the given value to the specified register
        self.__bus.write_word_data(self.__i2c_address, register, value)


    ###
    # Write a word (16-bit; big endian) to the specified I2C register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[in] value The byte value to be written.
    # @param[out] True in case of success; otherwise False.
    def _i2c_write_16BE(self, register, value):
        return self._i2c_write_16(register, value, False)


    ###
    # Read the configuration register.
    #
    # @param[in] self The object pointer.
    # @param[out] Configuration register value in case of success; otherwise False.
    def get_config(self):
        return self._i2c_read_U8(LM75_REG_CONF)


    ###
    # Read the configuration register flags.
    #
    # @param[in] self The object pointer.
    # @param[out] Configuration register flags (list) in case of success; otherwise False.
    def get_config_flags(self):
        # Read the config register
        ret = self.get_config()
        if ret is False:
            return False
        # Extract the single flags
        SHUTDOWN = 1 if(ret & (1 << LM75_CONF_SHDN_OFFSET)) else 0
        COMP     = 1 if(ret & (1 << LM75_CONF_COMP_OFFSET)) else 0
        POL      = 1 if(ret & (1 << LM75_CONF_POL_OFFSET)) else 0
        QUEUE    = (ret & LM75_CONF_QUEUE_MASK) >> LM75_CONF_QUEUE_OFFSET
        # Return the flag values
        return (SHUTDOWN,COMP,POL,QUEUE)


    ###
    # Read the temperature value from a given register.
    #
    # @param[in] self The object pointer.
    # @param[in] register The I2C register address.
    # @param[out] Temperature value in case of success; otherwise False.
    def _get_raw_temperature(self, register):
        # Read the temperature register value as signed integer (big endian)
        raw = self._i2c_read_S16BE(register)
        # Convert word to float
        return (raw / 32.0) / 8.0


    ###
    # Read the sensor temperature value.
    #
    # @param[in] self The object pointer.
    # @param[out] Sensor temperature value in case of success; otherwise False.
    def read_temperature(self):
        return self._get_raw_temperature(LM75_REG_TEMP)


    ###
    # Read the hysteresis temperature value.
    #
    # @param[in] self The object pointer.
    # @param[out] Hysteresis temperature value in case of success; otherwise False.
    def read_temperature_hyst(self):
        return self._get_raw_temperature(LM75_REG_HYST)


    ###
    # Read the overtemperature shutdown temperature value.
    #
    # @param[in] self The object pointer.
    # @param[out] Overtemperature shutdown temperature value in case of success; otherwise False.
    def read_temperature_os(self):
        return self._get_raw_temperature(LM75_REG_OS)


    ###
    # Set the configuration register.
    #
    # @param[in] self The object pointer.
    # @param[in] value Configuration register value.
    # @param[out] True in case of success; otherwise False.
    def set_config(self,value):
        return self._i2c_write_8(LM75_REG_CONF, value)


    ###
    # Set the configuration register flags.
    #
    # @param[in] self The object pointer.
    # @param[in] SHDN Shutdown flag.
    # @param[in] COMP Comparator flag.
    # @param[in] POL Polarity flag.
    # @param[in] QUEUE Queue flags.
    # @param[out] True in case of success; otherwise False.
    def set_config_flags(self,SHDN,COMP,POL,QUEUE):
        # Check the given value
        if(SHDN<0) or (SHDN>1):
            return False
        if(COMP<0) or (COMP>1):
            return False
        if(POL<0) or (POL>1):
            return False
        if QUEUE not in LM75_CONF_QUEUE:
            raise ValueError('Valid QUEUE values are: 1, 2, 4, or 6')
        # Get the resulting configuration
        config = (SHDN << LM75_CONF_SHDN_OFFSET) | (COMP << LM75_CONF_COMP_OFFSET) | (POL << LM75_CONF_POL_OFFSET) | (QUEUE << LM75_CONF_QUEUE_OFFSET)
        # Write the byte to the register
        return self.set_config(config)


    ###
    # Set the value of a given temperature register.
    #
    # @param[in] self The object pointer.
    # @param[in] value Configuration register value.
    # @param[in] register The I2C register address.
    # @param[out] True in case of success; otherwise False.
    def _set_temperature(self, value, register):
        # @todo: Convert float to word (not working yet!?)
        word = int(value * 256.0)
        # Write the given value to the register
        return self._i2c_write_16BE(register, word)


    ###
    # Set the hysteresis temperature value.
    #
    # @param[in] self The object pointer.
    # @param[in] temperature Hysteresis temperature value.
    # @param[out] True in case of success; otherwise False.
    def set_temperature_hyst(self,temperature):
        return self._set_temperature(temperature, LM75_REG_HYST)

    ###
    # Set the overtemperature shutdown temperature value.
    #
    # @param[in] self The object pointer.
    # @param[in] temperature Overtemperature shutdown temperature value.
    # @param[out] True in case of success; otherwise False.
    def set_temperature_os(self,temperature):
        return self._set_temperature(temperature, LM75_REG_OS)
