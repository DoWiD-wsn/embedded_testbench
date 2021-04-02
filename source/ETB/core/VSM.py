#####
# @package VSM
# @brief   VSM voltage scaling module (4x)
#
# Package containing the VSM voltage scaling module class used on the ETB.
#
# @file     /etb/core/VSM.py
# @author   $Author: Dominik Widhalm $
# @version  $Revision: 1.0 $
# @date     $Date: 2021/04/01 $
#
# @example  vsm = VSM()                     # Get an instance with default enable GPIOs
# @example  vsm.CH1_set_V(3.3)              # Set the voltage of channel 1
# @example  vsm.CH1_enable()                # Enable channel 1
# @example  volt = vsm.CH1_get_V()          # Read the voltage of channel 1 in volts (V)
# @example  curr = vsm.CH1_get_mA()         # Read the current of channel 1 in milliamps (mA)
# @example  vsm.CH1_disable()               # Disable channel 1
#####


##### LIBRARIES #####
# time (for sleep method)
import time
# Import required (local) modules
import .INA219
import .MIC24045
import .TCA9548A


##### GLOBAL VARIABLES #####
# Enable GPIOs
VSM_GPIO_EN1 = 5
VSM_GPIO_EN2 = 6
VSM_GPIO_EN3 = 19
VSM_GPIO_EN4 = 26


