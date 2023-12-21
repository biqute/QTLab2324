# MANUAL: https://www.keysight.com/it/en/assets/9018-03714/service-manuals/9018-03714.pdf?success=true
# pag 212


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
#       [2. SOURce Subsystem]

#                                    :
#########################################################################################################à



import pyvisa
import numpy as np
import time
import h5py 



class SMA100B:

# 1.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def __init__(self):

        self._resource = None
        self._connect_success = False
        self._sleep = 1

        try:
            rm = pyvisa.ResourceManager()
            self._resource = rm.open_resource(f"GPIB0::10::INSTR")
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


    def set_frequency(self, freq: float, ch = 1):
        if self._connect_success:
            self._resource.write(f'SOUR{ch}:FREQ {freq}')
        else:
            print("Error: No active connection.")

    def set_amplitude(self, ampl: float, ch = 1):
        if self._connect_success:
            self._resource.write(f'SOUR{ch}:VOLT {ampl}')
        else:
            print("Error: No active connection.")

    def set_phase(self, phase: float, ch = 1):
        if self._connect_success:
            self._resource.write(f'SOUR{ch}:PHAS {phase}')
        else:
            print("Error: No active connection.") 

    def channel_state(self, ch = 1, state = 1):
        if self._connect_success:
            self._resource.write(f'OUTP{ch} {state}')
        else:
            print("Error: No active connection.") 