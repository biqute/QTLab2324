###################################
#             Methods             #
#
# reset       :
# get_name    :
# set_mode    :
# set_NA_par  :
#                                 #
###################################


import pyvisa

class N99xx:
  
  def __init__(self, ip):
    rm = pyvisa.ResourceManager()
    self.vna = rm.open_resource(f"tcpip0::{ip}::inst0::INSTR")
    return

  def reset(self):
    self.vna.write('*RST')
    return
  
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