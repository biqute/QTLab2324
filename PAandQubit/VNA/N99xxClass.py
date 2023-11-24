###################################
#             Methods             #
#
# reset       :
# get_data    :
# get_name    :
# set_mode    :
# set_NA_par  :
#                                 #
###################################


import pyvisa
import numpy as np
import time

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
  

  def get_data(self):
    
    print('Impostare range di frequenze (GHz).')
    print('f min: ')
    fmin = float(input()) * 1e9
    print('f max: ')
    fmax = float(input()) * 1e9

    self.vna.query(f'FREQ:START {fmin};*OPC?')     #set freq iniziale
    self.vna.query(f'FREQ:STOP {fmax};*OPC?')      #set freq finale

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
  
