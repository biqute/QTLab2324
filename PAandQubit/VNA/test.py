import pyvisa
import matplotlib.pyplot as plt
import numpy as np
import N99xxClass


ip = '192.168.40.10'
vna = N99xxClass.N99xx(ip)

f, I, Q = vna.get_data(2, 5)

plt.plot(f, 20*np.log10(np.abs(Q)+1j*I))
plt.show()

dataset = vna.get_data(1, 10)
vna.w_hdf('HDF52.hdf5', 'NA', dataset)