import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import h5py
from PIL import Image
import os
from scipy.signal import find_peaks

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
	return {'mean': np.mean(y[idx]), 'std' : np.std(y[idx]), 'x': x, 'y': y,'idx': idx}


def find_key(dictionary, key_to_find):
    if key_to_find in dictionary:
        return dictionary[key_to_find]
    
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = find_key(value, key_to_find)
            if result is not None:
                return result
    return None

#============================================================================================
# Functions for plotting...
#============================================================================================

def rough_plotter(data, sample_rate,name):
	x = np.arange(len(data['CH0']))/sample_rate
	fig, axs = plt.subplots(2,2)
	fig.set_figheight(5)
	fig.set_figwidth(20)
	axs[0][0].scatter(x, data['CH0'], color='black', marker='.', label='CH0')
	axs[0][0].set_xlabel('Timestamp')
	axs[0][0].set_ylabel('Signal')
	axs[0][1].scatter(x, data['CH1'], color='black', marker='.', label='CH1')
	axs[0][1].set_xlabel('Timestamp')
	axs[0][1].set_ylabel('Signal')
	axs[1][0].scatter(x, data['CH2'], color='black', marker='.', label='CH2')
	axs[1][0].set_xlabel('Timestamp')
	axs[1][0].set_ylabel('Signal')
	axs[1][1].scatter(x, data['CH3'], color='black', marker='.', label='CH3')
	axs[1][1].set_xlabel('Timestamp')
	axs[1][1].set_ylabel('Signal')
	fig.set_facecolor('bisque')
	plt.savefig(str(name)+'.png','.png')


def channel_plotter(data, sample_rate):
	x = np.arange(len(data['CH0']))/sample_rate
	fig, axs = plt.subplots(1,2)
	fig.set_figheight(5)
	fig.set_figwidth(20)
	axs[0].plot(x, data['CH0'], color='black', label='CH0 - Q')
	axs[0].set_xlabel('Timestamp')
	axs[0].set_ylabel('Signal')
	axs[0].set_title('Q vs time_stamp')
	axs[0].set_facecolor('bisque')
	axs[0].legend()
	axs[0].grid()
	axs[1].plot(x, data['CH1'], color='black', label='CH1 - I')
	axs[1].set_xlabel('Timestamp')
	axs[1].set_ylabel('Signal')
	axs[1].set_title('I vs time_stamp')
	axs[1].set_facecolor('bisque')
	axs[1].grid()
	return fig

def S21_plotter(data, sample_rate):
	x = np.arange(len(data['CH0']))/sample_rate
	S21 = np.array(data['CH0'])**2+np.array(data['CH1'])**2
	PHASE = np.arctan(np.array(data['CH1'])/np.array(data['CH0']))
	fig, axs = plt.subplots(1,2)
	fig.set_figheight(5)
	fig.set_figwidth(20)
	axs[0].plot(x, S21, color='black', label='$|S_{21}(t)|$')
	axs[0].set_xlabel('Timestamp')
	axs[0].set_ylabel('$|S_{21}|$')
	axs[0].set_title('Modulus vs time_stamp')
	axs[0].set_facecolor('bisque')
	axs[0].legend()
	axs[0].grid()
	axs[1].plot(x, PHASE, color='black', label='$tan^{-1}\frac{I}{Q}(t)$')
	axs[1].set_xlabel('Timestamp')
	axs[1].set_ylabel('Phase')
	axs[1].set_title('Phase vs time_stamp')
	axs[1].set_facecolor('bisque')
	axs[1].grid()
	return fig
	
def IQ_plotter(data):
	fig, axs = plt.subplots(1,1)
	fig.set_figheight(5)
	fig.set_figwidth(20)
	axs.scatter(data['CH1'], data['CH0'], marker='.', color='black', label='I vs Q')
	axs.set_xlabel('Q')
	axs.set_ylabel('I')
	axs.set_title('I vs Q')
	axs.set_facecolor('bisque')
	axs.grid()
	return fig

def compressimages(image_file):
    # accessing the image file
    filepath = os.path.join(os.getcwd(), image_file)
    # maximum pixel size
    maxwidth = 1200
    # opening the file
    image = Image.open(filepath)
    # Calculating the width and height of the original photo
    width, height = image.size
    # calculating the aspect ratio of the image
    aspectratio = width / height
 
    # Calculating the new height of the compressed image
    newheight = maxwidth / aspectratio
 
    # Resizing the original image
    image = image.resize((maxwidth, round(newheight)))
 
    # Saving the image
    image.save(image_file, optimize=True, quality=85)
    return

#=======================================================================================
#Saveing data
#=======================================================================================
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