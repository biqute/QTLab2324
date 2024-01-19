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

def write(name: str, name_gp_data: str, freq_pump, dataset: dict):             
	with h5py.File(name, 'a') as f:                      # creo file hdf5 di nome tra virgolette e lo apro in modalità a = append
		if name_gp_data not in f.keys():
			gp = f.create_group(name_gp_data)
		else:
			gp = f[name_gp_data]
		gp_data = gp.create_group(str(freq_pump))
		for i, k in dataset.items():
			gp_data.create_dataset(i, data = k)

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #