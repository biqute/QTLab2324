import sys
import os

base_path = r"C:\Users\oper\SynologyDrive\Lab2023\KIDs\QTLab2324\IRSource"
sys.path.append(os.path.join(base_path, "DAQ"))
sys.path.append(os.path.join(base_path, "AFG310"))
sys.path.append(os.path.join(base_path, "Logger", "logs", "sessions"))
sys.path.append(os.path.join(base_path, "Exceptions"))
sys.path.append(base_path)


import json
from DAQ import DAQ
from AFG310 import diode
from Acquisition_config import ACQUISITION_CONFIG
import logging
from logging.config import dictConfig
from SingleFreq.logs.logging_config import LOGGING_CONFIG 
from Exceptions import replace_non_serializable
from PAmodules.QuickSyn import FSL_0010
from PAmodules.network.RS_Signal_Generator import RS_SMA100B
import niscope as ni
import numpy as np
from HDF5 import HDF5 as h5
from API.PAmodules.Tools import IQ_plotter


ip   = '192.168.40.15'   # Set IP address of SMA
devicename = 'PXI1Slot3' 
porta_diodo = 'GPIB0::1::INSTR'
filepath = r'C:\\Users\\oper\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRSource\\API\\SingleFreq\\png\\'

LO =  9e9 
RF     = LO + 2e6
amplitude       = 16  
sample_rate     = 250e6
k               = 4
pulse_period    = k * 1e-6
num_points      = int(sample_rate * pulse_period)
percent         = 5
pulse_width     = pulse_period * (1-percent/100)
pulse_delay     = 0

channels = {'I'			: 0, 
            'Q'			: 1,
            'trigger'	: 3}

#===============================================================================================
#Import logger configuration
#===============================================================================================
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('START EXECUTION')

try:
    cfg1 = json.dumps(replace_non_serializable(ACQUISITION_CONFIG))
    logger.info('Dumping acquisition configuration')
    with open(ACQUISITION_CONFIG['acq_conf']['path'] + 'config.json','w') as f:
        f.write(cfg1)
except Exception:
    logger.critical('Dumping acquisition configuration')
    raise SystemError("Could not dump acquisition configuration!")

#===============================================================================================
#Import DAQ configuration dictionaries
#===============================================================================================

try:
    daq = DAQ()
    logger.info('DAQ class object correctly created')
except Exception:
    logger.critical('Could not crate DAQ class object')
    raise SyntaxError('Could not create DAQ class object')


try:
    stat = daq.get_status
    logger.info('DAQ status: '+str(stat))
except Exception:
    logger.critical('Could not get DAQ status!')
    raise SystemError('Could not get DAQ status')

try:
    daq.reset_with_def()
    daq.get_status
    logger.info('Resetting DAQ with defaults')
except Exception:
    logger.error('Could not reset DAQ with defaults')
    pass
    #raise SystemError('Could not restet DAQ with defaults')

#===============================================================================================
#Set FSL and sGEN Synt
#===============================================================================================


try:
    fsl = FSL_0010.FSL10_synthesizer(device_address='COM36')
    logger.info('FSL_0010 class object correctly created')
except Exception:
    logger.critical('Could not crate FSL class object')
    raise SyntaxError('Could not create FSL class object')

try:
    sGen = RS_SMA100B.SMA100B(ip)
    logger.info('SMA class object correctly created')
except Exception:
    logger.critical('Could not crate SMA class object')
    raise SyntaxError('Could not create SMA class object')

try:    
    sGen.reset()
    sGen.clear()
    sGen.RF_lvl_ampl(amplitude)
    #sGen.pul_gen_params(delay = pulse_delay, width = pulse_width, period = pulse_period)  
    #sGen.pul_gen_mode('SING')
    #sGen.pul_trig_mode('SING')
    logger.info('SMA set up correctly')
except Exception:
    logger.critical('Could not set up SMA')
    raise SystemError('Could not create SMA class object')

#===============================================================================================
#Set Laser Diode
#===============================================================================================

try:
    logger.info('Connecting to diode...')
    diodo = diode()
    diodo.board         = porta_diodo
    diodo.connect()
except Exception:
    logger.critical('Could not connect to diode!')
    raise SystemError('Could not connect to diode!')

