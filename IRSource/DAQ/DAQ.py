# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================

import niscope as ni
import numpy as np
import h5py
from datetime import datetime
date = datetime.now().strftime("%m-%d-%Y")


class DAQ(object):
    _instance = None
    _session = None
    _device = None
    

    def __new__(cls, devicename):
        if cls._instance is None:
            try: 
                cls._instance = super(DAQ, cls).__new__(cls)
                print('Instance correctly created!')
            except Exception as e:
                raise ValueError("Could not create object instance")
        return cls._instance

    def __init__(self,devicename):
        
        if not self._device:
            self._device = devicename
            self._session = ni.Session(devicename)
            self.coeff = None
            self.chanchar = None
            self.vertical_dic = None
            self.horizontal_dic = None
            self.acq_conf = None
            self.waveform = []
            self.channels = []
            self.i_matrix_ch0, self.q_matrix_ch0, self.timestamp_ch0 = [], [], []
            self.i_matrix_ch1, self.q_matrix_ch1, self.timestamp_ch1 = [], [], []
            self.trigger = None
            self.triggertype = None

    def vertical_conf(cls, vertical):
        cls._instance.vertical_dic = vertical
        return cls._instance  # Return the instance of the class, not None

    def chan_conf(cls, char):
        cls._instance.chanchar = char
        return cls._instance  # Return the instance of the class, not None

    def horizontal_conf(cls, horizontal):
        cls._instance.horizontal_dic = horizontal
        return cls._instance  # Return the instance of the class, not None

    def eq_conf(cls, eq_coeff):
        cls._instance.vertical_dic = eq_coeff
        return cls._instance  # Return the instance of the class, not None
 
# ==================================================================================================================================
#__SESSION DEFINITION +...__ 
#===================================================================================================================================
    
    def calibrate(cls):            
        cls._instance._session.self_cal(option=ni.Option.SELF_CALIBRATE_ALL_CHANNELS)
    
    def test(cls):
        cls._instance._session.self_test()

    def session_reset(cls):
        cls._session.reset()     

    def device_reset(cls):
        cls._session.reset_device()     
        
    def reset_with_def(cls):
        cls._session.reset_with_defaults()    
    
    @property    
    def get_status(cls):
        print(str(cls._instance._session.acquisition_status()))
        return cls._instance._session.acquisition_status()

    def available(cls):
        if(cls.get_status()=="AcquisitionStatus.COMPLETE"):
              return True
        else: return False
    
    def disable(cls):
        cls._instance.disable()

    def commit(cls):
        cls._instance._session.commit()
        
    @property
    def get_session(cls):
        return  cls._instance._session

    def close(cls):
        cls._instance._session.close()
            
    def initiate(cls):
        cls._instance._session.initiate()

    @property
    def get_enabled(cls):
        return cls._session.enabled_channels

    def enable_channels(cls):
        for i in range(cls._instance._session.channel_count):
            cls._instance._session.channels[i].channel_enabled = True

# ==================================================================================================================================
#__Channels configuration__
#===================================================================================================================================        

    def config_vertical(cls):
        for c in cls._session.enabled_channels:
            if(c!=','):
                cls._session.channels[c].configure_vertical(cls._instance.vertical_dic['range'], cls._instance.vertical_dic['coupling'], cls._instance.vertical_dic['offset'], cls._instance.vertical_dic['probe_attenuation'], cls._instance.vertical_dic['enabled'])        
            else:
                pass
            
    def config_chan_char(cls):
        cls._instance._session.configure_chan_characteristics(cls._instance.chanchar['input_impedance'], cls._instance.chanchar['max_frequency'])
        
    def config_eqfilt_coeff(cls):
        cls._instance._session.configure_equalization_filter_coefficients(cls._instance.coeff)
        
    def config_hor_timing(cls):
        cls._instance._session.configure_horizontal_timing(cls._instance.horizontal_dic['min_sample_rate'], cls._instance.horizontal_dic['min_num_pts'], cls._instance.horizontal_dic['ref_position'], cls._instance.horizontal_dic['num_records'], cls._instance.horizontal_dic['enforce_realtime'])
        
                
#===================================================================================================================================
#__Waveform processing__
#===================================================================================================================================
    
    def add_wfm_proc(cls, meas_function):
        cls._instance._session.add_waveform_processing(meas_function)
        
    def clear_wfm_stats(cls,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):
        cls._instance._session.clear_waveform_measurement_stats(clearable_measurement_function)
    
    def clear_wfm_proc(cls):
        cls._instance._session.clear_waveform_processing()
        
