import niscope as ni
from datetime import datetime
import hightime
date = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

path = r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\API\SingleFreq\logs\\" 
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
            'num_records'     : 1,
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
        'num_records' : 2                       ,        # number of records to store
        'channels'    : [0,1]                   ,        # list of enabled channels
        'sample_rate' : 250e6                   ,        # rate of points sampling of PXIe-5170R
        'length'      : 1000                    ,        # record length
        'timeout'     : hightime.timedelta(seconds=1.0),
        'relative_to' : ni.FetchRelativeTo.PRETRIGGER,
        'source_rate' : 700,                             #diode rate in hz
        'acq_time'    : 5,                               #acquisition time in seconds
        'offset'      : 0
    },   

    #=================================Cont. Acq. Configuration==================================

    'cont_acq_conf': {
        'path'              : path,
        'file_name'         : name,
        'sample_rate'       : 1e7 ,  # rate of points sampling of PXIe-5170R in Hz
        'total_acq_time'    : 0.1 ,  # total acquisition time in seconds
        'total_samples'     : 0.1 * 1e7,  # total number of points sampled
        'samples_per_fetch' : 1000 ,  # number of points sampled at a time during the acquisition
        'relative_to'       : ni.FetchRelativeTo.READ_POINTER,
        'offset'            : 0 ,
        'record_number'     : 0 ,
        'num_records'       : 1
    }   

}
