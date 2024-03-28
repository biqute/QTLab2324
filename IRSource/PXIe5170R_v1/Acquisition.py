import logging
import json
import time
import sys
import datetime
import niscope as ni
from logging.config import dictConfig
from logs.DAQ_config import LOGGING_CONFIG
import DAQ

# LOG SYSTEM
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('Start acquisition')

path = r"F:\\LabIV\\QTLab2324\\IRSource\\logs\\sessions\\"
file_name = "test"
now = datetime.now()
date= now.strftime("%d%m%y")
hour = now.strftime("%H%M%S")
name = file_name + '_' + date + '_' + hour

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
    trigger_type   = 'EDGE',         #'EDGE', 'IMMEDIATE' or 'DIGITAL'
    trigger_source = '1',
    trigger_slope  = 'POSITIVE',          #'POSITIVE' or 'NEGATIVE'
    trigger_level  = '-0.031',
    trigger_delay  = '0.0'
)

config['trigger'] = trigger
config['ADCmax']  =  5
config['ADCmin']  = -5
config['ADCnbit'] = 14

###########

# Logging all the setting infos
logger.debug('Frequency: '     + str(config['freq']))
logger.debug('Filename: '      + str(config['file_name']))
logger.debug('Records: '       + str(config['records']))
logger.debug('Channels: '      + str(config['channels']))
logger.debug('Sample rate: '   + str(config['sample_rate']))
logger.debug('Length: '        + str(config['length']))

for key in trigger:
    logger.debug(str(key) + ': '   + trigger[key])

# Decide how many points we want based on signal length and sample_rate
# It seems that length indicates how long it is open, if it is 10k but the trigger goes off after 1000 it takes 9k (..?)


handle = DAQ.DAQ('PXI1Slot2', trigger=trigger, records=config['records'], channels=config['channels'], sample_rate=config['sample_rate'], length=config['length'], ref_pos=20.0)
handle.calibrate()
handle.test()
handle.config_vertical(range=1, coupling=ni.VerticalCoupling.DC)
handle.config_hor_timing(handle.sample_rate, handle.length, handle.ref_pos, handle.records, handle.encorceRT)

handle.fetch(timeout=10)
handle.fill_matrix()
handle.storage_hdf5(path + config['file_name'] + '.h5')

# save config for data analysis
cfg = json.dumps(config)
with open(path + 'config_' + config['file_name'] + '.json', 'w') as f:
    f.write(cfg)

logger.debug('Saved config for data analysis: config_' + config['file_name'] + '.json')
logger.info('END EXECUTION\n\n')