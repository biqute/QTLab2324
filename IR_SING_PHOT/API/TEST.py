from Acquisition_config import ACQUISITION_CONFIG
import sys
import time
sys.path.append(r'C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IR_SING_PHOT\Synth')
sys.path.append(r'C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IR_SING_PHOT\Exceptions')
sys.path.append(r'C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IR_SING_PHOT\DAQ')
import Synthesizer
from logs.logging_config import LOGGING_CONFIG
from logging.config import dictConfig
import logging
import json
from Exceptions import replace_non_serializable
import DAQ
import niscope as ni
import numpy as np
import matplotlib.pyplot as plt

filepath = r'C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IR_SING_PHOT\API'

channels = {'I'			: 0, 
            'Q'			: 1,
            'trigger'	: 0}

data = {'CH0': [],
            'CH1': [],
            'CH2': [],
            'CH3': [],
            'time': []
            }

devicename =  'PXI1Slot4'

res   = 5.3466
span  = 5*1e-2
start = res-span
stop  = res+span
num = 1000
minutes = num/10/60
fs = np.linspace(start,stop,num)

daq = DAQ.DAQ()

s1 = Synthesizer.Synthesizer(1)
s1.connettore()

daq.acq_conf = ACQUISITION_CONFIG['acq_conf']
daq.horizontal_conf = ACQUISITION_CONFIG['horizontal']
daq.vertical_conf = ACQUISITION_CONFIG['vertical']
daq.chan_conf = ACQUISITION_CONFIG['chan_conf']
daq.trigger_dic = ACQUISITION_CONFIG['trigger']

daq._session = ni.Session(devicename)
daq.config_trigger()
with daq._session as session:
    daq.configure_channels()
    
    for i,f in enumerate(fs):
        s1.set_frequency(str(f)+'GHz') # set frequency
        print(str(i)+'\t'+str(s1.get_frequency()))
        daq._session.initiate()
        waveforms = session.channels[0, 1].fetch()
        data['CH0'].append(np.array(waveforms[0].samples.tolist()).mean())
        data['CH1'].append(np.array(waveforms[1].samples.tolist()).mean())    
        

I = np.array(data['CH1'])
Q = np.array(data['CH0'])
C = Q+1j*I
P = np.unwrap(np.angle(C))
S = np.abs(C)

data['time'] = np.arange(0,len(data['CH0']),1)

fig, axs  = plt.subplots(1,2,figsize=(20,5))
axs[0].plot(data['time'],data['CH1'], label='I channel', color='black')
axs[1].plot(data['time'],data['CH0'], label='Q channel', color='black')
axs[0].set_xlabel('timestamp')
axs[1].set_xlabel('timestamp')
axs[0].set_ylabel('I signal')
axs[1].set_ylabel('Q signal')
axs[0].legend()
axs[1].legend()
fig.savefig('test1.png')


fig, axs  = plt.subplots(1,2,figsize=(20,5))
axs[0].plot(fs,S, label='Absolute value',  color='black')
axs[1].plot(fs,P, label='Phase', color='black')
axs[0].set_xlabel(r'$\nu [GHz]$')
axs[1].set_xlabel(r'$\nu [GHz]$')
axs[0].set_ylabel(r'$S_{21}$ [A.U.]')
axs[1].set_ylabel(r'$\phi$ [rad]')
axs[0].legend()
axs[1].legend()
fig.savefig('test2.png')