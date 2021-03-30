#!/usr/bin/env python3

########################################################################
#   TCA9548A I2C Multiplexer                                           #
#                                                                      #
#   Author: Dominik Widhalm                                            #
#   Date:   2020-10-19                                                 #
#                                                                      #
#   Usage:                                                             #
#     # Flashing                                                       #
#     mcu_flash('binary.hex')                                          #
#     # Erasing                                                        #
#     mcu_erase()                                                      #
#                                                                      #
#   See also:                                                          #
#   https://www.journaldev.com/16140/python-system-command-os-subprocess-call #
#   https://docs.python.org/3/library/subprocess.html#module-subprocess #
#                                                                      #
########################################################################


##### LIBRARIES ########################
# System Command functionality
import subprocess
# File/directory functionality
import os
# which functionality
from shutil import which
# GPIO functionality
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
# time functionality
from time import sleep


##### MACROS ###########################
# Stream #
FNULL       = open(os.devnull, 'w')
# Target specifics #
TOOL            = 'avrdude'
MCU             = 'atmega328p'
PORT            = '/dev/ttyACM0'
DUDE            = TOOL + ' -p ' + MCU + ' -c avrispv2 -P ' + PORT + ' -v'
FLASH           = DUDE + ' -U flash:w:'
ERASE           = DUDE + ' -e'
# CLK selection
# See also https://eleccelerator.com/fusecalc/fusecalc.php?chip=atmega328p
# w/o DIV/8
CLK_INT8             = ' -U lfuse:w:0xE2:m'
CLK_INT8_CKOUT       = ' -U lfuse:w:0xA2:m'
CLK_EXT16            = ' -U lfuse:w:0xFF:m'
CLK_EXT16_CKOUT      = ' -U lfuse:w:0xBF:m'
# w/ DIV/8
CLK_INT8_DIV8        = ' -U lfuse:w:0x62:m'
CLK_INT8_DIV8_CKOUT  = ' -U lfuse:w:0x22:m'
CLK_EXT16_DIV8       = ' -U lfuse:w:0x7F:m'
CLK_EXT16_DIV8_CKOUT = ' -U lfuse:w:0x3F:m'


##### FUNCTIONS ########################
# Flash a given binary to the MCU
def mcu_flash(binary):
    # Check if the given binary exists
    if not os.path.isfile(binary):
        return False
    # Check if avrdude is installed on the system
    if not which(TOOL):
        return False
    # Check if the serial interface exists
    if not os.path.exists(PORT):
        return False
    # Prepare program string
    cmd = FLASH + binary
    # Flash the binary
    ret = subprocess.run(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    # Check if flashing was successful
    if ret.returncode==0:
        return True
    else:
        return False

# Erase the MCU
def mcu_erase():
    # Check if avrdude is installed on the system
    if not which(TOOL):
        return False
    # Check if the serial interface exists
    if not os.path.exists(PORT):
        return False
    # Erase the MCU
    ret = subprocess.run(ERASE, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    # Check if erasing was successful
    if ret.returncode==0:
        return True
    else:
        return False

# Reset the MCU (via GPIO)
def mcu_reset(rst_pin):
    # Set RST to output
    GPIO.setup(rst_pin, GPIO.OUT)
    # Pull the RST line down
    GPIO.output(rst_pin, 0)
    # Wait for 200ms
    sleep(0.2)
    # Set RST line back to "1"
    GPIO.output(rst_pin, 1)
    # Release the RST line
    GPIO.setup(rst_pin, GPIO.IN)

# Set the CLK source of the AVR
# src   ... 0->INT8 / 1->EXT16
# ckout ... 0->DIS  / 1->EN
# div8  ... 0->DIS  / 1->EN
def mcu_set_clksrc(src, ckout, div8):
    # Check if avrdude is installed on the system
    if not which(TOOL):
        return False
    # Check if the serial interface exists
    if not os.path.exists(PORT):
        return False
    # Select fuse value based on given parameter
    if (div8==0):
        # w/o CLK/8
        if (src==0) and (ckout==0):
            cmd = DUDE + CLK_INT8
        elif (src==0) and (ckout==1):
            cmd = DUDE + CLK_INT8_CKOUT
        elif (src==1) and (ckout==0):
            cmd = DUDE + CLK_EXT16
        elif (src==1) and (ckout==1):
            cmd = DUDE + CLK_EXT16_CKOUT
        else:
            # Invalid parameter
            return False
    else:
        # w/ CLK/8
        if (src==0) and (ckout==0):
            cmd = DUDE + CLK_INT8_DIV8
        elif (src==0) and (ckout==1):
            cmd = DUDE + CLK_INT8_DIV8_CKOUT
        elif (src==1) and (ckout==0):
            cmd = DUDE + CLK_EXT16_DIV8
        elif (src==1) and (ckout==1):
            cmd = DUDE + CLK_EXT16_DIV8_CKOUT
        else:
            # Invalid parameter
            return False
    # Write the fuses
    ret = subprocess.run(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    # Check if flashing was successful
    if ret.returncode==0:
        return True
    else:
        return False
