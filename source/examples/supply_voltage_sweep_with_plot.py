#!/usr/bin/env python3

#####
# @brief   Supply voltage sweep example with result plotting
#
# Single output channel supply voltage sweep and power measurements
# example with definable voltage limits. The results are plotted
# via matplotlib.
#
# @file     /examlpes/supply_voltage_sweep_with_plot.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/30 $
#
# @example  Run with 'python3 supply_voltage_sweep_with_plot.py'
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
# directory/file functionality
import os
# Math functionality (ceil() for plotting)
from math import ceil
# CSV functionality
import csv
# Matplotlib for plotting
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})
from matplotlib import rc
rc('mathtext', default='regular')
from matplotlib.ticker import *


##### DEFINES ##########################
### Output channel
OUTPUT_CHANNEL  = 1
### Minimum and maximum voltage of sweep [V]
VOLT_MIN        = 1.5
VOLT_MAX        = 3.3
### Sweep direction (0 .. low to high / 1 .. high to low)
VOLT_DIR        = 1

### Number of measurements per voltage level
NUM_MEAS        = 10

### Delay between measurements of same voltage level [ms]
DELAY_GAP       = 10
### Voltage settle delay (before measurement) [ms]
DELAY_PRE       = 1000
### After measurement delay [ms]
DELAY_POST      = 500

### Result output as CSV file (0 .. disable / 1 .. enable) ###
OUTPUT_CSV      = 1
RESULT_DIR      = "results/"


##### FUNCTIONS ########################
def ceil_to_tens(x):
    return int(ceil(x/10.0)) * 10


########################################################################
# Save timestamp
timestamp = datetime.now()

# Check if result directory exists
if not os.path.exists(RESULT_DIR):
    try:
        os.makedirs(RESULT_DIR)
    except Exception as e:
        print("ERROR: Couldn't create directory for results ... aborting!")
        print(e)
        exit(-1)

# Check if CSV output is enabled
if OUTPUT_CSV==1:
    # Create the filename of the CSV file
    csv_file = RESULT_DIR+"%s-power_measurement.csv" % (timestamp.strftime("%Y-%m-%d_%H-%M-%S"))
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

# Dictionary to store measurements
volt_dict = dict()
curr_dict = dict()
powe_dict = dict()
# Arrays for post-processing
volt_dec = []
volt_min = []
curr_min = []
powe_min = []
volt_avg = []
curr_avg = []
powe_avg = []
volt_max = []
curr_max = []
powe_max = []

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
    # Initialize all dictionaries
    volt_dict[vout]     = []
    curr_dict[vout]     = []
    powe_dict[vout]     = []
    # Perform several measurements per voltage level
    for num in range(NUM_MEAS):
        # Measure voltage and current
        v = etb.ch_get_V(OUTPUT_CHANNEL)
        i = etb.ch_get_mA(OUTPUT_CHANNEL)
        # Limit current in case of wrongly measured negative values
        if i<0:
            i=0.0
        # Calculate power
        p = v * i
        # Add measurements to result arrays
        volt_dict[vout].append(round(v,3))
        curr_dict[vout].append(round(i,3))
        powe_dict[vout].append(round(p,3))
        # CSV output (if enabled)
        if OUTPUT_CSV==1:
            try:
                # Write a row into the CSV file
                csv_o.writerow([vout, v, i, p])
            except Exception as e:
                print("Writing measurement data to the CSV file failed ... aborting!", exc_info=True)
                exit(-1)
        # Inter-measurement delay
        time.sleep(DELAY_GAP/1000)
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

# Finish CSV output
if OUTPUT_CSV==1:
    try:
        # Write a row into the CSV file
        csv_f.close()
    except Exception as e:
        print("Finishing the CSV file failed ... aborting!", exc_info=True)
        exit(-1)

