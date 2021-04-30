#!/usr/bin/env python3

#####
# @brief   Supply voltage sweep example
#
# Single output channel supply voltage sweep and power measurements
# example with definable voltage limits.
#
# @file     /examlpes/supply_voltage_sweep.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/30 $
#
# @example  Run with 'python3 supply_voltage_sweep.py'
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
# CSV functionality
import csv


##### DEFINES ##########################
### Output channel
OUTPUT_CHANNEL  = 1
### Minimum and maximum voltage of sweep
VOLT_MIN        = 1.5
VOLT_MAX        = 3.3
### Sweep direction (0 .. low to high / 1 .. high to low)
VOLT_DIR        = 1

### Voltage settle delay (before measurement) [ms]
DELAY_PRE       = 1000
### After measurement delay [ms]
DELAY_POST      = 500

### Result output as CSV file (0 .. disable / 1 .. enable) ###
OUTPUT_CSV      = 1
RESULT_DIR      = "results/"


########################################################################
# Check if CSV output is enabled
if OUTPUT_CSV==1:
    # Check if result directory exists
    if not os.path.exists(RESULT_DIR):
        try:
            os.makedirs(RESULT_DIR)
        except Exception as e:
            print("ERROR: Couldn't create directory for results ... aborting!")
            print(e)
            exit(-1)
    # Create the filename of the CSV file
    csv_file = RESULT_DIR+"%s-power_measurement.csv" % (datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    # Try to open/create CSV file and CSV writer
    try:
        csv_f = open(csv_file, 'w')
        csv_o = csv.writer(csv_f)
    except Exception as e:
        print("Cannot open the CSV file/reader ... aborting!", exc_info=True)
        exit(-1)
    # Write initial rows to the CSV file
    try:
        csv_o.writerow(["dec", "volt [V]", "current [mA]", "power [mW]"])
    except Exception as e:
        print("Writing initial data to the CSV file failed ... aborting!", exc_info=True)
        exit(-1)

# Initialize ETB
etb = ETB()
etb.ch_disable_all()
etb.ch_set_V_decimal_all(0)

# Get voltage limits (decimal, for MIC)
if VOLT_DIR:
    vstart_dec = etb.volt2dec(VOLT_MAX)
    vend_dec = etb.volt2dec(VOLT_MIN)
else:
    vstart_dec = etb.volt2dec(VOLT_MIN)
    vend_dec = etb.volt2dec(VOLT_MAX)
vout = vstart_dec

# Arrays to store all measurments for post-processing
volt = []
current = []
power = []

# Write starting-message
print("===== POWER MEASUREMENT START =====")

##########
# Run loop (break by condition)
while True:
    print("Set Vout to %.2f V ..." % etb.dec2volt(vout))
    # Set output voltage
    etb.ch_set_V_decimal(OUTPUT_CHANNEL,vout)
    etb.ch_enable(OUTPUT_CHANNEL)
    
    # Pre-measurement delay
    time.sleep(DELAY_PRE/1000)
    
    # Measure voltage and current
    v = etb.ch_get_V(OUTPUT_CHANNEL)
    i = etb.ch_get_mA(OUTPUT_CHANNEL)
    # Limit current in case of wrongly measured negative values
    if i<0:
        i=0.0
    # Calculate power
    p = v * i
    
    # Print intermediate results
    print("...  Vout = %.2f V" % v)
    print("...  Iout = %.2f mA" % i)
    print("...  Pout = %.2f mW" % p)
    # Add measurements to result arrays
    volt.append(v)
    current.append(i)
    power.append(p)
    
    # CSV output (if enabled)
    if OUTPUT_CSV==1:
        try:
            # Write a row into the CSV file
            csv_o.writerow([vout, v, i, p])
        except Exception as e:
            print("Writing measurement data to the CSV file failed ... aborting!", exc_info=True)
            exit(-1)
    
    # Post-measurement delay
    time.sleep(DELAY_POST/1000)
    
    # Increment/decrement vout
    if VOLT_DIR:
        vout-=1
        # Check if limit has been reached
        if vout<vend_dec:
            break
    else:
        vout+=1
        # Check if limit has been reached
        if vout>vend_dec:
            break
##########
etb.ch_disable_all()

# Get minimum, maximum and mean value
v_min = 99999
v_max = 0
v_avg = 0
i_min = 99999
i_max = 0
i_avg = 0
p_min = 99999
p_max = 0
p_avg = 0
for i in range(len(volt)):
    v_avg += volt[i]
    i_avg += current[i]
    p_avg += power[i]
    # Check for minimum
    if volt[i]<v_min:
        v_min = volt[i]
    if current[i]<i_min:
        i_min = current[i]
    if power[i]<p_min:
        p_min = power[i]
    # Check for maximum
    if volt[i]>v_max:
        v_max = volt[i]
    if current[i]>i_max:
        i_max = current[i]
    if power[i]>p_max:
        p_max = power[i]
# Get mean value
v_avg = round(v_avg/len(volt), 2)
i_avg = round(i_avg/len(current), 2)
p_avg = round(p_avg/len(power), 2)

# Print min, mean, and max values
print("====================================")
print("mean: %2.2f V - %3.2f mA - %3.2f mW" % (v_avg, i_avg, p_avg))
print("min : %2.2f V - %3.2f mA - %3.2f mW" % (v_min, i_min, p_min))
print("max : %2.2f V - %3.2f mA - %3.2f mW" % (v_max, i_max, p_max))

# CSV output (if enabled)
if OUTPUT_CSV==1:
    try:
        # Write a row into the CSV file
        csv_o.writerow([])
        csv_o.writerow(["mean", v_avg, i_avg, p_avg])
        csv_o.writerow(["min", v_min, i_min, p_min])
        csv_o.writerow(["max", v_max, i_max, p_max])
    except Exception as e:
        print("Writing measurement data to the CSV file failed ... aborting!", exc_info=True)
        exit(-1)

# Finish CSV output
if OUTPUT_CSV==1:
    try:
        # Write a row into the CSV file
        csv_f.close()
    except Exception as e:
        print("Finishing the CSV file failed ... aborting!", exc_info=True)
        exit(-1)

# Measurements finished
print("===== POWER MEASUREMENT END   =====")
########################################################################

# End of experiment
exit(0)