try:
    logger.info('Setting diode settings')
    diodo.reset()
    diodo.amplitude     = 1
    diodo.func          = 'SQU'
    diodo.mode          = 'TRIG'
    diodo.freq          = 16e6
    diodo._diode.write(f'SOUR:PULS:DCYC {1}')

except Exception:
    logger.critical('Could not set diode configuration!')
    raise SystemError('Could not set diode configuration!')

#===============================================================================================
#Set DAQ configuration dictionaries
#===============================================================================================

try:
    daq.acq_conf = ACQUISITION_CONFIG['acq_conf']
    logger.info('Inserting acquisition configuration from ACQUISITION_CONFIG dictionary')
except Exception:
    logger.warning('Coulkd not insert acquisition configuration')
    raise SystemError('Coulkd not insert acquisition configuration')

try:
    daq.horizontal_conf = ACQUISITION_CONFIG['horizontal']
    logger.info('Inserting hconf dic')
except Exception:
    logger.warning('Could not insert hconf dic')
    raise SystemError('Could not insert hconf dic')

try:
    daq.vertical_conf = ACQUISITION_CONFIG['vertical']
    logger.info('Inserting vconf dic')
except Exception:
    logger.warning('Could not insert vconf dic')
    raise SystemError('Could not insert vconf dic')

try:
    daq.chan_conf = ACQUISITION_CONFIG['chan_conf']
    logger.info('Inserting chan char dic')
except Exception:
    logger.warning('Could not insert chan char dic')
    raise SystemError('Could not insert chan char dic')

try:
    daq.trigger_dic = ACQUISITION_CONFIG['trigger']
    logger.info('Inserting trigger dic')
except Exception:
    logger.warning('Could not insert trigger dic')
    raise SystemError('Could not insert trigger dic')

#===============================================================================================
#Define NISCOPE session
#===============================================================================================

try:
    daq._session = ni.Session(devicename)
    logger.info('Creating new session!!!')
except Exception:
    logger.critical('Could not create new Niscope sesison')
    raise SystemError('Could not create new Niscope session')

try:
    if daq._session is not None:
        daq.config_trigger()
        logger.info('implementing trigger')
    else:
        pass
except Exception:
    logger.warning('Could not implement trigger')
    raise SystemError('Could not implement trigger')

#======================================================================
# GET DATA!
#======================================================================

try:
    logger.info(f'FSL is now outputting signal at {LO} Hz')
    fsl.set_output('ON')
    fsl.set_frequency(int(LO*1e-9)) # GHz
except Exception:
    logger.critical('FSL is not outputting signal!')

with daq._session as session:
    logger.info('Configuring channels')
    daq.configure_channels()
    logger.info('Executing trigger')
    sGen.RF_freq(RF) 
    sGen.pul_state(1)
    sGen.RF_state(1)
    data = {'CH0': [],
            'CH1': [],
            'CH2': [],
            'CH3': []}
    wf_info = []
    try:
        session.initiate()
        logger.info('Session initiated')
    except Exception:
        logger.critical('Could not initiate session')
    try:
        logger.info('Initiating fetching...')
        diodo.exec_trigger()
        waveforms = session.channels[0,1].fetch()
        logger.info('Converting wfm[0] into dictionary')
        data['CH0'] = np.array(waveforms[0].samples.tolist()) 
        logger.info('Converting wfm[1] into dictionary')
        data['CH1'] = np.array(waveforms[1].samples.tolist()) 
    except Exception:
        logger.error('Could not fetch!!') 
        sys.exit() 

fsl.set_output('OFF')
fsl.set_ref_out('OFF')
sGen.pul_state(0)
sGen.RF_state(0)

try:
    hdf5 = h5.HDF5()
    path = r'C:\\Users\\oper\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRSource\\API\\files\\'
    hdf5.name = 'DiodeMixer.hdf5'
    hdf5.dic = data
    hdf5.to_hdf5()
    logger.info('Transfering data from python dic to '+str(path+hdf5.name))
except Exception:
    logger.warning('Could not transfer data into '+str(path+hdf5.name))

try:
    logger.info('Trying to save data plot')
    fig = IQ_plotter(data)
    path = r'C:\\Users\\oper\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRSource\\API\\files\\'
    name = 'DiodeMixer.png'
    fig.savefig(path+name,'png')
except Exception:
    logger.warning('Could not save figure!')