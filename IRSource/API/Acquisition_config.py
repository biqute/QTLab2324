import niscope as ni
from datetime import datetime
import hightime
date = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

path = r"C:\\Users\\oper\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRSource\\API\\SingleFreq\\logs\\" 
name = date + ".log",

k = 4
sample_rate = 250e6
pulse_period = k * 1e-6
min_num_pts = int(sample_rate * pulse_period)

ACQUISITION_CONFIG = { 

    #====================================Vertical Configuration==================================
    
    'vertical': {
            'range': 0.5,
            'coupling': ni.VerticalCoupling.AC,
            'offset': 0.0,
            'probe_attenuation': 1,
            'enabled': True
        },

    #====================================Horizontal Configuration==================================

    'horizontal': {
            'sample_rate'     : sample_rate,
            'min_num_pts'     : int(sample_rate * pulse_period),
            'ref_position'    : 0,
            'num_records'     : 50,
            'enforce_realtime': True
        },

    #====================================Channels Configuration==================================

    'chan_conf': {
        'input_impedance': float(50),
        'max_frequency': 0
    },

    #====================================Triggers Configuration==================================

    'trigger': {
            'trigger_type'    : 'EDGE',
            'trigger_source': '3',
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
        'num_records' : 50                      ,        # number of records to store
        'channels'    : [0,1]                   ,        # list of enabled channels
        'sample_rate' : sample_rate             ,        # rate of points sampling of PXIe-5170R
        'length'      : 1000                    ,        # record length
        'timeout'     : hightime.timedelta(seconds=1.0),
        'relative_to' : ni.FetchRelativeTo.PRETRIGGER,
        'source_rate' : 700,                             #diode rate in hz
        'acq_time'    : 1,                               #acquisition time in seconds
        'offset'      : 0
    }
}
