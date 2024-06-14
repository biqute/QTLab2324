import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from ellipse import LsqEllipse
from matplotlib.patches import Ellipse
import h5py
import Config as par


# //////////////////////////////////////////////////////// [dBm - mV Converter] ///////////////////////////////////////////////////////////////// #


def dBm_to_mVrms(dbm, R = 50):                            # R = 50 Ohm

	return (np.sqrt(R * 10**((dbm - 30)/10)))* 1e3



def mVrms_to_dBm(mv, R = 50):

	return 10 * np.log10((mv * 1e-3)**2 * 1000 / R)


def dBm_to_mVpk(dbm, R = 50):                            # R = 50 Ohm

	return (np.sqrt(2 * R * 10**((dbm - 30)/10)))* 1e3



def mVpk_to_dBm(mv, R = 50):

	return 10 * np.log10((mv * 1e-3)**2 * 500 / R)


def dBm_to_mVpp(dbm, R = 50):                            # R = 50 Ohm

	return 2 * (np.sqrt(2 * R * 10**((dbm - 30)/10)))* 1e3



def mVpp_to_dBm(mv, R = 50):

	return 10 * np.log10((mv * 1e-3)**2 * 125 / R)


# /////////////////////////////////////////////////////////// [Other functions] ///////////////////////////////////////////////////////////////// #


def find_key(dictionary, key_to_find):
    if key_to_find in dictionary:
        return dictionary[key_to_find]
    
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = find_key(value, key_to_find)
            if result is not None:
                return result
    return None


def ellipse_fit(x, y, toggle_plot = True, toggle_print = True):

	X = np.array(list(zip(x, y)))
	reg = LsqEllipse().fit(X)
	center, width, height, phi = reg.as_parameters()
	a, b, c, d, f, g = reg.coefficients

	if toggle_print:
		print(f'center	: ({center[0]:.3f}, {center[1]:.3f})')
		print(f'width	: {width:.3f}')
		print(f'height	: {height:.3f}')
		print(f'phi	: {phi:.3f}')
		print('-----------------------------')
		print(f'a	: {a}')
		print(f'b	: {b}')
		print(f'c	: {c}')
		print(f'd	: {d}')
		print(f'f	: {f}')
		print(f'g	: {g}')
		print('-----------------------------')

	if toggle_plot:
		fig = plt.figure(figsize=(6, 6))
		ax = plt.subplot()
		ax.axis('equal')
		ax.scatter(x, y, zorder=1, label = 'Data points')
		ellipse = Ellipse(
			xy=center, width=2*width, height=2*height, angle=np.rad2deg(phi),
			edgecolor='r', fc='None', lw=2, label='Fit', zorder=2
		)
		ax.add_patch(ellipse)

		plt.xlabel('Q')
		plt.ylabel('I')
		plt.grid()
		plt.legend()
		plt.show()
	
	return {
		'center': center,
		'width': width,
		'height': height,
		'phi': phi,
		'coefficients': {
			'a': a,
			'b': b,
			'c': c,
			'd': d,
			'f': f,
			'g': g
		}
	}


# //////////////////////////////////////////////////////////// [HDF5 functions] ///////////////////////////////////////////////////////////////// #

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

def get_avg_power(y: np.array, toggle_plot = True, sample_rate = 250e6):
	x = np.arange(len(y))/sample_rate
	std = np.std(y)
	indices = find_peaks(y, prominence=2*(np.max(y) - std))
	idx = indices[0]
	offset = 5
	idx = idx[offset:-offset]
	
	if toggle_plot:
							plt.figure(figsize=(10, 6)) 
							plt.plot(x, y, label='Signal')
							plt.scatter(x[idx], y[idx], color='orange', label='Peaks')
							plt.xlabel('Time (s)')
							plt.ylabel('Amplitude')
							plt.title('Signal with Peaks')
							plt.legend()
							plt.grid(True)
							plt.show()
	print(np.mean(y[idx]))
	return {'mean': np.mean(y[idx]), 'std' : np.std(y[idx]), 'x': x, 'y': y,'idx': idx}


def fetch_freq_range(f_range, CHs, LO, SG_Class, pxie_Class, sample_rate = 250e6):
	counter = 1
	digits_f = "{:0"+str(len(str(len(f_range))))+"d}"
	f_dict = {  'RF_input_Hz':  {},
				'LO_input_Hz':  LO}
	for i, f in enumerate(f_range):
		print(f'\rf{digits_f.format(i)}	: {int(counter*100/len(f_range))} %', end='', flush = True)
		counter += 1

		SG_Class.RF_freq(f_range) 
		SG_Class.pul_state(1)
		SG_Class.RF_state(1)
		waveforms = pxie_Class.acquisition(SG_Class.pul_exe_sing_trig)
		SG_Class.pul_state(0)
		SG_Class.RF_state(0)

		dict = {}
		for key, value in CHs.items():
			if value == 'I' or value == 'Q':
				dict[value] = np.array(waveforms[int(key)].samples.tolist())
				FT = np.abs(np.fft.fft(dict[value]))
				N = len(dict[value])
				freqs = np.fft.fftfreq(N,1/sample_rate) 
				dict['f_'+value+'_Hz'] = freqs[np.argmax(FT[:N // 2])]
				# dict['p_'+value+'_mV'] = get_avg_power(y = dict[value], toggle_plot = False, sample_rate = sample_rate)['mean']*1e3
		f_dict['RF_input_Hz'][f'f{digits_f.format(i)}'] = dict
		
	return f_dict


	