#####
# @class    VSM
# @brief    VSM voltage scaling module (4x)
#
# Class for the VSM voltage scaling module used on the ETB.
class VSM(object):
    ###
    # The constructor.
    #
    # @param[in] self The object pointer.
    # @param[in] enX GPIO pin for the enable signal of module X (in BCM numbering)
    def __init__(self, en1=VSM_GPIO_EN1, en2=VSM_GPIO_EN2, en3=VSM_GPIO_EN3, en4=VSM_GPIO_EN4):
        # @var __mux
        # Multiplexer object
        self.__mux = TCA9548A()
        # @var __mic[]
        # MIC objects (0-3)
        self.__mic = [None]
        self.__mic[1] = MIC24045(gpio=en1)
        self.__mic[2] = MIC24045(gpio=en2)
        self.__mic[3] = MIC24045(gpio=en3)
        self.__mic[4] = MIC24045(gpio=en4)
        # @var __ina[]
        # INA object (0-3)
        self.__ina = [None]
        self.__ina[1] = INA219()
        self.__ina[2] = INA219()
        self.__ina[3] = INA219()
        self.__ina[4] = INA219()


    ###
    # En/Disable a given channel (MIC).
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[in] enabled Enable (1) or disable (0)
    def _set_enable(self, channel, enabled):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Check if channel should be enabled or disabled
        if enabled:
            # Enable the MIC (GPIO)
            self.__mic[channel].enable()
        else:
            # Disable the MIC (GPIO)
            self.__mic[channel].disable()
        # Select the channel
        self.__mux.select(channel)
        # Check if MIC is really enabled
        ret = self.__mic[channel].is_enabled()
        # Deselect the channel
        self.__mux.select(0)
        # Return the result
        return ret
    ###
    # Enable channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH1_enable(self):
        return self._set_enable(1,1)
    ###
    # Disable channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH1_disable(self):
        return self._set_enable(1,0)
    ###
    # Enable channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH2_enable(self):
        return self._set_enable(2,1)
    ###
    # Disable channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH2_disable(self):
        return self._set_enable(2,0)
    ###
    # Enable channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH3_enable(self):
        return self._set_enable(3,1)
    ###
    # Disable channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH3_disable(self):
        return self._set_enable(3,0)
    # Enable channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH4_enable(self):
        return self._set_enable(4,1)
    ###
    # Disable channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    def CH4_disable(self):
        return self._set_enable(4,0)
    # Enable all channels (wrapper).
    #
    # @param[in] self The object pointer.
    def ALL_enable(self):
        for i in range(1,5):
            if not self._set_enable(i,1)
                return False
        return True
    ###
    # Disable all channel (wrapper).
    #
    # @param[in] self The object pointer.
    def ALL_disable(self):
        for i in range(1,5):
            if not self._set_enable(i,0)
                return False
        return True


    ###
    # Set the current limit of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[in] ilim Current limit for the MIC (default: 2A)
    def _limit_A(self, channel, ilim=2):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        self.__mux.select(channel)
        # Set the MIC current limit
        self.__mic[channel].set_current_limit(ilim)
        # Deselect the channel
        self.__mux.select(0)
    ###
    # Set the current limit of channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] ilim Current limit for the MIC (default: 2A)
    def CH1_limit_A(self, ilim=2):
        return self._limit_A(1,ilim)
    ###
    # Set the current limit of channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] ilim Current limit for the MIC (default: 2A)
    def CH2_limit_A(self, ilim=2):
        return self._limit_A(2,ilim)
    ###
    # Set the current limit of channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] ilim Current limit for the MIC (default: 2A)
    def CH3_limit_A(self, ilim=2):
        return self._limit_A(3,ilim)
    ###
    # Set the current limit of channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] ilim Current limit for the MIC (default: 2A)
    def CH4_limit_A(self, ilim=2):
        return self._limit_A(4,ilim)
    ###
    # Set the current limit of all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] ilim Current limit for the MIC (default: 2A)
    def ALL_limit_A(self, ilim=2):
        for i in range(1,5):
            if not self._limit_A(i,ilim)
                return False
        return True


    ###
    # Calibrate the INA of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[in] imax Maximum current for the INA (default: 400mA)
    def _calibrate_A(self, channel, imax=INA219_CAL_400MA):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        self.__mux.select(channel)
        # Set the MIC current limit
        self.__ina[channel].calibrate(imax)
        # Deselect the channel
        self.__mux.select(0)
    ###
    # Calibrate channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] imax Maximum current for the INA (default: 400mA)
    def CH1_calibrate_A(self, imax=INA219_CAL_400MA):
        return self._calibrate_A(1,imax)
    ###
    # Calibrate channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] imax Maximum current for the INA (default: 400mA)
    def CH2_calibrate_A(self, imax=INA219_CAL_400MA):
        return self._calibrate_A(2,imax)
    ###
    # Calibrate channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] imax Maximum current for the INA (default: 400mA)
    def CH3_calibrate_A(self, imax=INA219_CAL_400MA):
        return self._calibrate_A(3,imax)
    ###
    # Calibrate channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] imax Maximum current for the INA (default: 400mA)
    def CH4_calibrate_A(self, imax=INA219_CAL_400MA):
        return self._calibrate_A(4,imax)
    ###
    # Calibrate all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] imax Maximum current for the INA (default: 400mA)
    def ALL_calibrate_A(self, imax=INA219_CAL_400MA):
        for i in range(1,5):
            if not self._calibrate_A(i,imax)
                return False
        return True

    ###
    # Set the vout value of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[in] value Decimal value of the vout register
    def _set_vout(self, channel, value):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        self.__mux.select(channel)
        # Set the MIC current limit
        self.__mic[channel].set_output_voltage(value)
        # Deselect the channel
        self.__mux.select(0)
    ###
    # Set the vout value of channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] value Decimal value of the vout register
    def CH1_set_decimal_V(self, value):
        return self._set_vout(1,value)
    ###
    # Set the vout value of channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] value Decimal value of the vout register
    def CH2_set_decimal_V(self, value):
        return self._set_vout(2,value)
    ###
    # Set the vout value of channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] value Decimal value of the vout register
    def CH3_set_decimal_V(self, value):
        return self._set_vout(3,value)
    ###
    # Set the vout value of channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] value Decimal value of the vout register
    def CH4_set_decimal_V(self, value):
        return self._set_vout(4,value)
    ###
    # Set the vout value of all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] value Decimal value of the vout register
    def ALL_set_decimal_V(self, value):
        for i in range(1,5):
            if not self._set_vout(i,value)
                return False
        return True


    ###
    # Set the output voltage (V) of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[in] volt Output voltage in volts (V)
    # @param[out] True in case of success; otherwise False.
    def _set_V(self, channel, volt):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Convert volt to decimal value
        value = self.__mic[channel].get_register_from_voltage(volt)
        # Check if valid value was returned
        if not value:
            return False
        # Set the vout value of a given channel.
        self._set_vout(1,value)
        # Everything ok
        return True
    ###
    # Set the output voltage (V) of channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] volt Output voltage in volts (V)
    # @param[out] True in case of success; otherwise False.
    def CH1_set_V(self, volt):
        return self._set_V(1,volt)
    ###
    # Set the output voltage (V) of channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] volt Output voltage in volts (V)
    # @param[out] True in case of success; otherwise False.
    def CH2_set_V(self, volt):
        return self._set_V(2,volt)
    ###
    # Set the output voltage (V) of channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] volt Output voltage in volts (V)
    # @param[out] True in case of success; otherwise False.
    def CH3_set_V(self, volt):
        return self._set_V(3,volt)
    ###
    # Set the output voltage (V) of channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] volt Output voltage in volts (V)
    # @param[out] True in case of success; otherwise False.
    def CH4_set_V(self, volt):
        return self._set_V(4,volt)
    ###
    # Set the output voltage (V) of all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] volt Output voltage in volts (V)
    # @param[out] True in case of success; otherwise False.
    def ALL_set_V(self, volt):
        for i in range(1,5):
            if not self._set_V(i,volt)
                return False
        return True


    ###
    # Check if power-is-good (MIC) of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[out] True in case of success; otherwise False.
    def _is_power_good(self, channel):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        self.__mux.select(channel)
        # Set the MIC current limit
        ret = self.__mic[channel].is_power_good()
        # Deselect the channel
        self.__mux.select(0)
        # Return the result
        return ret
    ###
    # Check if power-is-good (MIC) of channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def CH1_is_power_good(self):
        return self._is_power_good(1)
    ###
    # Check if power-is-good (MIC) of channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def CH2_is_power_good(self):
        return self._is_power_good(2)
    ###
    # Check if power-is-good (MIC) of channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def CH3_is_power_good(self):
        return self._is_power_good(3)
    ###
    # Check if power-is-good (MIC) of channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def CH4_is_power_good(self):
        return self._is_power_good(4)
    ###
    # Check if power-is-good (MIC) of all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] True in case of success; otherwise False.
    def ALL_is_power_good(self):
        for i in range(1,5):
            if not self._is_power_good(i)
                return False
        return True


    ###
    # Wait for power-is-good (MIC) with timeout [ms] of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[in] timeout Timeout in milliseconds (ms; default: 1s)
    # @param[out] True in case of success; otherwise False.
    def _wait_power_good(self, channel, timeout=1000):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Time-passed counter
        passed = 0
        # Wait for power-good
        while not self._is_power_good(channel):
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
    # Wait for power-is-good (MIC) with timeout [ms] of channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] timeout Timeout in milliseconds (ms; default: 1s)
    # @param[out] True in case of success; otherwise False.
    def CH1_wait_power_good(self,timeout=1000):
        return self._wait_power_good(1,timeout)
    ###
    # Wait for power-is-good (MIC) with timeout [ms] of channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] timeout Timeout in milliseconds (ms; default: 1s)
    # @param[out] True in case of success; otherwise False.
    def CH2_wait_power_good(self,timeout=1000):
        return self._wait_power_good(2,timeout)
    ###
    # Wait for power-is-good (MIC) with timeout [ms] of channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] timeout Timeout in milliseconds (ms; default: 1s)
    # @param[out] True in case of success; otherwise False.
    def CH3_wait_power_good(self,timeout=1000):
        return self._wait_power_good(3,timeout)
    ###
    # Wait for power-is-good (MIC) with timeout [ms] of channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] timeout Timeout in milliseconds (ms; default: 1s)
    # @param[out] True in case of success; otherwise False.
    def CH4_wait_power_good(self,timeout=1000):
        return self._wait_power_good(4,timeout)
    ###
    # Wait for power-is-good (MIC) with timeout [ms] of all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[in] timeout Timeout in milliseconds (ms; default: 1s)
    # @param[out] True in case of success; otherwise False.
    def ALL_wait_power_good(self,timeout=1000):
        # Time-passed counter
        passed = 0
        # Wait for power-good
        while not self.ALL_is_power_good():
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
    # Get the bus voltage (INA) of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[out] Voltage in volts (V) in case of success; otherwise False.
    def _get_V(self, channel):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        self.__mux.select(channel)
        # Set the MIC current limit
        volts = self.__ina[channel].get_bus_voltage_V()
        # Deselect the channel
        self.__mux.select(0)
        # Return the result
        return volts
    ###
    # Get the bus voltage (INA) of channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Voltage in volts (V) in case of success; otherwise False.
    def CH1_get_V(self):
        return self._get_V(1)
    ###
    # Get the bus voltage (INA) of channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Voltage in volts (V) in case of success; otherwise False.
    def CH2_get_V(self):
        return self._get_V(2)
    ###
    # Get the bus voltage (INA) of channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Voltage in volts (V) in case of success; otherwise False.
    def CH3_get_V(self):
        return self._get_V(3)
    ###
    # Get the bus voltage (INA) of channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Voltage in volts (V) in case of success; otherwise False.
    def CH4_get_V(self):
        return self._get_V(4)
    ###
    # Get the bus voltage (INA) of all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] List of voltages in volts (V) in case of success; otherwise False.
    def ALL_get_V(self):
        volts = ()
        for i in range(1,5):
            ret = self._get_V(i)
            if ret:
                volts.append(ret)
            else:
                return False
        return volts


    ###
    # Get the current (INA) of a given channel.
    #
    # @param[in] self The object pointer.
    # @param[in] channel Channel to be selected (1-4)
    # @param[out] Current in milliamps (mA) in case of success; otherwise False.
    def _get_mA(self, channel):
        # Check the given channel
        assert 1 <= channel <= 4, 'Channel can only be between 1 and 4'
        # Select the channel
        self.__mux.select(channel)
        # Set the MIC current limit
        amps = self.__ina[channel].get_current_mA()
        # Deselect the channel
        self.__mux.select(0)
        # Return the result
        return amps
    ###
    # Get the current (INA) of channel 1 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Current in milliamps (mA) in case of success; otherwise False.
    def CH1_get_mA(self):
        return self._get_mA(1)
    ###
    # Get the current (INA) of channel 2 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Current in milliamps (mA) in case of success; otherwise False.
    def CH2_get_mA(self):
        return self._get_mA(2)
    ###
    # Get the current (INA) of channel 3 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Current in milliamps (mA) in case of success; otherwise False.
    def CH3_get_mA(self):
        return self._get_mA(3)
    ###
    # Get the current (INA) of channel 4 (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] Current in milliamps (mA) in case of success; otherwise False.
    def CH4_get_mA(self):
        return self._get_mA(4)
    ###
    # Get the current (INA) of all channels (wrapper).
    #
    # @param[in] self The object pointer.
    # @param[out] List of currents in milliamps (mA) in case of success; otherwise False.
    def ALL_get_mA(self):
        amps = ()
        for i in range(1,5):
            ret = self._get_mA(i)
            if ret:
                amps.append(ret)
            else:
                return False
        return amps


    ###
    # Convert a voltage in volts (V) to the corresponding decimal value (MIC).
    #
    # @param[in] self The object pointer.
    # @param[in] volt Voltage in volts (V)
    # @param[out] Decimal value in case of success; otherwise False.
    def volt2dec(self, volt):
        # Return the result
        return self.__mic[1].get_register_from_voltage(volt)


    ###
    # Convert a decimal value to the corresponding voltage in volts (V) (MIC).
    #
    # @param[in] self The object pointer.
    # @param[in] decimal Decimal value for the MIC's vout
    # @param[out] Voltage in volts (V) in case of success; otherwise False.
    def dec2volt(self, decimal):
        # Return the result
        return self.__mic[1].get_voltage_from_register(decimal)
