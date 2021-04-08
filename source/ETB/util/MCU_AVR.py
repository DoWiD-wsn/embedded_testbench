#####
# @brief   AVR MCU utilities
#
# Module containing AVR MCU utility functions.
#
# @file     /etb/util/MCU_AVR.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/08 $
#
# @see      https://docs.python.org/3/library/subprocess.html#module-subprocess
#
# @example  MCU_flash("path_to/binary.hex")             # Flash the given binary on the MCU
# @example  MCU_erase()                                 # Erase the MCU
# @example  MCU_reset()                                 # Reset the MCU (via RST GPIO pin)
# @example  MCU_set_clksrc(MCU_CLK_EXT, False, False)   # Select the clock source
#####


##### LIBRARIES #####
# Subprocesss to call AVRDUDE from Python
import subprocess
# File/directory functionality
import os
# time (for sleep method)
import time
# GPIO functionality
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


##### GLOBAL VARIABLES #####
# MCU target specifics
MCU_TOOL        = 'avrdude'
MCU_DEFAULT     = 'atmega1284p'
PORT_DEFAULT    = '/dev/ttyACM0'
# CLK selection
MCU_CLK_INT     = 0
MCU_CLK_EXT     = 1
### Fuse bytes ###
MCU_FUSE_TAG = {
    'extended': 'efuse',
    'high': 'hfuse',
    'low': 'lfuse'
}
# Fuse extended byte
MCU_FE_BODLEVEL_OFFSET  = 0
MCU_FE_BODLEVEL_MASK    = 0xF7
# Fuse high byte
MCU_FH_OCDEN_OFFSET     = 7
MCU_FH_JTAGEN_OFFSET    = 6
MCU_FH_SPIEN_OFFSET     = 5
MCU_FH_WDTON_OFFSET     = 4
MCU_FH_EESAVE_OFFSET    = 3
MCU_FH_BOOTSZ_OFFSET    = 1
MCU_FH_BOOTSZ_MASK      = 0xF9
MCU_FH_BOOTRST_OFFSET   = 0
# Fuse low byte
MCU_FL_CKDIV8_OFFSET    = 7
MCU_FL_CKOUT_OFFSET     = 6
MCU_FL_SUT_OFFSET       = 4
MCU_FL_SUT_MASK         = 0xCF
MCU_FL_CKSEL_OFFSET     = 0
MCU_FL_CKSEL_MASK       = 0xF0


