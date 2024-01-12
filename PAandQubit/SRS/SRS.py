# Stanford_Research_Systems,SIM900,s/n152741,ver3.6


#########################################################################################################
#              Methods               :              Description
#                                    :
#       [1. Basic methods]           :
# 1.1 | __init__ ................... : initializes object attributes in a class.
# 1.2 | get_name ................... : Returns the instrument identification.
# 1.3 | reset ...................... : Sets the instrument to a defined default status.
# 1.4 | clear ...................... : Clear status.
#                                    :
#                                    :
#       [2. Modulation]              :
# 2.1 | transition_type ............ : Sets the transition mode for the pulse signal.
# 2.2 | pul_gen_params ............. : Sets the period, delay and width of pulse.
# 2.3 | pul_gen_mode ............... : Selects the mode for the pulse modulation.
# 2.4 | pul_trig_mode .............. : Selects a trigger mode for generating the modulation signal.
# 2.5 | pul_state .................. : Activates pulse modulation (1: ON, 0: OFF).
#                                    :
#                                    :
#       [3. Frequency]               :
# 3.1 | RF_freq .................... : Sets the frequency of the RF output signal.
#                                    :
#                                    :
#       [4. Level]                   :
# 4.1 | RF_state ................... : Activates the RF output signal (1: ON, 0: OFF).                  
# 4.2 | RF_lvl_ampl ................ : Sets the amplitude level of the RF output signal.
#                                    :
#########################################################################################################à



import pyvisa
import numpy as np
import time
import h5py 



class SIM900:

# 1.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def __init__(self):

        self._resource = None
        self._connect_success = False
        self._sleep = 1

        try:
            rm = pyvisa.ResourceManager()
            self._resource = rm.open_resource("ASRL34::INSTR")
            self._connect_success = True
            print("Connection successful!")
        except pyvisa.Error as e:
            print(f"Unable to establish a connection: {e}")

# 1.2 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def get_name(self):
        if self._connect_success:
            print(self._resource.query('*IDN?'))
        else:
            print("Error: No active connection.")
        
# 1.3 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def reset(self):
        if self._connect_success:
            self._resource.write('*RST')
            time.sleep(self._sleep)
        else:
            print("Error: No active connection.")

# 1.4 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def clear(self):
        if self._connect_success:
            self._resource.write('*CLS')     
            time.sleep(self._sleep)
        else:
            print("Error: No active connection.")


    def module_connect(self, slot: int, name: str):                 #connessione a uno degli 8 slot
        if self._connect_success:
            self._resource.write(f'CONN {slot}, "{name}"')     
        else:
            print("Error: No active connection.")

    def set_voltage(self, voltage: float):
        """Input : Volt"""
        if self._connect_success:
            self._resource.write(f'VOLT {voltage}')
        else:
            print("Error: No active connection.")    

    def output_on(self):
        """Turn the output on."""
        self._resource.write("OPON")

    def output_off(self):
        """Turn the output on."""
        self._resource.write("OPOF")

    

   