# Calculate averages for plotting
for cnt in sorted(volt_dict.keys()):
    # Build voltage array
    volt_dec.append(cnt)
    ### Voltage ###
    Vmin = 99999
    Vavg = 0
    Vmax = 0
    for value in volt_dict[cnt]:
        Vavg += value
        if value > Vmax:
            Vmax = value
        if value < Vmin:
            Vmin = value
    Vavg = round(Vavg/NUM_MEAS, 3)
    # Add values to array
    volt_min.append(Vmin)
    volt_avg.append(Vavg)
    volt_max.append(Vmax)
    ### Current ###
    Imin = 99999
    Iavg = 0
    Imax = 0
    for value in curr_dict[cnt]:
        Iavg += value
        if value > Imax:
            Imax = value
        if value < Imin:
            Imin = value
    Iavg = round(Iavg/NUM_MEAS, 3)
    # Add values to array
    curr_min.append(Imin)
    curr_avg.append(Iavg)
    curr_max.append(Imax)
    ### Power ###
    Pmin = 99999
    Pavg = 0
    Pmax = 0
    for value in powe_dict[cnt]:
        Pavg += value
        if value > Pmax:
            Pmax = value
        if value < Pmin:
            Pmin = value
    Pavg = round(Pavg/NUM_MEAS, 3)
    # Add values to array
    powe_min.append(Pmin)
    powe_avg.append(Pavg)
    powe_max.append(Pmax)

##### PLOT DATA ######
# Create subplots
fig = plt.figure(figsize=(9,4), dpi=150)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

# AX1 (current)
ax1.grid(which='major', color='#CCCCCC', linestyle=':')
ax1.set_xlabel('supply voltage (V)')
ax1.set_ylabel('current consumption (mA)')
ax1.set_xlim(VOLT_MIN,VOLT_MAX)
ax1.set_ylim(0,ceil_to_tens(max(curr_max)))
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.xaxis.set_ticks_position('bottom')
ax1.spines['bottom'].set_position(('data',0))
ax1.yaxis.set_ticks_position('left')
ax1.spines['left'].set_position(('data',VOLT_MIN))
ax1.xaxis.set_major_locator(MultipleLocator(0.5))
ax1.xaxis.set_minor_locator(AutoMinorLocator(5))
ax1.xaxis.grid(False)
ax1.yaxis.set_major_locator(MultipleLocator(5))
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))

# AX2 (power)
ax2.set_ylabel("power consumption (mW)")
ax2.set_ylim(0,ceil_to_tens(max(powe_max)))
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.xaxis.set_ticks_position('bottom')
ax2.spines['bottom'].set_position(('data',0))
ax2.yaxis.set_ticks_position('right')
ax2.spines['right'].set_position(('data',VOLT_MAX))
ax2.yaxis.set_major_locator(MultipleLocator(10))
ax2.yaxis.set_minor_locator(AutoMinorLocator(2))

## plot y1
# Current
lns1 = ax1.plot(volt_avg, curr_avg, '-', label="Current", color="tab:red")
ax1.fill_between(volt_avg, curr_min, curr_max, alpha=0.35, antialiased=True, color="tab:red")

# plot y2
ax2._get_lines.prop_cycler = ax1._get_lines.prop_cycler
# Power
lns2 = ax2.plot(volt_avg, powe_avg, '-.', label="Power", color="tab:purple")
ax2.fill_between(volt_avg, powe_min, powe_max, alpha=0.35, antialiased=True, color="tab:purple")

# Prepare legend
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax2.legend(lns, labs, ncol=2, loc='upper center', facecolor='white', framealpha=1)

plot_file = RESULT_DIR+"%s-power_measurement.svg" % (timestamp.strftime("%Y-%m-%d_%H-%M-%S"))
plt.savefig(plot_file, transparent=True)
plt.cla()
plt.clf()

# Measurements finished
print("===== POWER MEASUREMENT END   =====")
########################################################################

# End of experiment
exit(0)
