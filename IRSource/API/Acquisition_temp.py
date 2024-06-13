import sys

sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Logger")
sys.path.append(r"C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\DAQ")
sys.path.append(r'C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Logger\logs\sessions')
sys.path.append(r'C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324\IRSource\Exceptions')
import json
from DAQ import DAQ
from Acquisition_config import ACQUISITION_CONFIG
import logging
from logging.config import dictConfig
from logs.logging_config import LOGGING_CONFIG
from  Exceptions import replace_non_serializable, trai
from PAmodules.QuickSyn import FSL_0010
from PAmodules.network.RS_Signal_Generator import RS_SMA100B
from niscope.errors import DriverError
import numpy as np
import niscope as ni
from PAmodules import Tools
import os

#===============================================================================================
#Save acquisition configuration parameters for DAQ configuration
#===============================================================================================

ip   = '192.168.40.15'   # Set IP address of SMA
devicename = 'PXI1Slot3' 

#===============================================================================================
#Import logger configuration
#===============================================================================================
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info('START EXECUTION')

try:
    cfg1 = json.dumps(replace_non_serializable(ACQUISITION_CONFIG))
    logger.info('Dumping acquisition configuration')
    print(ACQUISITION_CONFIG['acq_conf']['path'])
    with open(ACQUISITION_CONFIG['acq_conf']['path'] + '.json','w') as f:
        f.write(cfg1)
except Exception:
    logger.critical('Dumping acquisition configuration')
    raise SystemError("Could not dump acquisition configuration!")

#===============================================================================================
#Acquire DAQ configuration dictionaries
#===============================================================================================

try:
    daq = DAQ()
    logger.info('DAQ class object correctly created')
except Exception:
    logger.critical('Could not crate DAQ class object')
    raise SyntaxError('Could not create DAQ class object')

try:
    fsl = FSL_0010.FSL10_synthesizer(device_address='COM31')
    logger.info('FSL_0010 class object correctly created')
except Exception:
    logger.critical('Could not crate FSL class object')
    raise SyntaxError('Could not create FSL class object')

try:
    sGen = RS_SMA100B.SMA100B(ip)
    logger.info('SMA class object correctly created')
except Exception:
    logger.critical('Could not crate SMA class object')
    raise SyntaxError('Could not create SMA class object')

try:
    LO =  8.5e9 
    pulse_f_min     = LO + 10e6
    amplitude       = 0  
    sample_rate     = 250e6
    k               = 4
    pulse_period    = k * 1e-6
    num_points      = int(sample_rate * pulse_period)
    percent         = 5
    pulse_width     = pulse_period * (1-percent/100)
    pulse_delay     = 0
    
    sGen.reset()
    sGen.clear()
    sGen.pul_gen_params(delay = pulse_delay, width = pulse_width, period = pulse_period)  
    sGen.pul_gen_mode('SING')
    sGen.pul_trig_mode('SING')

    channels = {'I'			: 0, 
			    'Q'			: 1,
			    'trigger'	: 3}
    logger.info('SMA set up correctly')
except Exception:
    logger.critical('Could not set up SMA')
    raise SystemError('Could not create SMA class object')

try:
    stat = daq.get_status
    logger.info('DAQ status: '+str(stat))
except Exception:
    logger.critical('Could not get DAQ status!')
    raise SystemError('Could not get DAQ status')

try:
    daq.reset_with_def()
    daq.get_status
    logger.info('Resetting DAQ with defaults')
except Exception:
    logger.error('Could not reset DAQ with defaults')
    pass
    #raise SystemError('Could not restet DAQ with defaults')

try:
    daq.acq_conf = ACQUISITION_CONFIG['acq_conf']
    logger.info(f'Inserting acquisition configuration from ACQUISITION_CONFIG dictionary')
except Exception:
    logger.warning('Coulkd not insert acquisition configuration')
    raise SystemError('Coulkd not insert acquisition configuration')

try:
    daq.horizontal_conf = ACQUISITION_CONFIG['horizontal']
    logger.info('Inserting hconf dic')
except Exception:
    logger.warning('Could not insert hconf dic')
    raise SystemError('Could not insert hconf dic')

try:
    daq.vertical_conf = ACQUISITION_CONFIG['vertical']
    logger.info('Inserting vconf dic')
except Exception:
    logger.warning('Could not insert vconf dic')
    raise SystemError('Could not insert vconf dic')

try:
    daq.chan_conf = ACQUISITION_CONFIG['chan_conf']
    logger.info('Inserting chan char dic')
except Exception:
    logger.warning('Could not insert chan char dic')
    raise SystemError('Could not insert chan char dic')

try:
    daq.trigger_dic = ACQUISITION_CONFIG['trigger']
    logger.info('Inserting trigger dic')
except Exception:
    logger.warning('Could not insert trigger dic')
    raise SystemError('Could not insert trigger dic')

#===============================================================================================
#Configure session
#===============================================================================================