#===================================================================================================================================
#__Trigger config__ 
#===================================================================================================================================

    
    def set_trigger_dic(cls, trigger):
        cls._instance.trigger = trigger
        return cls._instance  

    @property
    def get_trigger_type(cls):
        print(cls._instance.trigger['trigger_type'])

    
    def config_imm_trigger(cls):
        if(cls._instance.trigger['trigger_type'] == "IMM"):
            cls._instance._session.configure_trigger_immediate()
    
    def config_dig_trigger(cls):
        if(cls._instance.trigger['trigger_type'] == "DIG"):
            cls._instance._session.configure_trigger_digital(cls._instance.trigger['trigger_source'], cls._instance.trigger['slope'], cls._instance.trigger['holdoff'], cls._instance.trigger['delay'])
    
    def config_edge_trigger(cls):
        if(cls._instance.trigger['trigger_type'] == "EDGE"):
            cls._instance._session.configure_trigger_edge(cls._instance.trigger['trigger_source'], cls._instance.trigger['level'], cls._instance.trigger['trigger_coupling'], cls._instance.trigger['slope'], cls._instance.trigger['holdoff'], cls._instance.trigger['delay'])
    
    def config_software_trigger(cls):
        if(cls._instance.trigger['trigger_type'] == "SOF"): 
            cls._instance._session.configure_trigger_software(cls._instance.trigger['holdoff'], cls._instance.trigger['delay'])
        
    def enabled(cls):
        en = []
        for i in range(cls._instance._session.channel_count):
                if(cls._instance._session.channels[i].channel_enabled):
                    en.append(cls._instance._session.channels[i])
#===================================================================================================================================
#__Fetching+reading+storage__
#===================================================================================================================================

    def fetch(cls):
        
        for channel in cls.enabled():
            cls._instance.waveform.extend([channel.fetch(num_samples=cls._instance.acq_conf['length'], timeout=cls._instance.acq_conf['timeout'], relative_to=cls._instance.acq_conf['relative_to'], num_records=cls._instance.acq_conf['num_records']) for i in cls._instance.acq_conf['channels']])
            print('Time from the trigger event to the first point in the waveform record: ' + str(cls._instance._session.acquisition_start_time))
            print('Actual number of samples acquired in the record: ' + str(cls._instance._session.points_done))
            print('Number of records that have been completely acquired: ' + str(cls._instance._session.records_done))
            cls._instance.get_status()
        
    
    def fill_matrix(cls, return_data=False):
        for i in range(cls._instance.records):
            cls._instance.i_matrix_ch0.append(np.array(cls._instance.waveform[0][i].samples))
            cls._instance.q_matrix_ch0.append(np.array(cls._instance.waveform[1][i].samples))
            cls._instance.timestamp_ch0.append(cls._instance.waveform[0][i].absolute_initial_x)
            try:
                cls._instance.i_matrix_ch1.append(np.array(cls._instance.waveform[2][i].samples))
                cls._instance.q_matrix_ch1.append(np.array(cls._instance.waveform[3][i].samples))
                cls._instance.timestamp_ch1.append(cls._instance.waveform[2][i].absolute_initial_x)
            except:
                pass
            
        #cls._instance.logger.debug("Raw data I and Q were collected for trigger acquisition")

        if return_data:
            return cls._instance.i_matrix, cls._instance.q_matrix, cls._instance.timestamp
        else:
            return None

    
    def storage_hdf5(cls, name):
        with h5py.File(name, 'w') as hdf:
            hdf.create_dataset('i_signal_ch0', data=cls._instance.i_matrix_ch0, compression='gzip', compression_opts=9)
            hdf.create_dataset('q_signal_ch0', data=cls._instance.q_matrix_ch0, compression='gzip', compression_opts=9)
            hdf.create_dataset('i_signal_ch1', data=cls._instance.i_matrix_ch1, compression='gzip', compression_opts=9)
            hdf.create_dataset('q_signal_ch1', data=cls._instance.q_matrix_ch1, compression='gzip', compression_opts=9)
            
            try:
                hdf.create_dataset('timestamp_ch0', data=cls._instance.timestamp_ch0, compression='gzip', compression_opts=9)
                hdf.create_dataset('timestamp_ch1', data=cls._instance.timestamp_ch1, compression='gzip', compression_opts=9)
            except:
                pass

        #cls._instance.logger.debug("Raw data I and Q were stored in an HDF5 file: " + name)
        
#===================================================================================================================================
# CONTINUOUS ACQUISITION
#===================================================================================================================================

    def continuous_acq(cls):
            
        current_pos = 0
        cls._instance.waveform = [np.ndarray(cls._instance.acq_conf['total_samples'], dtype=np.float64) for c in cls._instance.channels]

        cls._instance.get_status()

        while current_pos < cls._instance.acq_conf['total_samples']:
            for channel, wfm in zip(cls._instance.acq_conf['channels'], cls._instance.waveform):
                try:
                    cls._instance._session.channels[channel].fetch_into(wfm[current_pos:current_pos + cls._instance.acq_conf['samples_per_fetch']], relative_to=cls._instance.acq_conf['relative_to'], offset=cls._instance.acq_conf['offset'], record_number=cls._instance.acq_conf['record_number'], num_records=cls._instance.acq_conf['num_records'])
                    #cls._instance.logger.debug("Fetching into...")
                except Exception as e:
                    #cls._instance.logger.error("Fetching did not work")
                    raise ImportWarning("Fetching did not work")

            current_pos += cls._instance.acq_conf['samples_per_fetch']

        cls._instance.i_matrix_ch0 = np.array(cls._instance.waveform[0])
        cls._instance.q_matrix_ch0 = np.array(cls._instance.waveform[1])
        cls._instance.i_matrix_ch1 = np.array(cls._instance.waveform[2])
        cls._instance.q_matrix_ch1 = np.array(cls._instance.waveform[3])

        #cls._instance.logger.debug('Raw data I and Q were collected for continuous acquisition')