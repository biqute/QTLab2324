import niscope as ni
from datetime import datetime
import hightime
date = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

path = r"C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IR_SING_PHOT\API" 
name = date + ".log",
records = 10
record_lenght = 10000
sample_rate  =250e6
low = 0.0010
high = 0.0015
window = ni.TriggerWindowMode.ENTERING

ACQUISITION_CONFIG = { 

    #====================================Vertical Configuration==================================
    
    'vertical': {
            'range': 0.05,
            'coupling': ni.VerticalCoupling.AC,
            'offset': 0.0,
            'probe_attenuation': 1,
            'enabled': True
        },

    #====================================Horizontal Configuration==================================

    'horizontal': {
            'sample_rate'     : sample_rate,
            'min_num_pts'     : record_lenght,
            'ref_position'    : 0,
            'num_records'     : records,
            'enforce_realtime': True
        },

    #====================================Channels Configuration==================================

    'chan_conf': {
        'input_impedance': float(50),
        'max_frequency': 0
    },

    #====================================Triggers Configuration==================================

    'trigger': {
            'trigger_type'    : ni.TriggerType.WINDOW,
            'low_level'       : low,
            'high_level'       : high,
            'window_mode'     : window, 
            'trigger_source': '0',
            'level': 0,
            'trigger_coupling': ni.TriggerCoupling.DC,
            'slope': ni.TriggerSlope.POSITIVE,
            'holdoff' : 0,
            'delay' : 0
        },
    #=================================Std. Acq. Configuration==================================

    'acq_conf': {
        'file_name'   : name                    ,        # name of the file where data will be saved
        'path'        : path                    ,        # path to directory for saving files (default is current)        'freq'        : [5.86512, 5.63622]      ,        # frequency chosen to study I and Q (GHz)
        'num_records' : records                 ,        # number of records to store
        'channels'    : [0,1]                   ,        # list of enabled channels
        'sample_rate' : sample_rate             ,        # rate of points sampling of PXIe-5170R
        'length'      : record_lenght           ,        # record length
        'timeout'     : hightime.timedelta(seconds=1.0),
        'relative_to' : ni.FetchRelativeTo.PRETRIGGER,
        'source_rate' : 700,                             #diode rate in hz
        'acq_time'    : 1,                               #acquisition time in seconds
        'offset'      : 0
    }
}
