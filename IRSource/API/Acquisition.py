import sys
sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Logger")
sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\DAQ")
sys.path.append(r'C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Logger\logs\sessions')
import json
from DAQ import DAQ
from Acquisition_config import ACQUISITION_CONFIG
import logging
from logging.config import dictConfig
from logs.logging_config import LOGGING_CONFIG
from synth import synth

def replace_non_serializable(obj):
    if isinstance(obj, dict):
        return {k: replace_non_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [replace_non_serializable(item) for item in obj]
    elif isinstance(obj, (int, float, bool, str)):
        return obj
    else:
        # Convert non-serializable value to its string representation
        return str(obj)


args = sys.argv[1:]
#===============================================================================================
#Save acquisition configuration parameters for DAQ configuration
#===============================================================================================

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
    stat = daq.sh.session.get_status()
    logger.info('DAQ status: '+str(stat))
except Exception:
    logger.critical('Could not get DAQ status!')
    raise SystemError('Could not get DAQ status')

try:
    daq.sh.session.reset_with_def()
    daq.sh.session.get_status
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
    daq.trigger_dic = ACQUISITION_CONFIG['trigger']
    daq.config_trigger()
    logger.info('Inserting trigger dic')
except Exception:
    logger.warning('Could not insert trigger dic')
    raise SystemError('Could not insert trigger dic')


#===============================================================================================
#Test DAQ configuration
#===============================================================================================


try:
    daq.sh.session.test()
    logger.info('Testing DAQ actual configuration')
except Exception:
    logger.critical('DAQ test gone wrong!')

#===============================================================================================
#Set-up Synthesizers
#===============================================================================================

s1 = synth('ASRL26::INSTR')
logger.info(f'Connecting synth 1|Name : {s1.name}, Board: {s1.board}')
s2 = synth('ASRL5::INSTR')
logger.info(f'Connecting synth 2|Name : {s2.name}, Board: {s2.board}')

s1.set_frequency('1GHz')
logger.info('Setting 1st freq to 1GHz')
s2.set_frequency('1.005GHz')
logger.info('Setting 2nd freq to 1.005GHz')

s1.set_power('15')
logger.info('Setting 1st pwoer to 15 dBm')
s2.set_power('1.005GHz')
logger.info('Setting 2nd power to 15 dBm')


#===============================================================================================
#Output signal
#===============================================================================================
try:
    s1.set_outpt_stat('ON')
    logger.info('1st synth is outputting signal')
except Exception:
    logger.error('1st synth is NOT outputting signal')
try:
    s2.set_outpt_stat('ON')
    logger.info('1st synth is outputting signal')
except Exception:
    logger.error('2nd synth is NOT outputting signal')
    
#===============================================================================================
#Acquire data
#===============================================================================================