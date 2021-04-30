#!/usr/bin/env python3

#####
# @brief   ETB self-check example
#
# Simple power monitor continuously measuring and printing the voltage,
# current, and resulting power consumption of all 4 output channels.
#
# @file     /examlpes/etb_self-check.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/30 $
#
# @example  Run with 'python3 etb_self-check.py'
#####

##### PREREQUISITES ####################
# Add path to the ETB module
import sys
# Check the Python version
assert sys.version_info >= (3, 0), "ETB requires Python 3!"
# Add base folder to path
sys.path.insert(1, '../')
# Import the ETB module
from ETB.ETB import *


#### IMPORTS ###########################
# time (for sleep method)
import time
# datetime
from datetime import datetime
# Additional ETB libraries (sensors)
from ETB.sens.BME280 import *
from ETB.sens.DS18B20 import *
from ETB.sens.LM75 import *


##### DEFINES ##########################
# Thermistor 0 connected (0 .. no / 1 .. yes)
ENABLE_THERM_0          = 1
# Thermistor 1 connected (0 .. no / 1 .. yes)
ENABLE_THERM_1          = 0

# DS18B20 connected (0 .. no / 1 .. yes)
ENABLE_DS18B20          = 1
# Sensor path
DS18B20_path            = '/sys/bus/w1/devices/28-011927fdb603/w1_slave'

# LM75 connected (0 .. no / 1 .. yes)
ENABLE_LM75             = 1
# Sensor I2C address
LM75_address            = 0x48

# BME280 connected (0 .. no / 1 .. yes)
ENABLE_BME280           = 1
# Sensor I2C address
BME280_address          = 0x76


########################################################################
# Initialize ETB
etb = ETB()
# First, disable outputs until values are properly set
etb.ch_disable_all()

# Write starting-message
print("===== ETB SELF-TEST START =====")

### Check MICs
print("=== MIC (supply) ===")
ch_enable = [None]*5
# Step 1
print("-> Disable all")
sys.stdout.write("   ")
for i in range(1,5):
    ch_enable[i] = etb.ch_is_enabled(i)
    sys.stdout.write("ch%d = %d" % (i,ch_enable[i]))
    if i<4:
        sys.stdout.write(" | ")
    else:
        sys.stdout.write("\n")
if (ch_enable[1] == 0) and (ch_enable[2] == 0) and (ch_enable[3] == 0) and (ch_enable[4] == 0):
    print("   => OK")
else:
    print("   => FAIL")
    exit(-1)
# Step 2
print("-> Enable ch1")
etb.ch_enable(1)
sys.stdout.write("   ")
for i in range(1,5):
    ch_enable[i] = etb.ch_is_enabled(i)
    sys.stdout.write("ch%d = %d" % (i,ch_enable[i]))
    if i<4:
        sys.stdout.write(" | ")
    else:
        sys.stdout.write("\n")
if (ch_enable[1] == 1) and (ch_enable[2] == 0) and (ch_enable[3] == 0) and (ch_enable[4] == 0):
    print("   => OK")
else:
    print("   => FAIL")
    exit(-1)
# Step 3
print("-> Enable ch2")
etb.ch_enable(2)
sys.stdout.write("   ")
for i in range(1,5):
    ch_enable[i] = etb.ch_is_enabled(i)
    sys.stdout.write("ch%d = %d" % (i,ch_enable[i]))
    if i<4:
        sys.stdout.write(" | ")
    else:
        sys.stdout.write("\n")
if (ch_enable[1] == 1) and (ch_enable[2] == 1) and (ch_enable[3] == 0) and (ch_enable[4] == 0):
    print("   => OK")
else:
    print("   => FAIL")
    exit(-1)
# Step 4
print("-> Enable ch3")
etb.ch_enable(3)
sys.stdout.write("   ")
for i in range(1,5):
    ch_enable[i] = etb.ch_is_enabled(i)
    sys.stdout.write("ch%d = %d" % (i,ch_enable[i]))
    if i<4:
        sys.stdout.write(" | ")
    else:
        sys.stdout.write("\n")
if (ch_enable[1] == 1) and (ch_enable[2] == 1) and (ch_enable[3] == 1) and (ch_enable[4] == 0):
    print("   => OK")
else:
    print("   => FAIL")
    exit(-1)
