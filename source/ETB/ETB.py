##### LIBRARIES #####
### GLOBAL ###
# time (for sleep method)
import time
### CORE ###
from ETB.core.INA219 import *
from ETB.core.VSM import *
from ETB.core.ADS1115 import *
### SENS ###
from ETB.sens.BME280 import *
from ETB.sens.DS18B20 import *
from ETB.sens.LM75 import *
from ETB.sens.JT103 import *
### COMM ###

### UTIL ###
from ETB.util.I2C_helper import *
from ETB.util.MCU_AVR import *
from ETB.util.FCNT import *
### MISC ###
GPIO.setwarnings(False)

####################

### Checks
# INA219 - CH0:     OK
# INA219 - CH1:     OK
# INA219 - CH2:     OK
# INA219 - CH3:     OK
# INA219 - AUX1:    
# INA219 - AUX2:    
#
# MIC25045 - CH0:   OK
# MIC25045 - CH1:   OK
# MIC25045 - CH2:   NOT WORKING
# MIC25045 - CH3:   OK
#
# =>VSM:
#
# ADS1115:          communication: OK - value: always 0!?
#
# BME280:           OK
# DS18B20:          
# LM75:             OK
# JT103:            requires working ADS1115
#
# I2C_helper:       OK
# MCU_AVR:          
# FCNT:             not available

# sens = DS18B20("/sys/bus/w1/devices/28-011927fdb603/w1_slave")
# print("Temperature: %.2f °C" % (sens.read_temperature()))

sens = LM75(0x49)
print("Temperature: %.2f °C" % (sens.read_temperature()))

sens = BME280()
print("Temperature: %.2f °C" % (sens.read_temperature()))
