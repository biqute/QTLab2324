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
  
  def __init__(self, ip):
    rm = pyvisa.ResourceManager()
    self.vna = rm.open_resource(f"tcpip0::{str(ip)}::inst0::INSTR")
    self._sleep = 1
    return


  def reset(self):
    self.vna.write('*RST')
    time.sleep(self._sleep)
    return
  

  def get_data(self, fmin, fmax):
    
    # frequenze in GHz
    self.vna.write(f'FREQ:START {fmin * 1e9}')     #set freq iniziale                      CONTROLLARE DIFFERENZA WRITE E QUERY
    self.vna.write(f'FREQ:STOP {fmax * 1e9}')      #set freq finale

    valori = self.vna.query('TRACE:DATA? SDATA')  # pag 767  lista di parte reale e parte immaginaria alternati
    valori = list(map(float, valori.strip('\n').split(',')))

    I = np.array(valori[::2])   # parte immaginaria
    Q = np.array(valori[1::2])  # parte reale

    f = self.vna.query('FREQ:DATA?')
    f = np.array(list(map(float, f.strip('\n').split(',')))) / 1e9    # per esprimere i valori in GHz 

    return f, I, Q


  def get_name(self):
    print(self.vna.query('*IDN?'))
    return
  

  def set_mode(self, mode):
    valid_modes = ['NA', 'SA']
    if mode not in valid_modes:
      raise ValueError("Modalità non valida. Scegliere NA o SA.")
    self.vna.query(f'INST:SEL "{mode}";*OPC?')
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
    self.vna.query(f'CALC:PAR1:DEF {par};*OPC?')
    return
  

  def w_hdf(self, name, name_data, dataset):             # name = nome file hdf5    # name_data = NA o SA
    with h5py.File(name, "a") as f:                      # creo file hdf5 di nome tra virgolette e lo apro in modalità scrittura
      if name_data not in f.keys():
        gp = f.create_group(name_data)
      else:
        gp = f[name_data]
      gp_data = gp.create_group(f'fIQ_{len(gp.keys())}')
      gp_data.create_dataset('f', data = dataset[0])
      gp_data.create_dataset('I', data = dataset[1])
      gp_data.create_dataset('Q', data = dataset[2])

      # capire per SA quali e quanti dati devo caricare
      # mettere la condizione che l'utente usi solo NA o SA