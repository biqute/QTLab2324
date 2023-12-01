# https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/pdm/cl_manuals/user_manual/1178_3834_01/SMA100B_UserManual_en_10.pdf
#CAPITOLO 14 (E 13) DEL MANUALE!!!


# Se si comunica col PC, l'interfaccia sua smette di rispondere. Premere LOCAL sul pannello.
# LAvoriamo solitamente coi microsecondi

# Pulse Width = larghezza gradino
#   Pulse delay = piedino sinistro del gradino
#   Pulse period = periodo, dunque sinistro + width + destro  






###################################
#             Methods             #
#
# 01 | __init__         :
# 02 | get_name         :
#                                 #
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


    
    def on_off(self):
        if self._connect_success:
            self._resource.write('SOUR1:MOD:ALL:STAT 0')             #resta da capire perché SOURCE 1, ma probabilmente è perchè è l'unica.

        return


    
    def transition_type(self):                                      #così fa solo da fast a smoothed
        if self._connect_success:
            self._resource.write('SOUR1:PULM:TTYP SMO')            

        return

    #pagina 603-604
    def pulse_generator(self, delay, width):                                        #NON FUNZIONA!!!
        if self._connect_success:
            #self._resource.write(f'SOUR1:PULM:PER "{period*1e-6}"')
            self._resource.write(f'SOUR1:PULM:DOUB:DEL {delay*1e-9}')
            self._resource.write(f'SOUR1:PULM:DOUB:WIDT {width*1e-6}')

        return    