import h5py

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# Metodi di scrittura e lettura in un file HDF5
	
def read(name: str, name_gp_data: str, nth_data: int):
	with h5py.File(name, 'r') as f:
		gp = f[name_gp_data][str(nth_data)]
		dic = {}
		for i, k in gp.items():
			dic[i] = k[()]
	return dic

def save_dict_to_hdf5(data, hdf5_file, group_name=''):
    
    with h5py.File(hdf5_file, 'a') as f:  # 'a' mode opens the file in append mode
        if group_name:
            group = f.require_group(group_name)
        else:
            group = f
            
        def recursively_save_dict_contents_to_group(h5file, path, dictionary):
            for key, item in dictionary.items():
                if isinstance(item, dict):
                    new_group = h5file.require_group(path + key + '/')
                    recursively_save_dict_contents_to_group(h5file, path + key + '/', item)
                else:
                    # Create or update dataset
                    if path + key in h5file:
                        del h5file[path + key]
                    h5file.create_dataset(path + key, data=item)
        
        recursively_save_dict_contents_to_group(group, '/', data)
        

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #