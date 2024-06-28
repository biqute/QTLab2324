###################################
#             Methods             #
#
# 01 | __init__         	:
# 02 | reset            	:
# 03 | clear            	:
# 04 | write				:
# 05 | query				:
# 06 | get_data         	:
# 07 | get_name         	:
# 08 | run_hold         	:
# 09 | set_mode         	:
# 10 | set_NA_par       	:
# 11 | set_freq_range   	:
# 12 | set_num_pts			:
# 13 | set_freq_span		:
# 14 | set_freq_center		:
# 15 | set_freq_bandwidth	:
# 16 | num_avgs				:
# 17 | set_scaling			:
# 18 | get_freqs			:
# 19 | power				:
#                                 #
###################################

# https://helpfiles.keysight.com/csg/FFProgrammingHelpWebHelp/A_NA_Mode_Commands.htm


import pyvisa
import numpy as np
import time

class N9916A:


	def __init__(self, ip: str):

		self._resource = None
		self._connect_success = False
		self._sleep = 1
		self._device_name = "N9916A"
		try:
			rm = pyvisa.ResourceManager()
			self._resource = rm.open_resource(f"tcpip0::{ip}::inst0::INSTR")
			self._connect_success = True
			print(f"{self._device_name}:\tConnection successful!")
		except pyvisa.Error as e:
			print(f"{self._device_name}:\tUnable to establish a connection: {e}")


	def reset(self):
		self._resource.write('*RST')     
		time.sleep(self._sleep)
		

	def clear(self):
		self._resource.write('*CLS')     #*CLS   è il reset che svuota la memoria (il buffer), utile se si inchioda
		time.sleep(self._sleep)


	def write(self, command: str):
		self._resource.write(command)     
		time.sleep(self._sleep)
	
	def query(self, command: str):
		return self._resource.query(command)


	def get_data(self):
		data_type = ''
		NA_flag = False
		if self._resource.query('INST:SEL?') == '"NA"\n':
			data_type = ' SDATA'
			NA_flag = True
		
		valori = self._resource.query(f'TRAC1:DATA?{data_type}')  # pag 767  lista di parte reale e parte immaginaria alternati
		valori = list(map(float, valori.strip('\n').split(',')))

		if NA_flag:
			I = np.array(valori[::2])   # parte immaginaria
			Q = np.array(valori[1::2])  # parte reale
			f = self._resource.query('FREQ:DATA?')
			f = np.array(list(map(float, f.strip('\n').split(',')))) / 1e9    # per esprimere i valori in GHz 
			return {'f': f, 'I': I, 'Q': Q}
		
		else:
			return {'scalar': valori}


	def get_name(self):
		return self._resource.query('*IDN?')

	def get_freqs(self):
		return self._resource.query("FREQ:DATA?")

	
	def run_hold(self, mode = 'RUN'):        
		values = {'RUN': 1, 'HOLD': 0}
		if mode not in values.keys():
			raise ValueError("Invalid mode. Choose RUN or HOLD.")                    
		self._resource.write(f'INIT:CONT {values[mode]}')
		time.sleep(self._sleep)

		
	def set_mode(self, mode):
		valid_modes = ['NA', 'SA']
		if mode not in valid_modes:
			raise ValueError("Invalid mode. Choose NA or SA.")
		self._resource.query(f'INST:SEL "{mode}";*OPC?')
		time.sleep(self._sleep)                                              
	

	def set_NA_par(self, par: str = 'S21'):
		''' S11 - Forward reflection measurement\n
			S21 - Forward transmission measurement\n
			S12 - Reverse transmission\n
			S22 - Reverse reflection\n '''
		valid_modes = ['S11', 'S21', 'S12', 'S22']
		if par not in valid_modes:
			raise ValueError("Invalid parameter. Choose S11, S12, S21 or S22.")
		self._resource.query(f'CALC:PAR1:DEF {par};*OPC?')
		time.sleep(self._sleep)
	

	def set_freq_range(self, fmin: float, fmax: float):
		self._resource.write(f'FREQ:START {fmin}')     # set freq iniziale                    
		self._resource.write(f'FREQ:STOP {fmax}')      # set freq finale

	def set_num_pts(self, n_pts):
		self._resource.write(f'SWE:POIN {n_pts}')     
		time.sleep(self._sleep)

	def set_freq_span(self, f_span):
		self._resource.write(f'FREQ:SPAN {f_span}')     
		time.sleep(self._sleep)
	
	def set_freq_center(self, f_center):
		self._resource.write(f'FREQ:CENT {f_center}')     
		time.sleep(self._sleep)
	
	def set_freq_bandwidth(self, f_bwd):
		self._resource.write(f'BWID {f_bwd}')     
		time.sleep(self._sleep)


	def num_avgs(self, n):							  #  Set and query the number of sweep averages
		self._resource.write(f'AVER:COUN {n}')     
		time.sleep(self._sleep)


	def set_scaling(self, scale = 0, rf_lvl = 0, rf_pos = 0, auto = False):

		if auto: 
			self._resource.write(f'DISPlay:WINDow:TRAC1:Y:AUTO')     
			time.sleep(self._sleep)
		else:
			self._resource.write(f'DISP:WIND:TRAC1:Y:PDIV {scale}')     
			time.sleep(self._sleep)
			self._resource.write(f'DISP:WIND:TRAC1:Y:RLEV {rf_lvl}')     
			time.sleep(self._sleep)
			self._resource.write(f'DISP:WIND:TRAC1:Y:RPOS {rf_pos}')     
			time.sleep(self._sleep)


	@property
	def power(self):
		return float(self._resource.query('SOUR:POW?')[:-1])

	@power.setter
	def power(self, dBm_value):
		self._resource.write(f'SOUR:POW {dBm_value}')     
		time.sleep(self._sleep)




# ERRORI

# UnicodeDecodeError: 'ascii' codec can't decode byte 0xbc in position 10: ordinal not in range(128)
# fix it : launch clear() and then launch reset()