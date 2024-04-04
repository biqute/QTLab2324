# https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/pdm/cl_manuals/user_manual/1178_3834_01/SMA100B_UserManual_en_10.pdf
#CAPITOLO 14 (E 13) DEL MANUALE!!!

# WEBSITE       Way more useful. 
# https://www.rohde-schwarz.com/webhelp/SMA100B_HTML_UserManual_en/Content/645d6b33dfb54d9b.htm

# Se si comunica col PC, l'interfaccia sua smette di rispondere. Premere LOCAL sul pannello.
# Lavoriamo solitamente coi microsecondi

# Pulse Width = larghezza gradino
#   Pulse delay = piedino sinistro del gradino
#   Pulse period = periodo, dunque sinistro + width + destro  
#   Pulse Mode è MOLTO IMPORTANTE!! Per la caratt del qubit useremo impulsi singoli o treni di impulsi.





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
# 2.6 | pul_exe_sing_trig .......... : If "Trigger Mode = Single", initiates a single pulse sequence manually.
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
import time



class SMA100B:

# 1.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def __init__(self, ip: str):

        self._resource = None
        self._connect_success = False
        self._sleep = 1

        try:
            rm = pyvisa.ResourceManager()
            self._resource = rm.open_resource(f"tcpip0::{ip}::inst0::INSTR")
            self._connect_success = True
            print("SMA100B: Connection successful!")
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


# [2. Modulation] ----------------------------------------------------------------------------------------------------------------------------------- #

# 2.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def transition_type(self, trans_type: str):                                      #così fa solo da fast a smoothed
        if self._connect_success:            
            if trans_type in {'FAST', 'SMO'}:
                self._resource.write(f'SOUR1:PULM:TTYP {trans_type}')  
            else:
                print("Error. Invalid string mode. Write 'FAST' or 'SMO'")    
        else:
            print("Error: No active connection.")

# 2.2 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def pul_gen_params(self, period: float, delay: float = 0, width: float = 0):                        # magari aggiungere confronto con valori dei range operativi, altrimenti errore.        
        '''
        Values must be in μs
        '''   
        if self._connect_success:
            
            self._resource.write(f'SOUR:PULM:PER {period*1e-6}') # micro
            self._resource.write(f'SOUR:PULM:DEL {delay*1e-6}')  # micro                # passo di 5 ns. 1-4 approx a 0, 6-9 approx a 5
            self._resource.write(f'SOUR:PULM:WIDT {width*1e-6}') # micro

            #print(self._resource.query('SOUR:PULM:DEL?'))
        else:
            print("Error: No active connection.")

# 2.3 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def pul_gen_mode(self, mode: str):
        if self._connect_success:
            if mode in {'SING', 'DOUB', 'PTR'}:
                self._resource.write(f'SOUR:PULM:MODE {mode}')

            else:
                print("Error. Invalid string mode. Write 'SING', 'DOUB' or 'PTR'")
        else:
            print("Error: No active connection.")

# 2.4 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def pul_trig_mode(self, mode: str):
        if self._connect_success:
            if mode in {'AUTO', 'EXT', 'EGAT', 'SING', 'ESIN'}:
                self._resource.write(f'SOUR:PULM:TRIG:MODE {mode}')

            else:
                print("Error. Invalid string mode. Write 'AUTO', 'EXT', 'EGAT', 'SING' or 'ESIN'")
        else:
            print("Error: No active connection.")

# 2.5 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def pul_state(self, state: int):
        if self._connect_success:
            self._resource.write(f'SOUR:PULM:STAT {state}')
        else:
            print("Error: No active connection.")            

# 2.6 ----------------------------------------------------------------------------------------------------------------------------------------------- #
            
    def pul_exe_sing_trig(self):
        self._resource.write('SOUR:PULM:INT:TRA:TRIG:IMM')
        
        

# [3. Frequency] ------------------------------------------------------------------------------------------------------------------------------------#

#3.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def RF_freq(self, freq: float):
        if self._connect_success:
            self._resource.write(f'SOUR:FREQ:CW {freq}')
        else:
            print("Error: No active connection.")


# [4. Level] ---------------------------------------------------------------------------------------------------------------------------------------- #

# 4.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def RF_state(self, switch: int):                                            # Turn ON or OFF the signal
        if self._connect_success:
            self._resource.write(f'OUTP:STAT {switch}')
        else:
            print("Error: No active connection.")

# 4.2 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def RF_lvl_ampl(self, amplitude: float):
        if self._connect_success:
            self._resource.write(f'SOUR:POW:LEV:IMM:AMPL {amplitude}')
        else:
            print("Error: No active connection.")

##### FUNZIONI DA IMPLEMENTARE????? #####



####### MODULATION ######
#pulse_mod_sour? (pulse generator or external)
#pulse external connector: impedance, polarity, threshold


####### FREQUENCY ######à