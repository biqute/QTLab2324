###################################
#             Methods             #
#
# get_data    :
# get_name    :
# reset       :
# set_mode    :
# set_NA_par  :

# r_hdf       : 
# w_hdf       :
#                                 #
###################################


import pyvisa
import numpy as np
import time
import h5py 

class N99xx:
  
  def __init__(self, ip: str):
    self._risorsa = None
    self._connessione_riuscita = False
    self._sleep = 1
    try:
      rm = pyvisa.ResourceManager()
      self.risorsa = rm.open_resource(f"tcpip0::{ip}::inst0::INSTR")
      self._connessione_riuscita = True
      print("Connessione riuscita!")
    except pyvisa.Error as e:
      print(f"Errore durante la connessione: {e}")
    return


  def reset(self):
    if self._connessione_riuscita:
      self.vna.write('*RST')
      time.sleep(self._sleep)
    else:
      print("Impossibile eseguire il metodo reset: nessuna connessione attiva.")
    return
  

  def get_data(self, fmin, fmax):
    if self._connessione_riuscita:
      # frequenze in GHz
      self.vna.write(f'FREQ:START {fmin * 1e9}')     #set freq iniziale                    
      self.vna.write(f'FREQ:STOP {fmax * 1e9}')      #set freq finale

      valori = self.vna.query('TRACE:DATA? SDATA')  # pag 767  lista di parte reale e parte immaginaria alternati
      valori = list(map(float, valori.strip('\n').split(',')))

      I = np.array(valori[::2])   # parte immaginaria
      Q = np.array(valori[1::2])  # parte reale

      f = self.vna.query('FREQ:DATA?')
      f = np.array(list(map(float, f.strip('\n').split(',')))) / 1e9    # per esprimere i valori in GHz 
      return {'f': f, 'I': I, 'Q': Q}
    else:
      print("Impossibile eseguire il metodo get_data: nessuna connessione attiva.")
      return


  def get_name(self):
    if self._connessione_riuscita:
      print(self.vna.query('*IDN?'))
    else:
      print("Impossibile eseguire il metodo get_name: nessuna connessione attiva.")
    return
  

  def set_mode(self, mode):
    if self._connessione_riuscita:
      valid_modes = ['NA', 'SA']
      if mode not in valid_modes:
        raise ValueError("Modalità non valida. Scegliere NA o SA.")
      self.vna.query(f'INST:SEL "{mode}";*OPC?')
    else:
      print("Impossibile eseguire il metodo set_mode: nessuna connessione attiva.")
    return
  

  def set_NA_par(self, par):
    # S11 - Forward reflection measurement
    # S21 - Forward transmission measurement
    # S12 - Reverse transmission 
    # S22 - Reverse reflection
    # A - A receiver measurement
    # B - B receiver measurement
    # R1 - Port 1 reference receiver measurement
    # R2 - Port 2 reference receiver measurement
    if self._connessione_riuscita:
      self.vna.query(f'CALC:PAR1:DEF {par};*OPC?')
    else:
      print("Impossibile eseguire il metodo set_NA_par: nessuna connessione attiva.")
    return
  

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
# Metodi di scrittura e lettura in un file HDF5


  def r_hdf(self, name: str, name_data: str, nth_data: int):
    with h5py.File(name, 'r') as f:
      gp = f[name_data][str(nth_data)]
      dic = {}
      for i, k in gp.items():
        dic[i] = k[()]
    return dic
  

  def w_hdf(self, name: str, name_data: str, dataset: dict):             # name = nome file hdf5    # name_data = NA o SA
    with h5py.File(name, 'a') as f:                      # creo file hdf5 di nome tra virgolette e lo apro in modalità a = append
      if name_data not in f.keys():
        gp = f.create_group(name_data)
      else:
        gp = f[name_data]
      gp_data = gp.create_group(str(len(gp.keys())))
      for i, k in dataset.items():
        gp_data.create_dataset(i, data = k)
    return
      # capire per SA quali e quanti dati devo caricare


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#