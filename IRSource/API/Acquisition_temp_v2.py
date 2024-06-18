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
from  Exceptions import replace_non_serializable
from PAmodules.QuickSyn import FSL_0010
from PAmodules.network.RS_Signal_Generator import RS_SMA100B
from niscope.errors import DriverError
import numpy as np
import niscope as ni
import matplotlib.pyplot as plt

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
    daq = DAQ(devicename)
    logger.info('DAQ class object correctly created')
except Exception:
    logger.critical('Could not crate DAQ class object')
    raise SyntaxError('Could not create DAQ class object')

try:
    fsl = FSL_0010.FSL10_synthesizer(device_address='COM37')
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
    k = 2                                                               # coefficiente per prendere k*1000 punti                                                                     
    pulse_freq      = 1.010e9
    amplitude       = -18                                               # Set the amplitude of the signal in dBm
    sample_rate     = 250e6                                             # Maximum Value: 250.0e6
    pulse_width     = k * 3e-6                                          # min 5ns                             
    pulse_delay     = 0
    pulse_period    = k * 5e-6                                          # min 20ns
    sGen.reset()
    sGen.clear()
    sGen.pul_gen_params(delay = pulse_delay, width = pulse_width, period = pulse_period)   # da capire quale pulse width
    sGen.pul_gen_mode('SING')
    sGen.pul_trig_mode('SING')
    sGen.RF_freq(pulse_freq)
    sGen.RF_lvl_ampl(amplitude)
    logger.info('SMA set up correctly')
except:
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
    raise SystemError('Could not restet DAQ with defaults')

try:
    daq.horizontal_conf(ACQUISITION_CONFIG['horizontal'])
    logger.info('Inserting hconf dic')
except Exception:
    logger.warning('Could not insert hconf dic')
    raise SystemError('Could not insert hconf dic')

try:
    daq.vertical_conf(ACQUISITION_CONFIG['vertical'])
    logger.info('Inserting hconf dic')
except Exception:
    logger.warning('Could not insert vconf dic')
    raise SystemError('Could not insert vconf dic')

try:
    daq.chan_conf(ACQUISITION_CONFIG['chan_conf'])
    logger.info('Inserting chan char dic')
except Exception:
    logger.warning('Could not insert chan char dic')
    raise SystemError('Could not insert chan char dic')

try:
    daq.set_trigger_dic(ACQUISITION_CONFIG['trigger_dig'])
    logger.info('Inserting trigger dic')
except Exception:
    logger.warning('Could not insert trigger dic')
    raise SystemError('Could not insert trigger dic')

#===============================================================================================
#Apply DAQ configuration dictionaries
#===============================================================================================

try:
    daq.config_hor_timing()
    logger.info('Implementing horizontal configuration')
except Exception:
    logger.warning('Could not implement horizontal configuration')
    raise SystemError('Could not implement horizontal configuration')

try:
    daq.enable_channels()
    logger.info('Enabling all channels')
except Exception:
    logger.warning('Could not enable channels!')
    raise SystemError('Could not enable channels!')

try:
    daq.config_vertical()
    logger.info('Implementing vertical configuration')
except Exception:
    logger.warning('Could not implement vertical configuration')
    raise SystemError('Could not implement vertical configuration')

try:
    daq.config_chan_char()
    logger.info('Implementing channels configuration')
except Exception:
    raise SystemError('Could not implement channels configuration')

try:
    daq.config_chan_char()
    logger.info('Implementing channels configuration')
except Exception:
    raise SystemError('Could not implement channels configuration')

try:
    daq.config_edge_trigger()
    logger.info('implementing edge trigger')
except Exception:
    logger.warning('Could not implement edge trigger')
    raise SystemError('Could not implement edge trigger')

    
#===============================================================================================
#Test DAQ configuration
#===============================================================================================


try:
    daq.test()
    logger.info('Testing DAQ actual configuration')
except Exception:
    logger.critical('DAQ test gone wrong!')

#===============================================================================================
#GET DATA!
#===============================================================================================
fsl.set_frequency(1) # GHz
fsl.set_output('ON')

amplitudes  = np.arange(amplitude, amplitude + 3 , 1) #emitted powers from synths [-18 -17 -16]
frequencies = np.arange(pulse_freq, pulse_freq + 0.003e9, 0.001e9)

amp_freq = {}
counter  = 1
digits_a = "{:0"+str(len(str(len(amplitudes))))+"d}" #number of digits for amplitudes
digits_f = "{:0"+str(len(str(len(frequencies))))+"d}"#number of digits for frequencies


for a, amp in enumerate(amplitudes):
    amp_freq[f'p{digits_a.format(a)}'] = {'power_(dBm)': amp, 'freqs': {}}
    sGen.RF_lvl_ampl(amp)
    logger.info('Setting sGen amplitude'+digits_a.format(amp))

    for f, fre in enumerate(frequencies):
        
        sGen.RF_freq(fre) 
        sGen.pul_state(1)
        sGen.RF_state(1)
        flag = 0
        waveforms = []

        #with self._session.initiate():
        #    trig()
        #    # print(self._session.acquisition_status())
        #    try:
        #        return self._session.channels[0,1,2,3].fetch()#relative_to = ni.FetchRelativeTo.TRIGGER)
        #    except DriverError:
        #        print('DriverError in ni.session.channels.fetch()')
        #        sys.exit(0)
            

        with daq._session.initiate():
            while(True):
                try:
                    sGen.pul_exe_sing_trig #If "Trigger Mode = Single", initiates a single pulse sequence manually.
                    waveforms = daq.channels[0,1,2,3].fetch()
                except DriverError:
                    flag += 1
                    print(flag)
                if (flag>10 and ni.Session.acquisition_status!='IN_PROGRESS'):
                    break
            
        I = np.array(waveforms[0].samples.tolist())
        Q = np.array(waveforms[1].samples.tolist())
        if a == 1 and f == 1:
          plt.clf()
          #plt.plot(np.sqrt(I**2 + Q**2))
          plt.plot(np.arctan(Q/I))
          plt.show()
        
        sGen.pul_state(0)
        sGen.RF_state(0)

        print(counter*100/(len(amplitudes)*len(frequencies)),'%')
        counter += 1
        amp_freq[f'p{digits_a.format(a)}']['freqs'][f'f{digits_f.format(f)}'] = {'freq_(Hz)': fre, 'I': I, 'Q': Q}
fsl.set_output('OFF')

'''
# SAVE DATA ON HDF5 FILE
filename = 'IQMixer'+str(date)+'.hdf5'
if os.path.exists(filename):
  os.remove(filename)
hdf5_write(amplidick, filename)



 
#===============================================================================================
#Initiate Acquisition
#===============================================================================================

if (args[1]=='SINGLE'):
    
    with daq.initiate():
        waveforms = daq._instance._session.channels[0,1,2,3].fetch()
    for wfm in waveforms:
        print('Channel {0}, record {1} samples acquired: {2:,}\n'.format(wfm.channel, wfm.record, len(wfm.samples)))
    a = wfm[0].samples.tolist()
    plt.figure()
    plt.plot(np.arange(len(a))/250e6, a)
    plt.savefig('test'+datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))

'''
'''
    daq._instance.logger.info('END EXECUTION\n\n')
    
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
'''       