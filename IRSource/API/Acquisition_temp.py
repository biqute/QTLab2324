import sys

from IRSource.diodo.diodo import trigger
sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Logger")
sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\DAQ")
sys.path.append(r'C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Logger\logs\sessions')
sys.path.append(r'C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Exceptions')
import json
from DAQ import DAQ
from Acquisition_config import ACQUISITION_CONFIG
import logging
from logging.config import dictConfig
from logs.logging_config import LOGGING_CONFIG
from  Exceptions import replace_non_serializable, trai
from PAmodules.QuickSyn import FSL_0010
from PAmodules.network.RS_Signal_Generator import RS_SMA100B
from niscope.errors import DriverError
import numpy as np
import niscope as ni
import matplotlib.pyplot as plt

#===============================================================================================
#Save acquisition configuration parameters for DAQ configuration
#===============================================================================================

ip   = '192.168.40.15'   # Set IP address of SMA
devicename = 'PXI1Slot3' 

#===============================================================================================
#Import logger configuration
#===============================================================================================
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('START EXECUTION')

try:
    cfg1 = json.dumps(replace_non_serializable(ACQUISITION_CONFIG))
    logger.info('Dumping acquisition configuration')
    print(ACQUISITION_CONFIG['acq_conf']['path'])
    with open(ACQUISITION_CONFIG['acq_conf']['path'] + '.json','w') as f:
        f.write(cfg1)
except Exception:
    logger.critical('Dumping acquisition configuration')
    raise SystemError("Could not dump acquisition configuration!")

#===============================================================================================
#Acquire DAQ configuration dictionaries
#===============================================================================================

try:
    daq = DAQ(devicename)
    logger.info('DAQ class object correctly created')
except Exception:
    logger.critical('Could not crate DAQ class object')
    raise SyntaxError('Could not create DAQ class object')

try:
    fsl = FSL_0010.FSL10_synthesizer(device_address='COM37')
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
    k = 2                                                               # coefficiente per prendere k*1000 punti                                                                     
    pulse_freq      = 1.010e9
    amplitude       = -18                                               # Set the amplitude of the signal in dBm
    sample_rate     = 250e6                                             # Maximum Value: 250.0e6
    pulse_width     = k * 3e-6                                          # min 5ns                             
    pulse_delay     = 0
    pulse_period    = k * 5e-6                                          # min 20ns
    sGen.reset()
    sGen.clear()
    sGen.pul_gen_params(delay = pulse_delay, width = pulse_width, period = pulse_period)   # da capire quale pulse width
    sGen.pul_gen_mode('SING')
    sGen.pul_trig_mode('SING')
    sGen.RF_freq(pulse_freq)
    sGen.RF_lvl_ampl(amplitude)
    logger.info('SMA set up correctly')
except Exception:
    logger.critical('Could not set up SMA')
    raise SystemError('Could not create SMA class object')

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
    raise SystemError('Could not restet DAQ with defaults')

try:
    daq.horizontal_conf(ACQUISITION_CONFIG['horizontal'])
    logger.info('Inserting hconf dic')
except Exception:
    logger.warning('Could not insert hconf dic')
    raise SystemError('Could not insert hconf dic')

try:
    daq.vertical_conf(ACQUISITION_CONFIG['vertical'])
    logger.info('Inserting hconf dic')
except Exception:
    logger.warning('Could not insert vconf dic')
    raise SystemError('Could not insert vconf dic')

try:
    daq.chan_conf(ACQUISITION_CONFIG['chan_conf'])
    logger.info('Inserting chan char dic')
except Exception:
    logger.warning('Could not insert chan char dic')
    raise SystemError('Could not insert chan char dic')

try:
    daq.set_trigger_dic(ACQUISITION_CONFIG['trigger_dig'])
    logger.info('Inserting trigger dic')
except Exception:
    logger.warning('Could not insert trigger dic')
    raise SystemError('Could not insert trigger dic')

#===============================================================================================
#Apply DAQ configuration dictionaries
#===============================================================================================

try:
    daq.config_hor_timing()
    logger.info('Implementing horizontal configuration')
except Exception:
    logger.warning('Could not implement horizontal configuration')
    raise SystemError('Could not implement horizontal configuration')

try:
    daq.enable_channels()
    logger.info('Enabling all channels')
except Exception:
    logger.warning('Could not enable channels!')
    raise SystemError('Could not enable channels!')

try:
    daq.config_vertical()
    logger.info('Implementing vertical configuration')
except Exception:
    logger.warning('Could not implement vertical configuration')
    raise SystemError('Could not implement vertical configuration')

try:
    daq.config_chan_char()
    logger.info('Implementing channels configuration')
except Exception:
    raise SystemError('Could not implement channels configuration')

try:
    daq.config_chan_char()
    logger.info('Implementing channels configuration')
except Exception:
    raise SystemError('Could not implement channels configuration')

try:
    daq.config_edge_trigger()
    logger.info('implementing edge trigger')
except Exception:
    logger.warning('Could not implement edge trigger')
    raise SystemError('Could not implement edge trigger')
    
#===============================================================================================
#Test DAQ configuration
#===============================================================================================

try:
    daq.test()
    logger.info('Testing DAQ actual configuration')
except Exception:
    logger.critical('DAQ test gone wrong!')

#===============================================================================================
#GET DATA!
#===============================================================================================
fsl.set_frequency(1) # GHz
fsl.set_output('ON')
sGen.RF_freq(pulse_freq) 
sGen.pul_state(1)
sGen.RF_state(1)

try:
    waveforms, infos = daq.singleac(sGen.pul_exe_sing_trig)
    logger.info('Retrieving data...')
except Exception:
    logger.error('Could not retrieve data!')
    raise SystemError ('Could not retrieve data!')

daq._session.close()