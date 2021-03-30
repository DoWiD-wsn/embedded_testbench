#!/usr/bin/env python3

########################################################################
#   I2C Helper Functions                                               #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-14                                                 #
#                                                                      #
#   Notes:                                                             #
#       *) Don't forget to enable I2C, e.g. with sudo raspi-config     #
#                                                                      #
#   Usage:                                                             #
#     stemma = STEMMA()                                                #
#     or                                                               #
#     stemma = STEMMA(0x36)                                            #
#     then                                                             #
#     tempC = stemma.readTemp()                                        #
#     tempC = stemma.readMoisture()                                    #
#                                                                      #
#   See also:                                                          #
#   https://github.com/muhammadrefa/python-i2c-scanner/blob/master/i2c-scanner.py #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# Import board and busio for I2C functionality
import smbus


##### I2C SCANNER ######################
def i2c_scan(start=0x00, end=0x78, busnum=1):
    try:
        bus = smbus.SMBus(busnum)
    except:
        return None
    else:
        devices = []
        for i in range(start, end):
            val = 1
            try:
                bus.read_byte(i)
            except OSError as e:
                val = e.args[0]
            else:
                if val == 1:
                    devices.append(i)
        return devices


##### CHECK FOR I2C DEVICE #############
def i2c_is_available(address, busnum=1):
    try:
        bus = smbus.SMBus(busnum)
    except:
        return False
    else:
        try:
            bus.read_byte(address)
            return True
        except:
            return False
