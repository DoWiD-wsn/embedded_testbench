#!/usr/bin/env python3

#####
# @brief   Power monitor example
#
# Simple power monitor continuously measuring and printing the voltage,
# current, and resulting power consumption of all 4 output channels.
#
# @file     /examlpes/power_monitor.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/30 $
#
# @example  Run with 'python3 power_monitor.py'
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
# To catch system signals
import signal


##### DEFINES ##########################
### Update interval [ms]
UPDATE_INTERVAL = 250

### Output voltages [V]
VOUT_CH1        = 3.3
VOUT_CH2        = 3.3
VOUT_CH3        = 3.3
VOUT_CH4        = 3.3

### Terminate flag
terminate = 0


##### CALLBACK #########################
# SIGINT CALLBACK
def sigint_callback(sig, frame):
    # Need to make terminate global
    global terminate
    # Set terminate to 1
    terminate = 1
    # Remove "^C" from output
    sys.stdout.write("\b\b\b\b")


########################################################################
# Add CRTL-C callback (needed for program termination)
signal.signal(signal.SIGINT, sigint_callback)

# Initialize ETB
etb = ETB()
# First, disable outputs until values are properly set
etb.ch_disable_all()
# Get decimal output voltage values
vch1_dec = etb.volt2dec(VOUT_CH1)
vch2_dec = etb.volt2dec(VOUT_CH2)
vch3_dec = etb.volt2dec(VOUT_CH3)
vch4_dec = etb.volt2dec(VOUT_CH4)
# Set output voltages
etb.ch_set_V_decimal(1, vch1_dec)
etb.ch_set_V_decimal(2, vch2_dec)
etb.ch_set_V_decimal(3, vch3_dec)
etb.ch_set_V_decimal(4, vch4_dec)
# Enable outputs
etb.ch_enable_all()

# Write starting-message
print("=====          POWER MONITOR START          =====")
print("===             (quit with CTRL+C             ===")

# Print header
print("channel | voltage (V) | current (mA) | power (mW)")
print("-------------------------------------------------")
print(" %4d   | %9.2f   | %10.2f   | %8.2f" % (1,0,0,0))
print(" %4d   | %9.2f   | %10.2f   | %8.2f" % (2,0,0,0))
print(" %4d   | %9.2f   | %10.2f   | %8.2f" % (3,0,0,0))
print(" %4d   | %9.2f   | %10.2f   | %8.2f" % (4,0,0,0))

# Run loop as long as no SIGINT was received
while (terminate != 1):
    # Move cursor up
    print("\033[A\033[A\033[A\033[A\033[A")
    # Measure all channels
    for ch in range(1,5):
        # Measure voltage and current
        v = etb.ch_get_V(ch)
        i = etb.ch_get_mA(ch)
        # Limit current in case of wrongly measured negative values
        if i<0:
            i=0.0
        # Calculate power
        p = v * i
        # Update result
        print(" %4d   | %9.2f   | %10.2f   | %8.2f" % (ch,v,i,p))
    
    # Measure channels
    time.sleep(UPDATE_INTERVAL/1000)

# Measurements finished
print("=====         POWER MEASUREMENT END         =====")
########################################################################

# End of experiment
exit(0)