# Step 5
print("-> Enable ch4")
etb.ch_enable(4)
sys.stdout.write("   ")
for i in range(1,5):
    ch_enable[i] = etb.ch_is_enabled(i)
    sys.stdout.write("ch%d = %d" % (i,ch_enable[i]))
    if i<4:
        sys.stdout.write(" | ")
    else:
        sys.stdout.write("\n")
if (ch_enable[1] == 1) and (ch_enable[2] == 1) and (ch_enable[3] == 1) and (ch_enable[4] == 1):
    print("   => OK")
else:
    print("   => FAIL")
    exit(-1)
# Step 6
print("-> Disable all again")
sys.stdout.write("   ")
etb.ch_disable_all()
for i in range(1,5):
    ch_enable[i] = etb.ch_is_enabled(i)
    sys.stdout.write("ch%d = %d" % (i,ch_enable[i]))
    if i<4:
        sys.stdout.write(" | ")
    else:
        sys.stdout.write("\n")
if (ch_enable[1] == 0) and (ch_enable[2] == 0) and (ch_enable[3] == 0) and (ch_enable[4] == 0):
    print("   => OK")
else:
    print("   => FAIL")
    exit(-1)
print()

### Check INAs
print("=== INA (wattmeter) ===")
# Main channels
for i in range(1,5):
    v = etb.ch_get_V(i)
    a = etb.ch_get_mA(i)
    if (v is not False) and (a is not False):
        print("-> ch%d: V = %.2f V | I = %.2f mA" % (i,v,a))
        print("   => OK")
    else:
        print("-> ch%d: FAIL" % (i))
        exit(-1)
# Auxiliary channels
for i in range(1,3):
    v = etb.aux_get_V(i)
    a = etb.aux_get_mA(i)
    if (v is not False) and (a is not False):
        print("-> aux%d: V = %.2f V | I = %.2f mA" % (i,v,a))
        print("   => OK")
    else:
        print("-> aux%d: FAIL" % (i))
        exit(-1)
print()

### Check ADC
print("=== ADS1115 (ADC) ===")
# Raw channels
for i in range(4):
    adc = etb.read_channel(i)
    if (adc is not False):
        print("-> adc%d = %d" % (i,adc))
        print("   => OK")
    else:
        print("-> adc%d: FAIL" % (i))
        exit(-1)
# Thermistor temperature
if ENABLE_THERM_0:
    temp = etb.read_thermistor(0)
    if (adc is not False):
        print("-> thermistor0 = %.2f °C" % (temp))
        print("   => OK")
    else:
        print("-> thermistor0: FAIL")
        exit(-1)
if ENABLE_THERM_1:
    temp = etb.read_thermistor(1)
    if (adc is not False):
        print("-> thermistor1 = %.2f °C" % (temp))
        print("   => OK")
    else:
        print("-> thermistor1: FAIL")
        exit(-1)
print()
### Check Sensors
print("=== SENSORS ===")
# DS18B20
if ENABLE_DS18B20:
    print("-> DS18B20")
    ds18b20 = DS18B20(DS18B20_path)
    temp = ds18b20.read_temperature()
    if (temp is not False):
        print("   temperature = %.2f °C" % (temp))
        print("   => OK")
    else:
        print("   => FAIL")
        exit(-1)
    print()
# LM75
if ENABLE_LM75:
    print("-> LM75")
    lm75 = LM75(LM75_address)
    temp = lm75.read_temperature()
    if (temp is not False):
        print("   temperature = %.2f °C" % (temp))
        print("   => OK")
    else:
        print("   => FAIL")
        exit(-1)
    print()
# BME280
if ENABLE_BME280:
    print("-> BME280")
    bme280 = BME280(BME280_address)
    temp = bme280.read_temperature()
    if (temp is not False):
        print("   temperature = %.2f °C" % (temp))
        print("   => OK")
    else:
        print("   => FAIL")
        exit(-1)
    pres = bme280.read_pressure()
    if (temp is not False):
        print("   pressure = %.2f hPa" % (pres))
        print("   => OK")
    else:
        print("   => FAIL")
        exit(-1)
    humi = bme280.read_humidity()
    if (temp is not False):
        print("   humidity = %.2f %% RH" % (humi))
        print("   => OK")
    else:
        print("   => FAIL")
        exit(-1)
    print()

# Self-test finished
print("===== ETB SELF-TEST END   =====")
########################################################################

# End of experiment
exit(0)

