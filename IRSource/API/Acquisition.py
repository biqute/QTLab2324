import sys
import niscope as ni
import json
sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\DAQ")
from DAQ import DAQ
from Acquisition_config import ACQUISITION_CONFIG
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def main():
    args = sys.argv[1:]
    #===============================================================================================
    #Save acquisition configuration parameters for DAQ configuration
    #===============================================================================================

    devicename = 'PXI1Slot3' 
    
    try:
        cfg1 = json.dumps(ACQUISITION_CONFIG)
        with open(ACQUISITION_CONFIG['cont_acq_conf']['path'] + 'config_' + ACQUISITION_CONFIG['cont_acq_conf']['file_name'] + '.json','w') as f:
            f.write(cfg1)
    except Exception:
        raise SystemError("Cannot Dump Config!")

    #===============================================================================================
    #Acquire DAQ configuration dictionaries
    #===============================================================================================

    daq = DAQ.DAQ(devicename)
    daq.get_status()
    #daq.reset_with_def()
    #daq.vertical_conf(ACQUISITION_CONFIG['vertical'])
    #daq.vertical_conf(ACQUISITION_CONFIG['horizontal'])
    #daq.vertical_conf(ACQUISITION_CONFIG['chan_char'])
    #daq.set_trigger_dic(ACQUISITION_CONFIG['trigger_dig'])
'''
    #===============================================================================================
    #Apply DAQ configuration dictionaries
    #===============================================================================================

    daq.get_status()
    daq.config_vertical()
    daq.config_hor_timing()
    daq.config_dig_trigger()    
    
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