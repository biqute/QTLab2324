import niscope as ni
from datetime import datetime
import hightime
date = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

path = r"C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IR_SING_PHOT\API" 
name = date + ".log",
records = 1
duration = 0.05
sample_rate  = 1e7
record_lenght = int(sample_rate * duration)
low = 0.0010
high = 0.0015
window = ni.TriggerWindowMode.ENTERING
I_mean =   -0.0012098545472224293
I_std  =    0.0010330664432030368
Q_mean =   -0.013278884023457258
Q_std  =    0.0009372143685608173

ACQUISITION_CONFIG = { 

    #====================================Vertical Configuration==================================
    
    'vertical': {
            'range': 1,
            'coupling': ni.VerticalCoupling.DC,
            'offset': 0.0,
            'probe_attenuation': 0,
            'enabled': True
        },

    #====================================Horizontal Configuration==================================

    'horizontal': {
            'sample_rate'           : sample_rate,
            'min_num_pts'           : record_lenght,
            'horz_record_lenght'    : record_lenght,
            'ref_position'          : 100.0,
            'num_records'           : records,
            'enforce_realtime'      : True
        },

    #====================================Channels Configuration==================================

    'chan_conf': {
        'input_impedance': float(50),
        'max_frequency': -1
    },

    #====================================Triggers Configuration==================================

    'trigger': {
            'trigger_type'    : ni.TriggerType.IMMEDIATE,
            'low_level'       : I_mean-5*I_std,
            'high_level'      : I_mean+5*I_std,
            'window_mode'     : window, 
            'trigger_source': '1',
            'level': 0.01,
            'trigger_coupling': ni.TriggerCoupling.DC,
            'slope': ni.TriggerSlope.POSITIVE,
            'holdoff' : 0,
            'delay' : 0
        },
    'tresholds' :{
        'I_mean' :  -0.0012098545472224293,
        'I_std'  :    0.0010330664432030368,
        'Q_mean' :   -0.013278884023457258,
        'Q_std'  :    0.0009372143685608173
    },
    #=================================Std. Acq. Configuration==================================

    'acq_conf': {
        'file_name'   : name                    ,        # name of the file where data will be saved
        'path'        : path                    ,        # path to directory for saving files (default is current)        'freq'        : [5.86512, 5.63622]      ,        # frequency chosen to study I and Q (GHz)
        'num_records' : records                 ,        # number of records to store
        'channels'    : [0,1]                   ,        # list of enabled channels
        'sample_rate' : sample_rate             ,        # rate of points sampling of PXIe-5170R
        'length'      : record_lenght           ,        # record length
        'timeout'     : hightime.timedelta(seconds=0.0),
        'relative_to' : ni.FetchRelativeTo.PRETRIGGER,
        'source_rate' : 700,                             #diode rate in hz
        'acq_time'    : 1,                               #acquisition time in seconds
        'offset'      : 0
    }
}
