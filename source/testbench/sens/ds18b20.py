#!/usr/bin/env python3

########################################################################
#   DS18B20 Temperature Sensor (One Wire Interface)                    #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-14                                                 #
#                                                                      #
#   Notes:                                                             #
#   *) Do not forget the pull up (10k or 4k7) between DATA and VCC     #
#                                                                      #
#   Usage:                                                             #
#     sensor = DS18B20()                                               #
#     or                                                               #
#     sensor = DS18B20('/sys/bus/w1/devices/28-011927fdb603/w1_slave') #
#     then                                                             #
#     tempC = sensor.readTemp()                                        #
#                                                                      #
#   See also:                                                          #
#   https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/ #
#   https://github.com/timofurrer/w1thermsensor/                       #
#                                                                      #
########################################################################

##### LIBRARIES ########################
# time functionality
from time import sleep

##### SETTINGS (adapt if necessary #####################################
MAX_ATTEMPTS = 10

##### DS18B20 CLASS ####################
class DS18B20(object):
    # Constructor
    def __init__(self, path):
        self.__path = path

    # Read the raw sensor data
    def __read_raw(self) :
        # Open given system bus address
        data = False
        try:
            sens = open(self.__path, 'r')
            data = sens.readlines()
            sens.close()
        except:
            return False
        else:
            return data

    # Read the converted sensor data (degreeC)
    def read_temp(self):
        data = self.__read_raw()
        if data:
            # Check if sensor is ready
            attempts = 0
            while ((len(data) < 1) or (data[0].strip()[-3:] != "YES") or ("00 00 00 00 00 00 00 00 00" in data[0])):
                sleep(0.25)
                data = self.__read_raw()
                attempts = attempts + 1
                if attempts >= MAX_ATTEMPTS:
                    return False
            # Check for temperature reading suffix
            equals_pos = data[1].find('t=')
            if equals_pos != -1:
                return (float(data[1][equals_pos+2:]) / 1000.0)
        else:
            return False
