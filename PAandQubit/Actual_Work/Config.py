# DEV CONNECTION
QSyn_port       = 'COM37'
SG_ip           = '192.168.40.15'                                   # Set IP address of the device
Card_Name       = 'PXI1Slot3'


# Quick Syn
LO =  5e9
fsl_freq = round(LO, 1)
 

# MR GEN
dwc_f = 10e6                                                        # Down conversion frequency
step = 10e6
n = 20                                                              # number of steps

pulse_f_min     = LO + dwc_f
pulse_f_max		= pulse_f_min + n * step

amp_i			= -30                                               # dBm
amp_f           = -10
 
pulse_period    = 1e-6                                              # 4e-6 con 250e6 dà 1000 punti
pulse_delay     = 0
percent         = 5
pulse_width     = pulse_period * (1 - percent/100)                  # min 20ns


# PXIE
sample_rate     = 250e6                                             # Maximum Value: 250.0e6
num_pts         = int(sample_rate * pulse_period)                   # min 5ns                             
channels = {'I'			: 0, 
			'Q'			: 1,
			'trigger'	: 3}







