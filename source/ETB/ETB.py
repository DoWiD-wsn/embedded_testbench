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
for i in range(4):
    cnt = i
    
    vsm._mux.select(cnt+1)
    vsm._mic[cnt].enable()
    time.sleep(1)
    vsm._mic[cnt].disable()
    print(vsm._mic[cnt].read_register_status())   # (0, 0, 0, 0, 0)
    print(vsm._mic[cnt].read_register_setting1()) # (1, 2)
    print(vsm._mic[cnt].read_register_setting2()) # (0, 0, 0)
    print(vsm._mic[cnt].read_register_vout())
    print(vsm._mic[cnt].set_output_voltage(123))
    print(vsm._mic[cnt].read_register_vout())
    print(vsm._mic[cnt].is_enabled())
    vsm._mic[cnt].enable()
    time.sleep(0.5)
    print(vsm._mic[cnt].is_enabled())
    print()

# GPIO #
GPIO.cleanup()

exit(0)

vsm.ALL_disable()
time.sleep(1)
vsm.CH3_enable()
for i in range(vsm.volt2dec(3.3)+1):
    print("Set %.2f V" % (vsm.dec2volt(i)))
    vsm.CH3_set_decimal_V(i)
    print("  %.2f V -> %.2f mA" % (vsm.CH3_get_V(), vsm.CH3_get_mA()))
time.sleep(1)
vsm.ALL_disable()

# adc = ADS1115()
# print("AIN1: %d" % (adc.read_channel(channel=0)))
# print("AIN2: %d" % (adc.read_channel(channel=1)))
# print("AIN3: %d" % (adc.read_channel(channel=2)))
# print("AIN4: %d" % (adc.read_channel(channel=3)))

# GPIO #
GPIO.cleanup()
