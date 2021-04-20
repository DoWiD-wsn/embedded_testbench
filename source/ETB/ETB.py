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
# INA219 - AUX1:    OK
# INA219 - AUX2:    OK
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
# DS18B20:          OK  (sensor must be present at boot time)
# LM75:             OK
# JT103:            requires working ADS1115
#
# I2C_helper:       OK
# MCU_AVR:          
# FCNT:             not available

vsm = VSM()

ina_aux1 = INA219(address=(0x41))
ina_aux1.calibrate()
ina_aux2 = INA219(address=(0x44))
ina_aux2.calibrate()
print("AUX1: %.2f V - %.2f mA" % (ina_aux1.get_bus_voltage_V(), ina_aux1.get_current_mA()))
print("AUX2: %.2f V - %.2f mA" % (ina_aux2.get_bus_voltage_V(), ina_aux2.get_current_mA()))

adc = ADS1115()
print("AIN1: %d" % (adc.read_channel(channel=0)))
print("AIN2: %d" % (adc.read_channel(channel=1)))
print("AIN3: %d" % (adc.read_channel(channel=2)))
print("AIN4: %d" % (adc.read_channel(channel=3)))

sens = DS18B20("/sys/bus/w1/devices/28-011927fdb603/w1_slave")
print("Temperature: %.2f °C" % (sens.read_temperature()))

sens = LM75(0x49)
print("Temperature: %.2f °C" % (sens.read_temperature()))

sens = BME280()
print("Temperature: %.2f °C" % (sens.read_temperature()))
