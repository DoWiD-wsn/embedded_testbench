#####
# @brief   Embedded Testbench (ETB) module
#
# Module containing the embedded testbench (ETB) class.
#
# @file     /etb/ETB.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/30 $
#
# @note     Don't forget to enable I2C, e.g. with sudo raspi-config
#
# @example  For examples refer to the scripts in the examples directory
#####


##### LIBRARIES #####
### GLOBAL ###
# time (for sleep method)
import time

### ETB ###
# Core functionality
from ETB.core.INA219 import *
from ETB.core.VSM import *
from ETB.core.ADS1115 import *
# Miscy
from ETB.sens.JT103 import raw_to_degree


#####
# @class    ETB
# @brief    ETB embedded testbench
#
# Class for the VSM voltage scaling module used on the ETB.
class ETB(object):
    ###
    # The constructor.
    #
    # @param[in]    self            The object pointer.
    def __init__(self):
        # @var _vsm
        # voltage scaling module (with default enable lines)
        self._vsm = VSM()
        # @var _adc
        # onboard ADC (with default I2C address)
        self._adc = ADS1115()
        # @var _inaaux[]
        # auxiliary INA wattmeters
        self._inaaux = [None]*3
        self._inaaux[1] = INA219(0x41)
        self._inaaux[2] = INA219(0x44)
        # Calibrate the INA
        for i in range(1,3):
            # Check if MIC is really enabled
            self._inaaux[i].calibrate()


    ###
    # Check if a given output channel is enabled.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True if enabled; False otherwise
    def ch_is_enabled(self, channel):
        return self._vsm.ch_is_enabled(channel)


    ###
    # Enable a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True is enabled; False otherwise
    def ch_enable(self, channel):
        return self._vsm.ch_enable(channel)


    ###
    # Disable a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True is enabled; False otherwise
    def ch_disable(self, channel):
        return self._vsm.ch_disable(channel)


    # Enable all output channels.
    #
    # @param[in]    self            The object pointer.
    # @return       True is enabled; False otherwise
    def ch_enable_all(self):
        return self._vsm.ch_enable_all()


    ###
    # Disable all output channels.
    #
    # @param[in]    self            The object pointer.
    # @return       True is enabled; False otherwise
    def ch_disable_all(self):
        return self._vsm.ch_disable_all()


    ###
    # Set the current limit of a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    ilim            Current limit for the MIC (default: 2A)
    # @return       True in case of success; False otherwise
    def ch_limit_A(self, channel, ilim=2):
        return self._vsm.ch_limit_A(channel, ilim)


    ###
    # Set the current limit of all output channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    ilim            Current limit for the MIC (default: 2A)
    # @return       True in case of success; False otherwise
    def ch_limit_A_all(self, ilim=2):
        return self._vsm.ch_limit_A_all(ilim)


    ###
    # Calibrate a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    imax            Maximum current for the INA (default: 400mA)
    # @return       True in case of success; False otherwise
    def ch_calibrate_A(self, channel, imax=INA219_CAL_400MA):
        return self._vsm.ch_calibrate_A(channel, imax)


    ###
    # Calibrate all output channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    imax            Maximum current for the INA (default: 400mA)
    # @return       True in case of success; False otherwise
    def ch_calibrate_A_all(self, imax=INA219_CAL_400MA):
        return self._vsm.ch_calibrate_A_all(imax)


    ###
    # Set the Vout value of a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    value           Decimal value of the vout register
    # @return       True in case of success; False otherwise
    def ch_set_V_decimal(self, channel, value):
        return self._vsm.ch_set_V_decimal(channel, value)


    ###
    # Set the Vout value of all output channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    value           Decimal value of the vout register
    # @return       True in case of success; False otherwise
    def ch_set_V_decimal_all(self, value):
        return self._vsm.ch_set_V_decimal_all(value)


    ###
    # Set the output voltage (V) of a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    volt            Output voltage in volts (V)
    # @return       True in case of success; False otherwise
    def ch_set_V(self, channel, volt):
        return self._vsm.ch_set_V(channel, volt)


    ###
    # Set the output voltage (V) of all output channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    volt            Output voltage in volts (V)
    # @return       True in case of success; False otherwise
    def ch_set_V_all(self, volt):
        return self._vsm.ch_set_V_all(volt)


    ###
    # Check if power-is-good (MIC) of output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True in case of success; False otherwise
    def ch_is_power_good(self, channel):
        return self._vsm.ch_is_power_good(channel)


    ###
    # Check if power-is-good (MIC) of all output channels.
    #
    # @param[in]    self            The object pointer.
    # @return       True in case of success; False otherwise
    def ch_is_power_good_all(self):
        return self._vsm.ch_is_power_good_all()


    ###
    # Wait for power-is-good (MIC) with timeout [ms] of output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    timeout         Timeout in milliseconds (ms; default: 1s)
    # @return       True in case of success; False otherwise
    def ch_wait_power_good(self,channel,timeout=1000):
        return self._vsm.ch_wait_power_good(channel,timeout)


    ###
    # Wait for power-is-good (MIC) with timeout [ms] of all output channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    timeout         Timeout in milliseconds (ms; default: 1s)
    # @return       True in case of success; False otherwise
    def ch_wait_power_good_all(self,timeout=1000):
        return self._vsm.ch_wait_power_good_all(timeout)


    ###
    # Get the bus voltage (INA) of a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       Voltage in volts (V) in case of success; otherwise False.
    def ch_get_V(self, channel):
        return self._vsm.ch_get_V(channel)


    ###
    # Get the bus voltage (INA) of all output channels.
    #
    # @param[in]    self        The object pointer.
    # @return       List of voltages in volts (V) in case of success; otherwise False.
    def ch_get_V_all(self):
        return self._vsm.ch_get_V_all()


    ###
    # Get the current (INA) of a given output channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       Current in milliamps (mA) in case of success; otherwise False.
    def ch_get_mA(self, channel):
        return self._vsm.ch_get_mA(channel)


    ###
    # Get the current (INA) of all output channels.
    #
    # @param[in]    self            The object pointer.
    # @return       List of currents in milliamps (mA) in case of success; otherwise False.
    def ch_get_mA_all(self):
        return self._vsm.ch_get_mA_all()


    ###
    # Convert a voltage in volts (V) to the corresponding decimal value (MIC).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    volt            Voltage in volts (V)
    # @preturn      Decimal value in case of success; otherwise False.
    def volt2dec(self, volt):
        return self._vsm.volt2dec(volt)


    ###
    # Convert a decimal value to the corresponding voltage in volts (V) (MIC).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    decimal         Decimal value for the MIC's vout
    # @return       Voltage in volts (V) in case of success; otherwise False.
    def dec2volt(self, decimal):
        return self._vsm.dec2volt(decimal)


    ###
    # Read a single ADC channel and return signed integer result.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         ADC channel to be queried
    # @param[in]    gain            Gain to be used
    # @param[in]    data_rate       Data rate to be used
    # @return       Signed conversion value in case of success; otherwise False.
    def read_channel(self, channel, gain=1, data_rate=ADS1115_DR_DEFAULT):
        return self._adc.read_channel(channel, gain, data_rate)


    ###
    # Read the temperature value of a thermistor input (degree Celsius).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    thermistor      Thermistor input (ADC channel; 0-1)
    # @param[out]   Temperature value [°C] in case of success; otherwise False.
    def read_thermistor(self, thermistor):
        # Check the given thermistor channel
        assert 0 <= thermistor <= 1, 'Thermistor channel can only be between 0 and 1'
        # Read the raw ADC thermistor
        data = self._adc.read_channel(thermistor)
        # Check if the ADC returned a valid conversion result
        if data is not False:
            # Return the temperature (in degree Celsius)
            return raw_to_degree(data)
        else:
            return False


    ###
    # Calibrate a given auxiliary channel (1-2).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    imax            Maximum current for the INA (default: 400mA)
    # @return       True in case of success; False otherwise
    def ch_calibrate_A(self, channel, imax=INA219_CAL_400MA):
        # Check the given thermistor channel
        assert 1 <= channel <= 2, 'Auxiliary channel can only be 1 or 2'
        # Get the voltage
        return self._inaaux[channel].calibrate(imax)


    ###
    # Get the bus voltage (INA) of a given auxiliary channel (1-2).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-2)
    # @return       Voltage in volts (V) in case of success; otherwise False.
    def aux_get_V(self, channel):
        # Check the given thermistor channel
        assert 1 <= channel <= 2, 'Auxiliary channel can only be 1 or 2'
        # Get the voltage
        return self._inaaux[channel].get_bus_voltage_V()


    ###
    # Get the current (INA) of a given auxiliary channel (1-2).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-2)
    # @return       Current in milliamps (mA) in case of success; otherwise False.
    def aux_get_mA(self, channel):
        assert 1 <= channel <= 2, 'Auxiliary channel can only be 1 or 2'
        # Get the current
        return self._inaaux[channel].get_current_mA()
