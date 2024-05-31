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
    cfg1 = json.dumps(ACQUISITION_CONFIG)
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
    raise SystemError('Could not implement horizontal configuration')

try:
    daq.config_vertical()
    logger.info('Implementing vertical configuration')
except Exception:
    raise SystemError('Could not implement vertical configuration')
'''
try:
    daq.config_chan_char()
    logger.info('Implementing channels configuration')
except Exception:
    raise SystemError('Could not implement channels configuration')


#===============================================================================================
#Test DAQ configuration
#===============================================================================================

daq.get_status()
daq.test()
daq.available()

 
#===============================================================================================
#Initiate Acquisition
#===============================================================================================

if (args[1]=='SINGLE'):
    
    with daq.initiate():
        waveforms = daq._instance._session.channels[0,1,2,3].fetch()
    for wfm in waveforms:
        print('Channel {0}, record {1} samples acquired: {2:,}\n'.format(wfm.channel, wfm.record, len(wfm.samples)))
    a = wfm[0].samples.tolist()
    plt.figure()
    plt.plot(np.arange(len(a))/250e6, a)
    plt.savefig('test'+datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))

'''
'''
    daq._instance.logger.info('END EXECUTION\n\n')
    
elif  (args[1]=='CONTINUOUS'):
    if handler.trigger["trigger_type"] == 'CONTINUOS':
        handler.config_software_trigger()
    else:
        handler._session.trigger_type       = getattr(ni.TriggerType, handler.trigger["trigger_type"])
        handler._session.trigger_source     = handler.trigger["trigger_source"]
        handler._session.trigger_slope      = getattr(ni.TriggerSlope, handler.trigger["trigger_slope"])
        handler._session.trigger_level      = float(handler.trigger["trigger_level"])
        handler._session.trigger_delay_time = float(handler.trigger["trigger_delay"])
    
    handler.initiate()
    handler.continuous_acq()        
    handler.close()
    
    #save config for data analysis
    cfg = json.dumps(cont_acq_conf)
    with open(cont_acq_conf['path'] + 'config_' + cont_acq_conf['file_name'] + '.json','w') as f:
        f.write(cfg)

    handler.logger.info('END EXECUTION\n\n')

    try:
        handler.initiate()
        handler.waveform.extend([handler._session.channels[i].fetch(num_samples=handler.acq_conf['length'], timeout=acq_conf['timeout'], relative_to=acq_conf['relative_to'], num_records=acq_conf['num_records']) for i in handler.channels])
        handler.logger.debug('Time from the trigger event to the first point in the waveform record: ' + str(handler._session.acquisition_start_time))
        handler.logger.debug('Actual number of samples acquired in the record: ' + str(handler._session.points_done))
        handler.logger.debug('Number of records that have been completely acquired: ' + str(handler._session.records_done))
    except Exception as e:
        handler.logger.debug("Extending waveform went wrong")
        raise MemoryError("Extending waveform went wrong")

    handler.acq()        
    handler.fill_matrix(return_data=True)
    handler.storage_hdf5()
'''       