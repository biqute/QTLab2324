# Se si comunica col PC, l'interfaccia sua smette di rispondere. Premere LOCAL sul pannello.

# LAvoriamo solitamente coi microsecondi

# Pulse Width = larghezza gradino
#   Pulse delay = piedino sinistro del gradino
#   Pulse period = periodo, dunque sinistro + width + destro  






import pyvisa
import numpy as np
import time
import h5py 



class SMA100B:

    def __init__(self, ip: str):

        self._risorsa = None
        self._connessione_riuscita = False
        self._sleep = 1

        try:
            rm = pyvisa.ResourceManager()
            self._risorsa = rm.open_resource(f"tcpip0::{ip}::inst0::INSTR")
            self._connessione_riuscita = True
            print("Connessione riuscita!")
        except pyvisa.Error as e:
            print(f"Errore durante la connessione: {e}")
        return



    def get_name(self):
        if self._connessione_riuscita:
            print(self._risorsa.query('*IDN?'))
        else:
            print("Impossibile eseguire il metodo get_name: nessuna connessione attiva.")
        return