import h5py as h5
from HDF5.utils import utils

class HDF5():
    _filename = None
    
    def __init__(self):
        self._filename = ''
        self._dic = {}

    @property
    def name(self):
        return self._filename
    
    @name.setter
    def name(self,name):
        self._filename = name

    @name.deleter
    def name(self):
        del self._filename

    @property
    def dic(self):
        return self._dic
    
    @dic.setter
    def dic(self, dictionary):
        if isinstance(dictionary,dict):
            self._dic = dictionary
        else:
            print('Object parameter must be a dictionary!')

    @utils.exec_time
    def to_hdf5(self):
        with h5.File(self._filename, 'w') as file:
            for gkey, gvalue in self._dic.items():
                if isinstance(gvalue, dict):
                    g = file.create_group(gkey)
                    for key, item in gvalue.items():
                        g.create_dataset(key, data=item)
                else:
                    file.create_dataset(gkey, data=gvalue)
        return file 
    
    @utils.exec_time
    def load_hdf5(self):
        def recursively_load_group(group):
            result = {}
            for key, item in group.items():
                if isinstance(item, h5.Group):
                    result[key] = recursively_load_group(item)
                elif isinstance(item, h5.Dataset):
                    result[key] = item[()]  # Load the dataset into memory
            return result

        with h5.File(self._filename, 'r') as file:
            self._dic = recursively_load_group(file)