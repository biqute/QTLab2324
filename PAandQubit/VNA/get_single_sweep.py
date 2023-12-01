import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import N99xxClass


###############################
                            
ip          = '192.168.40.10'   
mode        = 'NA'              
s_par       = 'S21'             
f_min       = 3                 
f_max       = 5 
hdf5_file   = 'DATA.hdf5'            
                            
###############################


vna = N99xxClass.N99xx(ip)

vna.reset()
vna.clear()
vna.set_mode(mode)

if mode == 'NA': 
    vna.set_NA_par(s_par)
    name_group = f'{mode}_{s_par}'
elif mode == 'SA':
    name_group = mode

vna.set_freq_range(f_min, f_max)

sweep = vna.get_data()
vna.w_hdf(hdf5_file, name_group, sweep)