###
# Flash a given binary to the MCU.
#
# @param[in] binary Path to the binary (.hex).
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] True in case of success; otherwise False.
def MCU_flash(binary, port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    # Check if the given binary exists
    if not os.path.isfile(binary):
        return False
    # Check if the serial interface exists
    if not os.path.exists(port):
        return False
    # Prepare program string
    cmd = "%s -p %s -c avrispv2 -P %s -v -U flash:w:%s" % (MCU_TOOL, mcu, port, binary)
    # Try to flash the binary
    ret = subprocess.run(cmd, shell=True, capture_output=True)
    # Check if flashing was successful
    if ret.returncode==0:
        return True
    else:
        return False


###
# Read the specified fuses of the MCU.
#
# @param[in] fuse Fuse byte to be read.
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] Fuse byte value in case of success; otherwise False.
def _MCU_get_fuse(fuse, port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    # Check if the serial interface exists
    if not os.path.exists(port):
        return False
    # Check if a valid fuse byte was chosen
    if fuse not in MCU_FUSE_TAG:
        raise ValueError('Valid fuse bytes are: \'extended\', \'high\', and \'low\'')
    # Prepare program string
    cmd = "%s -p %s -c avrispv2 -P %s -v -U %s:r:-:d" % (MCU_TOOL, mcu, port, MCU_FUSE_TAG[fuse])
    # Try to program the fuses
    ret = subprocess.run(cmd, shell=True, capture_output=True)
    # Check if programming was successful
    if ret.returncode==0:
        return int(ret.stdout.decode("utf-8"))
    else:
        return False


###
# Read the extended fuses of the MCU.
#
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] Fuse byte value in case of success; otherwise False.
def MCU_get_efuse(port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    return _MCU_get_fuse('extended', port, mcu)


###
# Read the high fuses of the MCU.
#
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] Fuse byte value in case of success; otherwise False.
def MCU_get_hfuse(port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    return _MCU_get_fuse('high', port, mcu)


###
# Read the low fuses of the MCU.
#
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] Fuse byte value in case of success; otherwise False.
def MCU_get_lfuse(port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    return _MCU_get_fuse('low', port, mcu)


###
# Program the specified fuses of the MCU.
#
# @param[in] fuse Fuse byte to be programmed.
# @param[in] byte Fuse byte value.
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] True in case of success; otherwise False.
def _MCU_set_fuse(fuse, byte, port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    # Check if the serial interface exists
    if not os.path.exists(port):
        return False
    # Check if a valid fuse byte was chosen
    if fuse not in MCU_FUSE_TAG:
        raise ValueError('Valid fuse bytes are: \'extended\', \'high\', and \'low\'')
    # Prepare program string
    cmd = "%s -p %s -c avrispv2 -P %s -v -U %s:w:0x%02X:m" % (MCU_TOOL, mcu, port, MCU_FUSE_TAG[fuse], byte)
    # Try to program the fuses
    ret = subprocess.run(cmd, shell=True, capture_output=True)
    # Check if programming was successful
    if ret.returncode==0:
        return True
    else:
        return False


###
# Program the extended fuses of the MCU.
#
# @param[in] byte Fuse byte.
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] True in case of success; otherwise False.
def MCU_set_efuse(byte, port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    return _mcu_set_fuse('extended', byte, port, mcu)


###
# Program the high fuses of the MCU.
#
# @param[in] byte Fuse byte.
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] True in case of success; otherwise False.
def MCU_set_hfuse(byte, port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    return _mcu_set_fuse('high', byte, port, mcu)


###
# Program the low fuses of the MCU.
#
# @param[in] byte Fuse byte.
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] True in case of success; otherwise False.
def MCU_set_lfuse(byte, port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    # Try to program the fuses
    return _mcu_set_fuse('low', byte, port, mcu)


###
# Program the CLK source of the MCU.
#
# @param[in] src Clock source (INT/EXT).
# @param[in] div8_en Enable clock division by 8.
# @param[in] ckout_en Enable clock output (CKOUT).
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] True in case of success; otherwise False.
def MCU_set_clksrc(src, div8_en=False, ckout_en=False, port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    # Check if the serial interface exists
    if not os.path.exists(port):
        return False
    # Check if clock source is valid
    if (src<MCU_CLK_INT) or (src>MCU_CLK_EXT):
        raise ValueError('Valid clock sources are: MCU_CLK_INT (0) and MCU_CLK_EXT (1)')
    # Start with 0x00
    byte = 0x00
    # Internal oscillator
    if src==MCU_CLK_INT:
        # Set CKSEL to 0010
        byte |= (0b0010<<MCU_FL_CKSEL_OFFSET)
        # Set SUT to 10
        byte |= (0b10<<MCU_FL_SUT_OFFSET)
    # External oscillator
    else:
        # Set CKSEL to 1111
        byte |= (0b1111<<MCU_FL_CKSEL_OFFSET)
        # Set SUT to 11
        byte |= (0b11<<MCU_FL_SUT_OFFSET)
    # Set the CKDIV8 bit
    if not div8_en:
        byte |= 0x80
    # Set the CKOUT bit
    if not ckout_en:
        byte |= 0x40
    # Write the low fuses
    return MCU_set_lfuse(byte, port, mcu)


###
# Erase the MCU.
#
# @param[in] port Serial port to be used.
# @param[in] mcu MCU model for AVRDUDE.
# @param[out] True in case of success; otherwise False.
def mcu_erase(port=PORT_DEFAULT, mcu=MCU_DEFAULT):
    # Check if the serial interface exists
    if not os.path.exists(port):
        return False
    # Prepare erase string
    cmd = "%s -p %s -c avrispv2 -P %s -v -e" % (MCU_TOOL, mcu, port)
    # Try to erase the MCU
    ret = subprocess.run(cmd, shell=True, capture_output=True)
    # Check if erasing was successful
    if ret.returncode==0:
        return True
    else:
        return False


###
# Reset the MCU (via GPIO).
#
# @param[in] rst_pin GPIO pin for RST signal (BCM; default: 23).
# @param[out] True in case of success; otherwise False.
def mcu_reset(rst_pin=23):
    # Set RST to output
    GPIO.setup(rst_pin, GPIO.OUT)
    # Pull the RST line down
    GPIO.output(rst_pin, 0)
    # Wait for 500ms
    time.sleep(0.5)
    # Set RST line back to "1"
    GPIO.output(rst_pin, 1)
    # Release the RST line
    GPIO.setup(rst_pin, GPIO.IN)
