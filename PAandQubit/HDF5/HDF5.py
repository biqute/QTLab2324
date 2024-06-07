import h5py

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# Metodi di scrittura e lettura in un file HDF5


def save_dict_to_hdf5(data, hdf5_file, group_name=''):
    
    def recursively_save(h5file, path, dictionary):
        for key, item in dictionary.items():
            if isinstance(item, dict):
                new_group = h5file.require_group(path + key + '/')
                recursively_save(h5file, path + key + '/', item)
            else:
                # Create or update dataset
                if path + key in h5file:
                    del h5file[path + key]
                h5file.create_dataset(path + key, data=item)    
    
    with h5py.File(hdf5_file, 'a') as f:  # 'a' mode opens the file in append mode
        if group_name:
            group = f.require_group(group_name)
        else:
            group = f
        
        recursively_save(group, '/', data)




def load_hdf5_to_dict(hdf5_file, group_name=''):

    def recursively_load(h5group):
        dictionary = {}
        for key, item in h5group.items():
            if isinstance(item, h5py.Dataset):
                dictionary[key] = item[()]
            elif isinstance(item, h5py.Group):
                dictionary[key] = recursively_load(item)
        return dictionary

    with h5py.File(hdf5_file, 'r') as f:
        if group_name:
            group = f[group_name]
        else:
            group = f
        data_dict = recursively_load(group)
    
    return data_dict

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #