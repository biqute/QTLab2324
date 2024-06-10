import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

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
		fig, axs = plt.subplots(2, 2, figsize=(10, 8))
		axs.clf()
		axs.grid()
		axs.plot(x, y)
		axs.scatter(x[idx],y[idx], color = 'orange')
		plt.show()
	return {'mean': np.mean(y[idx]), 'std' : np.std(y[idx]), 'x': x, 'y': y,'idx': idx}