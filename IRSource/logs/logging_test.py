import logging
import logging
import json
from logging.config import dictConfig
from DAQ_config import LOGGING_CONFIG
import pathlib

# LOG SYSTEM
dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
logger.info('START EXECUTION')
name = "test.log"
path = r'F:\\LabIV\\QTLab2324\\IRSource\\logs\\sessions\\'

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

# Logging all the setting infos
logger.info('Frequency: '     + str(config['freq']))
logger.info('Filename: '      + str(config['file_name']))
logger.info('Records: '       + str(config['records']))
logger.info('Channels: '      + str(config['channels']))
logger.info('Sample rate: '   + str(config['sample_rate']))
logger.info('Length: '        + str(config['length']))

for key in trigger:
    logger.info(str(key) + ': '   + trigger[key])
    
# save config for data analysis
cfg = json.dumps(config)
with open(path + 'config_' + config['file_name'] + '.json', 'w') as f:
    f.write(cfg)

logger.debug('Saved config for data analysis: config_' + config['file_name'] + '.json')
logger.info('END EXECUTION\n\n')