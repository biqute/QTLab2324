import IRSource.PXIe5170R.DAQ as DAQ
import sys
import niscope as ni
import datetime

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

    config = {
        'freq'        : [5.86512, 5.63622]      ,        # frequency chosen to study I and Q (GHz)
        'file_name'   : name                    ,        # name of the file where data will be saved
        'records'     : 10000                   ,        # number of records to store
        'channels'    : [0,1,2,3]               ,        # list of enabled channels
        'sample_rate' : 5e7                     ,        # rate of points sampling of PXIe-5170R
        'length'      : 6000                    ,        # record length
        'resonators'  : [0,1]                   ,        # list of resonators used, it's probably a useless variable
        'source_rate' : 700 #diode rate in hz
    }               

    trigger = dict(
        trigger_type   = 'EDGE',         #'EDGE', 'IMMEDIATE', 'DIGITAL', 'SOFTWARE'
        trigger_source = '1',
        trigger_slope  = 'POSITIVE',          #'POSITIVE' or 'NEGATIVE'
        trigger_level  = '-0.031',
        trigger_delay  = '0.0'
    )

    trigger_source, level, trigger_coupling, slope=niscope.TriggerSlope.POSITIVE, holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0)

    config['trigger'] = trigger
    config['ADCmax']  =  5
    config['ADCmin']  = -5
    config['ADCnbit'] = 14

    ###########

    # Logging all the setting infos
    handler.logger.debug('Frequency: '     + str(config['freq']))
    handler.logger.debug('Filename: '      + str(config['file_name']))
    handler.logger.debug('Records: '       + str(config['records']))
    handler.logger.debug('Channels: '      + str(config['channels']))
    handler.logger.debug('Sample rate: '   + str(config['sample_rate']))
    handler.logger.debug('Length: '        + str(config['length']))

    for key in trigger:
        handler.logger.debug(str(key) + ': '   + trigger[key])



    device_name = _
    device_address = _ 
    id = _
    rd = _
    dic = {} 
    vertical = {}
    horizontal = {}
    chan_char = {}
    trigger = {}
    acq_conf = {}
    coefficients = [] 

    #===============================================================================================
    #Initialize DAQ session
    #===============================================================================================

    handler = DAQ.DAQ(device_name, device_address, id, rd, dic, vertical, horizontal, chan_char, coefficients)

    #===============================================================================================
    #Set and test DAQ configuration
    #===============================================================================================

    handler.config_chan_char()
    handler.config_vertical()
    handler.config_hor_timing()

    handler.calibrate()
    handler.test()
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