try:
    daq._session = ni.Session(devicename)
    logger.info('Creating new session!!!')
except Exception:
    logger.critical('Could not create new Niscope sesison')
    raise SystemError('Could not create new Niscope session')


#===============================================================================================
#Configure trigger
#===============================================================================================

try:
    if daq._session is not None:
        daq.config_trigger()
        logger.info('implementing trigger')
    else:
        pass
except Exception:
    logger.warning('Could not implement trigger')
    raise SystemError('Could not implement trigger')
    


#===============================================================================================
#GET DATA!
#===============================================================================================
fsl.set_frequency(LO) # GHz
fsl.set_output('ON')
pula = np.arange(pulse_f_min, pulse_f_min + 0.010e9, 0.010e9)
data_dict   = {'power_(dBm)': amplitude, 'power_(mV peak)': round(Tools.dBm_to_mVpk(amplitude),3), 'freqs': {}}
counter     = 1

digits_f = "{:0"+str(len(str(len(pula))))+"d}"
sGen.RF_lvl_ampl(amplitude)

with daq._session as session:
    daq.configure_channels()
    logger.info('Executing trigger')

    for i, pul in enumerate(pula):
        logger.info('Looping on frequency '+str(i)+' : '+str(pul))
        sGen.RF_freq(pul) 
        sGen.pul_state(1)
        sGen.RF_state(1)
        logger.info('Initiating session')
        wf_info = []
        logger.info('Initiating fetching...')
        try:
            waveforms = session.channels[0,1].fetch()#num_samples=total_samples, relative_to=daq._acq_conf['relative_to'], offset=daq._acq_conf['offset'], record_number=daq._acq_conf['num_records'], timeout=daq._acq_conf['timeout'])
        except Exception:
            logger.error('Could not fetch!!')
            raise SystemError('BASTARDO!')
        dict = {'input_freq_(Hz)'	: pul}
        for key, value in channels.items():
            logger.info('Looping on channel ' + str(value))
            if key == 'trigger' or value is None:
                continue
            dict[key] = np.array(waveforms[value].samples.tolist())
            FT = np.abs(np.fft.fft(dict[key]))
            N = len(dict[key])
            T = 1/sample_rate
            freqs = np.fft.fftfreq(N,T) 
            dict[key+'_freq'] = round(freqs[np.argmax(FT[:N // 2])], 3)
            dict[key+'_power'] = round(Tools.get_avg_power(y = dict[key], toggle_plot = False, sample_rate = sample_rate)['mean']*1e3, 3)
        sGen.pul_state(0)
        sGen.RF_state(0)

        print(f'\rf{digits_f.format(i)}	: {int(counter*100/len(pula))} %\n', end='')
        sys.stdout.flush()
        counter += 1
        data_dict['freqs'][f'f{digits_f.format(i)}'] = dict
    print(fsl.set_output('OFF'))

try:
    logger.info('Creating new acquisition hdf5 file!!')
    cam = 'C:\\Users\\oper\\SynologyDrive\\Lab2023\\Qubit\\QTLab2324\\IRSource\\API\\hdf5_temp_files\\'
    filename = f'Mixer_1135_{round(LO*1e-9,1)}GHz.h5'
    if os.path.exists(filename+cam):
        os.remove(filename+cam)
    Tools.save_dict_to_hdf5(data_dict, filename+cam)
except Exception:
    logger.critical('Could not create file!')







'''
total_samples = int(daq._acq_conf['acq_time'] * daq._acq_conf['sample_rate'])
with daq._session as session:
    sGen.pul_exe_sing_trig()
    logger.info('Executing trigger')
    daq.configure_channels()
    logger.info('Configuring channels')
    with session.initiate():
        logger.info('Initiating session')
        wf_info = []
        logger.info('Initiating fetching...')
        try:
            waveforms = session.channels[0,1].fetch()#num_samples=total_samples, relative_to=daq._acq_conf['relative_to'], offset=daq._acq_conf['offset'], record_number=daq._acq_conf['num_records'], timeout=daq._acq_conf['timeout'])
        except Exception:
            logger.error('Could not fetch!!')
            raise SystemError('BASTARDO!')
        for (k,wfm) in enumerate(waveforms):
            wf_info.append({'Waveform number'   : k,
                            'Samples'           : wfm.samples,
                            'Relative_initial_x': wfm.relative_initial_x,
                            'Absolute_initial_x': wfm.absolute_initial_x,
                            'x_increment'       : wfm.x_increment,
                            'Channel'           : wfm.channel,
                            'Record'            : wfm.record,
                            'Gain'              : wfm.gain,
                            'Offset'            : wfm.offset })
            logger.info(str(wf_info))
            daq.waveform = waveforms
'''




'''
try:
    waveforms, infos = daq.single_acquisition(sGen.pul_exe_sing_trig)
    logger.info('Retrieving data...')
except Exception:
    logger.error('Could not retrieve data!')
    raise SystemError ('Could not retrieve data!')
'''