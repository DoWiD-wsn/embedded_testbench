#####
# @brief   VSM - voltage scaling module
#
# Module containing the voltage scaling module (VSM) class used on the ETB.
#
# @file     /etb/core/VSM.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/29 $
#
# @example  vsm = VSM()                     # Get an instance with default enable GPIOs
# @example  vsm.ch_set_V(1, 3.3)            # Set the voltage of channel 1
# @example  vsm.ch_enable(1)                # Enable channel 1
# @example  volt = vsm.ch_get_V(1)          # Read the voltage of channel 1 in volts (V)
# @example  curr = vsm.ch_get_mA(1)         # Read the current of channel 1 in milliamps (mA)
# @example  vsm.ch_disable(1)               # Disable channel 1
#####


##### LIBRARIES #####
# time (for sleep method)
import time
# Import required (local) modules
from ETB.core.INA219 import *
from ETB.core.MIC24045 import *
from ETB.core.TCA9548A import *


##### GLOBAL VARIABLES #####
# Enable GPIOs
VSM_GPIO_EN1 = 5
VSM_GPIO_EN2 = 6
VSM_GPIO_EN3 = 19
VSM_GPIO_EN4 = 26


#####
# @class    VSM
# @brief    VSM voltage scaling module
#
# Class for the VSM voltage scaling module used on the ETB.
class VSM(object):
    ###
    # The constructor.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    enX             GPIO pin for the enable signal of module X (in BCM numbering)
    def __init__(self, en1=VSM_GPIO_EN1, en2=VSM_GPIO_EN2, en3=VSM_GPIO_EN3, en4=VSM_GPIO_EN4):
        # @var _mux
        # Multiplexer object
        self._mux = TCA9548A()
        # @var _mic[]
        # MIC objects (1-4)
        self._mic = [None]*5
        self._mic[1] = MIC24045(gpio=en1)
        self._mic[2] = MIC24045(gpio=en2)
        self._mic[3] = MIC24045(gpio=en3)
        self._mic[4] = MIC24045(gpio=en4)
        # @var _ina[]
        # INA object (1-4)
        self._ina = [None]*5
        self._ina[1] = INA219()
        self._ina[2] = INA219()
        self._ina[3] = INA219()
        self._ina[4] = INA219()
        # Calibrate the INA
        for i in range(1,5):
            # Select the channel
            self._mux.select(i)
            # Check if MIC is really enabled
            self._ina[i].calibrate()
            # Deselect the channel
            self._mux.select(0)


    ###
    # Check if a given channel (MIC) is enabled.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True if enabled; False otherwise
    def ch_is_enabled(self, channel):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        self._mux.select(channel)
        # Check if MIC is enabled
        ret = self._mic[channel].is_enabled()
        # Deselect the channel
        self._mux.select(0)
        # Return the result
        return ret


    ###
    # En/Disable a given channel (MIC).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    enabled         Enable (1) or disable (0)
    # @return       True if enabled; False otherwise
    def _set_enable(self, channel, enabled):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Check if channel should be enabled or disabled
        if enabled:
            # Enable the MIC (GPIO)
            self._mic[channel].enable()
        else:
            # Disable the MIC (GPIO)
            self._mic[channel].disable()
        # Check if the channel is enabled now
        return self.ch_is_enabled(channel)


    ###
    # Enable the given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True is enabled; False otherwise
    def ch_enable(self, channel):
        return self._set_enable(channel,1)


    ###
    # Disable the given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True is enabled; False otherwise
    def ch_disable(self, channel):
        return self._set_enable(channel,0)


    # Enable all channels.
    #
    # @param[in]    self            The object pointer.
    # @return       True is enabled; False otherwise
    def ch_enable_all(self):
        for i in range(1,5):
            if self.ch_enable(i) is False:
                return False
        return True


    ###
    # Disable all channels.
    #
    # @param[in]    self            The object pointer.
    # @return       True is enabled; False otherwise
    def ch_disable_all(self):
        for i in range(1,5):
            if self.ch_disable(i) is False:
                return False
        return True


    ###
    # Set the current limit of a given channel.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    ilim            Current limit for the MIC (default: 2A)
    # @return       True in case of success; False otherwise
    def _limit_A(self, channel, ilim=2):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        if rself._mux.select(channel) is False:
            return False
        # Set the MIC current limit
        if self._mic[channel].set_current_limit(ilim) is False:
            return False
        # Deselect the channel
        if self._mux.select(0) is False:
            return False
        # Done
        return True


    ###
    # Set the current limit of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    ilim            Current limit for the MIC (default: 2A)
    # @return       True in case of success; False otherwise
    def ch_limit_A(self, channel, ilim=2):
        return self._limit_A(channel, ilim)


    ###
    # Set the current limit of all channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    ilim            Current limit for the MIC (default: 2A)
    # @return       True in case of success; False otherwise
    def ch_limit_A_all(self, ilim=2):
        for i in range(1,5):
            if self.ch_limit_A(i, ilim) is False:
                return False
        return True


    ###
    # Calibrate the INA of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    imax            Maximum current for the INA (default: 400mA)
    # @return       True in case of success; False otherwise
    def _calibrate_A(self, channel, imax=INA219_CAL_400MA):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        if self._mux.select(channel) is False:
            return False
        # Set the MIC current limit
        if self._ina[channel].calibrate(imax) is False:
            return False
        # Deselect the channel
        if self._mux.select(0) is False:
            return False
        # Done
        return True


    ###
    # Calibrate a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    imax            Maximum current for the INA (default: 400mA)
    # @return       True in case of success; False otherwise
    def ch_calibrate_A(self, channel, imax=INA219_CAL_400MA):
        return self._calibrate_A(channel,imax)


    ###
    # Calibrate all channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    imax            Maximum current for the INA (default: 400mA)
    # @return       True in case of success; False otherwise
    def ch_calibrate_A_all(self, imax=INA219_CAL_400MA):
        for i in range(1,5):
            if self.ch_calibrate_A(i,imax) is False:
                return False
        return True


    ###
    # Set the vout value of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    value           Decimal value of the vout register
    # @return       True in case of success; False otherwise
    def _set_vout(self, channel, value):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        if self._mux.select(channel) is False:
            return False
        # Set the MIC current limit
        if self._mic[channel].set_output_voltage(value) is False:
            return False
        # Deselect the channel
        if self._mux.select(0) is False:
            return False
        # Done
        return True


    ###
    # Set the Vout value of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    value           Decimal value of the vout register
    # @return       True in case of success; False otherwise
    def ch_set_V_decimal(self, channel, value):
        return self._set_vout(channel,value)


    ###
    # Set the Vout value of all channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    value           Decimal value of the vout register
    # @return       True in case of success; False otherwise
    def ch_set_V_decimal_all(self, value):
        for i in range(1,5):
            if self.ch_set_V_decimal(i,value) is False:
                return False
        return True


    ###
    # Set the output voltage (V) of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    volt            Output voltage in volts (V)
    # @return       True in case of success; False otherwise
    def _set_V(self, channel, volt):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Convert volt to decimal value
        value = self._mic[channel].get_register_from_voltage(volt)
        # Check if valid value was returned
        if value is False:
            return False
        # Set the vout value of a given channel.
        return self._set_vout(channel,value)


    ###
    # Set the output voltage (V) of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    volt            Output voltage in volts (V)
    # @return       True in case of success; False otherwise
    def ch_set_V(self, channel, volt):
        return self._set_V(channel, volt)


    ###
    # Set the output voltage (V) of all channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    volt            Output voltage in volts (V)
    # @return       True in case of success; False otherwise
    def ch_set_V_all(self, volt):
        for i in range(1,5):
            if self.ch_set_V(i,volt) is False:
                return False
        return True


    ###
    # Check if power-is-good (MIC) of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True in case of success; False otherwise
    def _is_power_good(self, channel):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        if self._mux.select(channel) is False:
            return False
        # Set the MIC current limit
        ret = self._mic[channel].is_power_good()
        # Check return value
        if ret is False:
            return False
        # Deselect the channel
        if self._mux.select(0) is False:
            return False
        # Return the result
        return ret


    ###
    # Check if power-is-good (MIC) of channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       True in case of success; False otherwise
    def ch_is_power_good(self, channel):
        return self._is_power_good(channel)


    ###
    # Check if power-is-good (MIC) of all channels.
    #
    # @param[in]    self            The object pointer.
    # @return       True in case of success; False otherwise
    def ch_is_power_good_all(self):
        for i in range(1,5):
            if self._is_power_good(i) is False:
                return False
        return True


    ###
    # Wait for power-is-good (MIC) with timeout [ms] of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    timeout         Timeout in milliseconds (ms; default: 1s)
    # @return       True in case of success; False otherwise
    def _wait_power_good(self, channel, timeout=1000):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Time-passed counter
        passed = 0
        # Wait for power-good
        while self._is_power_good(channel) is False:
            # check if timeout has already been reached
            if passed >= timeout:
                # Timeout
                return False
            # wait for 10ms
            time.sleep(0.01)
            # increment timeout counter by 10ms
            passed += 10
        return True


    ###
    # Wait for power-is-good (MIC) with timeout [ms] of channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @param[in]    timeout         Timeout in milliseconds (ms; default: 1s)
    # @return       True in case of success; False otherwise
    def ch_wait_power_good(self,channel,timeout=1000):
        return self._wait_power_good(channel,timeout)


    ###
    # Wait for power-is-good (MIC) with timeout [ms] of all channels.
    #
    # @param[in]    self            The object pointer.
    # @param[in]    timeout         Timeout in milliseconds (ms; default: 1s)
    # @return       True in case of success; False otherwise
    def ch_wait_power_good_all(self,timeout=1000):
        # Time-passed counter
        passed = 0
        # Wait for power-good
        while self.ALL_is_power_good() is False:
            # check if timeout has already been reached
            if passed >= timeout:
                # Timeout
                return False
            # wait for 10ms
            time.sleep(0.01)
            # increment timeout counter by 10ms
            passed += 10
        # Everything ok
        return True


    ###
    # Get the bus voltage (INA) of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       Voltage in volts (V) in case of success; otherwise False.
    def _get_V(self, channel):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        if self._mux.select(channel) is False:
            return False
        # Set the MIC current limit
        volts = self._ina[channel].get_bus_voltage_V()
        # Check return value
        if volts is False:
            return False
        # Deselect the channel
        if self._mux.select(0) is False:
            return False
        # Return the result
        return volts


    ###
    # Get the bus voltage (INA) of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       Voltage in volts (V) in case of success; otherwise False.
    def ch_get_V(self, channel):
        return self._get_V(channel)


    ###
    # Get the bus voltage (INA) of all channels.
    #
    # @param[in]    self        The object pointer.
    # @return       List of voltages in volts (V) in case of success; otherwise False.
    def ch_get_V_all(self):
        volts = ()
        for i in range(1,5):
            ret = self.ch_get_V(i)
            if ret:
                volts.append(ret)
            else:
                return False
        return volts


    ###
    # Get the current (INA) of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       Current in milliamps (mA) in case of success; otherwise False.
    def _get_mA(self, channel):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        if self._mux.select(channel) is False:
            return False
        # Set the MIC current limit
        amps = self._ina[channel].get_current_mA()
        # Check return value
        if amps is False:
            return False
        # Deselect the channel
        if self._mux.select(0) is False:
            return False
        # Return the result
        return amps


    ###
    # Get the current (INA) of a given channel (1-4).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    channel         Channel to be selected (1-4)
    # @return       Current in milliamps (mA) in case of success; otherwise False.
    def ch_get_mA(self, channel):
        return self._get_mA(channel)


    ###
    # Get the current (INA) of all channels.
    #
    # @param[in]    self            The object pointer.
    # @return       List of currents in milliamps (mA) in case of success; otherwise False.
    def ch_get_mA_all(self):
        amps = ()
        for i in range(1,5):
            ret = self.ch_get_mA(i)
            if ret:
                amps.append(ret)
            else:
                return False
        return amps


    ###
    # Convert a voltage in volts (V) to the corresponding decimal value (MIC).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    volt            Voltage in volts (V)
    # @preturn      Decimal value in case of success; otherwise False.
    def volt2dec(self, volt):
        # Return the result
        return self._mic[1].get_register_from_voltage(volt)


    ###
    # Convert a decimal value to the corresponding voltage in volts (V) (MIC).
    #
    # @param[in]    self            The object pointer.
    # @param[in]    decimal         Decimal value for the MIC's vout
    # @return       Voltage in volts (V) in case of success; otherwise False.
    def dec2volt(self, decimal):
        # Return the result
        return self._mic[1].get_voltage_from_register(decimal)
