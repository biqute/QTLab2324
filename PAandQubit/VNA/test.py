import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import N99xxClass


ip = '192.168.40.10'
vna = N99xxClass.N99xx(ip)

# f, I, Q = vna.get_data(2, 5)

# plt.plot(f, 20*np.log10(np.abs(Q)+1j*I))
# plt.show()

# dataset = vna.get_data(1, 10)
# dic = {'a':[1,2],'b':[3,4]} 
# vna.w_hdf('HDF5.hdf5', 'NA', dic)
# print(vna.r_hdf('HDF5.hdf5', 'NA', 0))



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


# 

#vna.reset()

# vna.set_mode('NA')

# vna.set_NA_par('S21')

# # valori = vna.get_data()

# # vna.get_name()
# vna.set_freq_range(2, 7)

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
