#===============================================================================================
import sys
sys.path.append(r"C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRSource\AFG310")
sys.path.append(r"C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRSource\Synth")
sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\KIDs\QTLab2324\IRSource\DAQ")
sys.path.append(r"C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRSource\API\logs")
sys.path.append(r'C:\Users\oper\SynologyDrive\Lab2023\KIDs\QTLab2324\IRSource\Exceptions')
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRSource\HDF5')
#===============================================================================================

from IRSource import diodo
from IRSource.Synth import Synthesizer
from DAQ import DAQ
from AFG310 import diode
import json
from Acquisition_config import ACQUISITION_CONFIG
import logging
from logging.config import dictConfig
from logs.logging_config import LOGGING_CONFIG
from Exceptions import replace_non_serializable
import numpy as np
import niscope as ni
from HDF5 import HDF5 as h5
import Tools 

#===============================================================================================
#Save acquisition configuration parameters for DAQ configuration
#===============================================================================================

filepath = r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRSource\Runs'

#===============================================================================================
#Import logger configuration
#===============================================================================================
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('START EXECUTION')

devicename = 'PXIeSlot1'
sGen_board = ''


try:
    cfg1 = json.dumps(replace_non_serializable(ACQUISITION_CONFIG))
    logger.info('Dumping acquisition configuration')
    with open(ACQUISITION_CONFIG['acq_conf']['path'] + 'config.json','w') as f:
        f.write(cfg1)
except Exception:
    logger.critical('Dumping acquisition configuration')
    raise SystemError("Could not dump acquisition configuration!")

#===============================================================================================
#Acquire DAQ configuration dictionaries
#===============================================================================================

res = 5.5757
sgen_board = ''
amplitude = 0
f = 0

try:
    daq = DAQ()
    logger.info('DAQ class object correctly created')
except Exception:
    logger.critical('Could not crate DAQ class object')
    raise SyntaxError('Could not create DAQ class object')

try:
    s1 = Synthesizer.Synthesizer(1)
    s1.connettore()
    logger.info('Synth class object correctly created and connected!')
except Exception:
    logger.critical('Could not crate synth class object')
    raise SyntaxError('Could not create synth class object')


channels = {'I'			: 0, 
            'Q'			: 1,
            'trigger'	: 0}


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
#Configure session
#===============================================================================================

try:
    daq._session = ni.Session(devicename)
    logger.info('Creating new session!!!')
except Exception:
    logger.critical('Could not create new Niscope sesison')
    raise SystemError('Could not create new Niscope session')

#===============================================================================================
#Configure trigger
#===============================================================================================

try:
    if daq._session is not None:
        daq.config_trigger()
        logger.info('implementing trigger')
    else:
        pass
except Exception:
    logger.warning('Could not implement trigger')
    raise SystemError('Could not implement trigger')

#===============================================================================================
#GET DATA!
#===============================================================================================

runs = 1000 # runs number        

with daq._session as session:
    logger.info('Configuring channels')
    daq.configure_channels()
    data = {'CH0': [],
            'CH1': [],
            'CH2': [],
            'CH3': []}
    wfm = []
    
    for run in range(runs):
        
        LO = res
        try:
            s1.set_frequency(LO)
            s1.outp_frequency_on()
            logger.info(f'Synth 1 is now outputting signal at {LO} GHz')
        except Exception:
            logger.critical('FSL is not outputting signal!')

        try:
            daq._session.initiate()
            logger.info('Initiating fetching...')
            waveforms = session.channels[0,1].fetch()
            logger.info('Converting wfm[0] into dictionary')
            
            logger.info('Converting wfm[1] into dictionary')
             
        except Exception:
            logger.error('Could not fetch!!')
            sys.exit()

        try:
            data['CH0'] = np.array(waveforms[0].samples.tolist())
            data['CH1'] = np.array(waveforms[1].samples.tolist())
            hdf5 = h5.HDF5()
            path = r'C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IR_SING_PHOT\API\Noise_data\\'
            hdf5.name = 'Run_'+str(res)+'.hdf5'
            hdf5.dic = data
            hdf5.to_hdf5()
            logger.info('Transfering data from python dic to '+str(path+hdf5.name))
        except Exception:
            logger.warning('Could not transfer data into '+str(path+hdf5.name))

try:
    s1.outp_frequency_off()
    logger.info('Synth stopped outputting signal')
except Exception:
    logger.critical("Synth hasn't stopped outputting signal!")