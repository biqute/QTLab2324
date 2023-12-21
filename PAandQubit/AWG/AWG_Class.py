# MANUAL    :       https://www.keysight.com/it/en/assets/9018-03714/service-manuals/9018-03714.pdf?success=true
# Pag 212   :       Alphabetical List of SCPI Commands and Queries



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
#       [2. SOURce Subsystem]        :
# 2.1 | set_frequency .............. : Sets output frequency.
# 2.2 | set_amplitude .............. : Sets output amplitude.
# 2.3 | set_offset ................. :
# 2.4 | set_phase .................. : Sets waveform's phase offset angle.
# 2.5 | set_function ............... : Selects the output function.
#                                    :
#                                    :
#       [3. OUTPut Subsystem]        :
# 3.1 | channel_state .............. : Enables or disables the front panel output connector.
#                                    :
#                                    :
#       [4. APPLy Subsystem]         :
# 4.1 | set_waveform ............... : Configure entire waveforms with one command.
#                                    :
#########################################################################################################à



import pyvisa
import time



class Ks_33500B:

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


# [2. SOURce Subsystem] ----------------------------------------------------------------------------------------------------------------------------- #
            
# 2.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #
            
    def set_frequency(self, freq: float, ch: int = 1):
        # sjkasdnaksjnd
        if self._connect_success:
            self._resource.write(f'SOUR{ch}:FREQ {freq}')
        else:
            print("Error: No active connection.")

# 2.2 ----------------------------------------------------------------------------------------------------------------------------------------------- #
            
    def set_amplitude(self, ampl: float, ch: int = 1):
        if self._connect_success:
            self._resource.write(f'SOUR{ch}:VOLT {ampl}')
        else:
            print("Error: No active connection.")

# 2.2 ----------------------------------------------------------------------------------------------------------------------------------------------- #
            
    def set_offset(self, offs: float, ch: int = 1):
        if self._connect_success:
            self._resource.write(f'SOUR{ch}:VOLT:OFFS {offs}')
        else:
            print("Error: No active connection.")

# 2.4 ----------------------------------------------------------------------------------------------------------------------------------------------- #
            
    def set_phase(self, phase: float, ch: int = 1):
        if self._connect_success:
            self._resource.write(f'SOUR{ch}:PHAS {phase}')
        else:
            print("Error: No active connection.") 

# 2.5 ----------------------------------------------------------------------------------------------------------------------------------------------- #
            
    def set_function(self, fun: str, ch: int = 1):
        if self._connect_success:
            if fun in {'SIN', 'SQU', 'TRI', 'RAMP', 'PULS', 'PRBS', 'NOIS', 'ARB', 'DC'}:
                self._resource.write(f'SOUR{ch}:FUNC {fun}')
            else:
                print("Error. Invalid string mode. Write 'SIN', 'SQU', 'TRI', 'RAMP', 'PULS', 'PRBS', 'NOIS', 'ARB', or 'DC'")
        else:
            print("Error: No active connection.") 


# [3. OUTPut Subsystem] ----------------------------------------------------------------------------------------------------------------------------- #

# 3.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def channel_state(self, ch: int = 1, state: int = 1):
        if self._connect_success:
            self._resource.write(f'OUTP{ch} {state}')
        else:
            print("Error: No active connection.") 


# [4. APPLy Subsystem] ------------------------------------------------------------------------------------------------------------------------------ #

# 4.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #
            
    def set_waveform(self, freq: float = 1e3, ampl: float = .1, offs: float = 0, ch: int = 1, fun = 'SIN'):
        if self._connect_success:
            if fun in {'SIN', 'SQU', 'TRI', 'RAMP', 'PULS', 'PRBS', 'NOIS', 'ARB', 'DC'}:
                self._resource.write(f'SOUR{ch}:APPL:{fun} {freq},{ampl},{offs}')
            else:
                print("Error. Invalid string mode. Write 'SIN', 'SQU', 'TRI', 'RAMP', 'PULS', 'PRBS', 'NOIS', 'ARB', or 'DC'")
        else:
            print("Error: No active connection.")