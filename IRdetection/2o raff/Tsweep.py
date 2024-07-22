import sys
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRdetection\Instruments\VNA')
sys.path.append(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRdetection\Instruments\Gas_Handler22')
import HP8753E as hp
import FridgeHandler as handler
import logging
import numpy as np
import time

def setup_logger(log_file=r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRdetection\2o raff\Logs\Tsweep.log', level=logging.DEBUG):
    """
    Set up a file logger with the specified log file and logging level.

    Parameters:
    - log_file: Name of the log file where logs will be written.
    - level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Create a formatter and set it for the file handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


#===============================TEST=================================================================
logger = setup_logger()
try:
    fridge = handler.FridgeHandler()
    logger.debug('Created fridge instance')
except:
    logger.warning('Could not create fridge instance')
try:
    fridge.set_control('remote')
    logger.debug('Setting fridge to remote control')
except:
    logger.warning('Could not set fridge to remote control')

outp = fridge.state()
logger.debug('Current fridge state is '+str(outp))

outp = fridge.get_sensor(3)
logger.debug('Current mixing chamber T is '+str(outp))

T = 200
fridge.set_mixc_temp(T)
logger.debug('Setting fridge T to '+str(T))

outp = fridge.get_sensor(3)
if outp!=T:
    logger.critical('Did not set temperature correctly!')
#====================================================================================================

#====================================================================================================

try:
    vna = hp.HP8753E()
    logger.debug('Creating VNA instance')
except:
    logger.critical('Could not create VNA instance!')

try:
    vna.ask_name()
except:
    logger.critical('Something is deeply wrong')

check, msg = vna.check_status()
logger.debug('Current VNA status is '+str(msg))
vna.set_chan('S21')
logger.debug('Setting channel S21')
vna.set_mode('SING')
logger.debug('Setting SING mode')
vna.set_meas('B')
logger.debug('Setting MEAS to B')

pw = -40
bw = 300
pt = 1601
ctr = 5.34e9
span = 2e7
try:
    vna.set_power(pw)
    logger.debug('Power: '+str(pw))
    vna.set_IFBW(bw)
    logger.debug('Power: '+str(bw))
    vna.set_points(pt)
    logger.dbug('Points are: '+str(pt))
    vna.set_center(ctr)
    logger.dbug('Center is: '+str(ctr))
    vna.set_span(span)
    logger.dbug('Span is: '+str(span))
except:
    logger.warning('Could not set parameters!')

temps = np.arange(200,30,-10)
res = [5.3465, 5.5757, 5.6748, 5.98126]
t1 = 0

for T in temps:
    fridge.set_mxc_temp(T)
    while(T in range(t1-5,t1+5)):
        time.sleep(30)
        t1 = fridge.get_sensor(3)
    logger.debug('Temperature is : '+str(T))
    vna.set_save_path(r'C:\Users\ricca\Desktop\MAGISTRALE\QTLab2324\IRdetection\2o raff\Data\T_'+str(T))
    for k,r in enumerate(res):
        try:
            vna.set_center(r)
            logger.debug('Power: '+str(pw))
            i,q,f =vna.get_IQF_center()
            logger.debug('Getting data...')
            vna.create_run_file(k,i,q,f)
            logger.debug('Run file created')
        except:
            logger.warning('Something went wrong!!')