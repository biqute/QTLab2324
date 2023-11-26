import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import N99xxClass


ip = '192.168.40.10'
vna = N99xxClass.N99xx(ip)

# f, I, Q = vna.get_data(2, 5)

# plt.plot(f, 20*np.log10(np.abs(Q)+1j*I))
# plt.show()

dataset = vna.get_data(1, 10)
dic = {'a':[1,2],'b':[3,4]} 
vna.w_hdf('HDF5.hdf5', 'NA', dic)
print(vna.r_hdf('HDF5.hdf5', 'NA', 0))
