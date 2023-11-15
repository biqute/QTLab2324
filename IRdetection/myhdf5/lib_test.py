import numpy as np
import h5py
from myhdf5 import h5_and as hdf5

keys=['I','Q','Power','VR']
rows= 10000

dic = dict()

for key in keys:
    values = np.random.normal(loc=1.0, scale=0.01, size=rows)
    dic.update({key: list(values)})

name = 'prova1'
hdf5.dic_to_h5(name, dic)
hdf5.dict_to_structured_array(dic)
hdf5.h5_to_dic(name)
hdf5.open_h5(name)