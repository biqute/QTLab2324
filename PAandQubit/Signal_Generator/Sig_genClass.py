# https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/pdm/cl_manuals/user_manual/1178_3834_01/SMA100B_UserManual_en_10.pdf
#CAPITOLO 14 (E 13) DEL MANUALE!!!

# WEBSITE       Way more useful. 
# https://www.rohde-schwarz.com/webhelp/SMA100B_HTML_UserManual_en/Content/645d6b33dfb54d9b.htm

# Se si comunica col PC, l'interfaccia sua smette di rispondere. Premere LOCAL sul pannello.
# LAvoriamo solitamente coi microsecondi

# Pulse Width = larghezza gradino
#   Pulse delay = piedino sinistro del gradino
#   Pulse period = periodo, dunque sinistro + width + destro  
#   Pulse Mode è MOLTO IMPORTANTE!! Per la caratt del qubit useremo impulsi singoli o treni di impulsi.





###################################
#             Methods             #
#
# 01 | __init__         :
# 02 | get_name         :
#
# 
# Modulation
# 01 | transition_type
# 02 | pul_gen_params
# 03 | pul_gen_mode   
# 
# 
# Level
# 01 | RF_onoff                       #
###################################



import pyvisa
import numpy as np
import time
import h5py 



class SMA100B:

    def __init__(self, ip: str):

        self._resource = None
        self._connect_success = False
        self._sleep = 1

        try:
            rm = pyvisa.ResourceManager()
            self._resource = rm.open_resource(f"tcpip0::{ip}::inst0::INSTR")
            self._connect_success = True
            print("Connessione riuscita!")
        except pyvisa.Error as e:
            print(f"Errore durante la connessione: {e}")
        return



    def get_name(self):
        if self._connect_success:
            print(self._resource.query('*IDN?'))
        else:
            print("Impossibile eseguire il metodo get_name: nessuna connessione attiva.")
        return


    def reset(self):
        self._resource.write('*RST')
        return




    






    def transition_type(self, trans_type):                                      #così fa solo da fast a smoothed
        if self._connect_success:            
            if trans_type in {'FAST', 'SMO'}:
                self._resource.write(f'SOUR1:PULM:TTYP {trans_type}')  
            else:
                print('Error. Write FAST or SMO')    
            
        return

    #pagina 603-604
    def pul_gen_params(self, period, delay, width):                        # magari aggiungere confronto con valori dei range operativi, altrimenti errore.           
        if self._connect_success:

            
            self._resource.write(f'SOUR:PULM:PER {period*1e-6}')
            self._resource.write(f'SOUR:PULM:DEL {delay}')                  #passo di 5 ns. 1-4 approx a 0, 6-9 approx a 5
            self._resource.write(f'SOUR:PULM:WIDT {width*1e-6}')

            print(self._resource.query('SOUR:PULM:DEL?'))
        return    


    def pul_gen_mode(self, mode):
        if self._connect_success:
            if mode in {'SING', 'DOUB', 'PTR'}:
                self._resource.write(f'SOUR:PULM:MODE {mode}')

            else:
                print("Error. Invalid string mode. Write SING DOUB PTR")
        return            












    def RF_onoff (self, switch):                                            #accendere o spegnere il segnale
        if self._connect_success:
            self._resource.write(f'OUTP:STAT {switch}')
        return
    
    
##### FUNZIONI DA IMPLEMENTARE????? #####



####### MODULATION ######
#Trigger mode (Molto probabilmente no)
#pulse_mod_sour? (pulse generator or external)
#pulse external connector: impedance, polarity, threshold


####### FREQUENCY ######à