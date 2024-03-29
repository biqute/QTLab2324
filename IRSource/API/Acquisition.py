import IRSource.PXIe5170R.DAQ as DAQ
import sys
import niscope as ni
import datetime
import hightime
import json

def get_date(file_name = None):
    now = datetime.now()
    date= now.strftime("%d%m%y")
    hour = now.strftime("%H%M%S")
    name = file_name + '_' + date + '_' + hour
    return (date, hour) if file_name == None else name


def main():
    args = sys.argv[1:]
    #===============================================================================================
    #Initial parameters for DAQ configuration
    #===============================================================================================

    name = get_date(file_name = 'test')
    device_name = None
    device_address = 'PXI1Slot2'
    id = None
    rd = None
    
    dic = {} 
    
    vertical = {
        'range': 1,
        'coupling': ni.VerticalCoupling.DC,
        'offset': 0.0,
        'probe_attenuation': 0.0,
        'enabled': True
    }    
    
    horizontal = {
        'min_sample_rate': 5e7,
        'min_num_pts': 1000,
        'ref_position': float(),
        'num_records': 10000,
        'enforce_realtime': True
    }
    
    chan_char = {
        'input_impedance': float(50), #(50 Ohms?)
        'max_input_frequency': float()
    }
        
    trigger = {
        'trigger_type'    : 'EDGE',
        'trigger_source'  : '1',
        'level'           : '-0.031',
        'trigger_coupling': None,
        'slope'           : 'POSITIVE',
        'holdoff'         : 0.0,
        'delay'           : 0.0       
    }
    
    acq_conf = {
        'file_name'   : name                    ,        # name of the file where data will be saved
        'path'        : ''                       ,       # path to directory for saving files (default is current)
        'freq'        : [5.86512, 5.63622]      ,        # frequency chosen to study I and Q (GHz)
        'num_records' : 10000                   ,        # number of records to store
        'channels'    : [0,1,2,3]               ,        # list of enabled channels
        'sample_rate' : 5e7                     ,        # rate of points sampling of PXIe-5170R
        'length'      : 6000                    ,        # record length
        'resonators'  : [0,1]                   ,        # list of resonators used, it's probably a useless variable
        'timeout'     : hightime.timedelta(seconds=5.0),
        'relative_to' : ni.FetchRelativeTo.PRETRIGGER,
        'source_rate' : 700 #diode rate in hz
    }   
    
    cont_acq_conf = {
        'path'              : '',
        'file_name'         : name,
        'sample_rate'       : 1e7 ,  # rate of points sampling of PXIe-5170R in Hz
        'total_acq_time'    : 0.1 ,  # total acquisition time in seconds
        'total_samples'     : int(cont_acq_conf['total_acq_time'] * cont_acq_conf['sample_rate'])   ,  # total number of points sampled
        'samples_per_fetch' : 1000 ,  # number of points sampled at a time during the acquisition
        'relative_to'       : ni.FetchRelativeTo.READ_POINTER,
        'offset'            : 0 ,
        'record_number'     : 0 ,
        'num_records'       : 1
    }    
    
    cfg1 = json.dumps(vertical)
    cfg2 = json.dumps(horizontal)
    cfg3 = json.dumps(chan_char)
    with open(cont_acq_conf['path'] + 'config_' + cont_acq_conf['file_name'] + '.json','w') as f:
        f.write(cfg1)
        f.write(cfg2)
        f.write(cfg3)

    coefficients = [] 

    #===============================================================================================
    #Initialize DAQ session
    #===============================================================================================

    handler = DAQ.DAQ(device_name, device_name, device_address, id, rd, acq_conf, vertical, horizontal, chan_char, coefficients, trigger, dic)
    handler.logger.debug('Frequency: '     + str(acq_conf['freq']))
    handler.logger.debug('Filename: '      + str(acq_conf['file_name']))
    handler.logger.debug('Records: '       + str(acq_conf['records']))
    handler.logger.debug('Channels: '      + str(acq_conf['channels']))
    handler.logger.debug('Sample rate: '   + str(acq_conf['sample_rate']))
    handler.logger.debug('Length: '        + str(acq_conf['length']))

    #===============================================================================================
    #Set and test DAQ configuration
    #===============================================================================================

    #handler.config_chan_char()
    handler.config_vertical()
    handler.config_hor_timing()

    #handler.calibrate()
    #handler.test()
    handler.get_status()

    #===============================================================================================
    #Set trigger type and properties
    #===============================================================================================

    if (trigger['trigger_type']=='IMMEDIATE'):
        handler.config_imm_trigger()
    elif (trigger['trigger_type']=='EDGE'):
        handler.config_edge_trigger()
    elif (trigger['trigger_type']=='DIGITAL'):
        handler.config_dig_trigger()
    elif (trigger['trigger_type']=='SOFTWARE'):
        handler.config_software_trigger()
        
    #===============================================================================================
    #Initiate Acquisition
    #===============================================================================================
    
    if (args[1]=='SINGLE'):
        
        handler.initiate()
        handler.fetch()      
        handler.fill_matrix(return_data=False)
        handler.storage_hdf5(cont_acq_conf['path'] + cont_acq_conf['file_name'] + '.h5')
        handler.close()
        
        #save config for data analysis
        cfg = json.dumps(acq_conf)
        with open(acq_conf['path'] + 'config_' + acq_conf['file_name'] + '.json','w') as f:
            f.write(cfg)

        handler.logger.info('END EXECUTION\n\n')
        
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