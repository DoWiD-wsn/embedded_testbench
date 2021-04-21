#####
# @brief   I2C helper functions
#
# Module containing I2C helper functions.
#
# @file     /etb/util/I2C_helper.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/08 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
# @see      https://github.com/muhammadrefa/python-i2c-scanner/blob/master/i2c-scanner.py
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


###
# Scan the I2C bus for available devices.
#
# @param[in]    start           Start address for scan (default: 0x00).
# @param[in]    end             End address for scan (default: 0x78).
# @param[in]    busnum          Specific I2C bus number (default: 1)
# return        List of available devices (addresses).
def I2C_scan(start=0x00, end=0x78, busnum=1):
    # Try to open the I2C bus
    try:
        bus = smbus.SMBus(busnum)
    except:
        return None
    else:
        devices = []
        # Scan specified addresses for devices
        for i in range(start, end):
            val = 1
            try:
                # If read is successful, device is available at this address
                bus.read_byte(i)
            except OSError as e:
                val = e.args[0]
            else:
                if val == 1:
                    # Add device-address to the list
                    devices.append(i)
        # Return the list of found devices
        return devices


###
# Check if device at given address is available.
#
# @param[in]    address         Address to be checked.
# @param[in]    busnum          Specific I2C bus number (default: 1)
# @return       True in case of success; otherwise False.
def I2C_is_available(address, busnum=1):
    # Try to open the I2C bus
    try:
        bus = smbus.SMBus(busnum)
    except:
        return False
    else:
        try:
            # Try to communicate with the device
            bus.read_byte(address)
        except:
            return False
        else:
            return True
