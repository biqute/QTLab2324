import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import QTLab2324.PAandQubit.Instruments.VNA.NA_N9916A as NA_N9916A


###############################
                            
ip          = '192.168.40.10'   
mode        = 'NA'              
s_par       = 'S21'             
f_min       = 3                 
f_max       = 5 
hdf5_file   = 'DATA.hdf5'            
                            
###############################


vna = NA_N9916A.N99xx(ip)

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

# for i in np.arange(99):         #FUNZIONA!!

#     vna.w_hdf('culone.hdf5', 'NA', vna.get_data())
#     if i==50:
#         print('Sono a metà')

#vna.runhold()

    #prima_lett = vna.r_hdf_data('culone.hdf5', 'NA',  1)

# f = prima_lett['f']
# I = prima_lett['I']
# Q = prima_lett['Q']



# plt.plot(f, 20*np.log10(np.abs(Q + 1j*I)))
# plt.show()
