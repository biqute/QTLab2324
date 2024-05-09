# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================

import niscope as ni
import hightime
import sys
sys.path.insert(1, r'C:\\Users\\oper\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRSource\\logs\\sessions\\')
import logging
import numpy as np
import h5py
from logging.config import dictConfig
from logs.DAQ_config import LOGGING_CONFIG

# LOG SYSTEM

class DAQ(object):
    _instance = None

    def __new__(cls, device_name):
        if cls._instance is None:
            cls._instance = super(DAQ, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, device_name):
        if not self._initialized:
            self._initialized = True
            try: 
                self._devicename = device_name
                self.logger = logging.getLogger(__name__)  # Initialize logger
                dictConfig(LOGGING_CONFIG)
                self.logger.info('START EXECUTION')
            except:
                print("Not working!")
            name = "test.log"
            path = 'C:\\Users\\oper\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRSource\\logs\\sessions\\'
            self._session = ni.Session(self._devicename)
            self.coeff = None
            self.chanchar = None
            self.vertical_dic = None
            self.horizontal_dic = None
            self.acq_conf = None
            self.waveform = []
            self.i_matrix_ch0, self.q_matrix_ch0, self.timestamp_ch0 = [], [], []
            self.i_matrix_ch1, self.q_matrix_ch1, self.timestamp_ch1 = [], [], []
            self.trigger = None
            self.triggertype = None

            print('Connected to', self._devicename)
            self.logger.debug("Connected to PXIe-5170R")


    @classmethod
    def vertical_conf(cls, vertical):
        try:
            cls._instance.vertical_dic = vertical
            cls._instance.logger.info("Vertical config property added")
            print("Vertical config property added")
        except Exception as e:
            cls._instance.logger.info("Vertical config property NOT added")
            print("Vertical config property NOT added")

        return cls._instance  # Return the instance of the class, not None

    @classmethod
    def chan_conf(cls, char):
        try:
            cls._instance.chanchar = char
            cls._instance.logger.info("channels char config property added")
            print("Vertical config property added")
        except Exception as e:
            cls._instance.logger.info("Channels char config property NOT added")
            print("Channels char config property NOT added")

        return cls._instance  # Return the instance of the class, not None

    @classmethod
    def horizontal_conf(cls, horizontal):
        try:
            cls._instance.horizontal_dic = horizontal
            cls._instance.logger.info("Horizontal config property added")
            print("Horizontal config property added")
        except Exception as e:
            cls._instance.logger.info("Horizontal config property NOT added")
            print("Horizontal config property NOT added")

        return cls._instance  # Return the instance of the class, not None

    @classmethod
    def eq_conf(cls, eq_coeff):
        try:
            cls._instance.vertical_dic = eq_coeff
            cls._instance.logger.info("Equalization filters coefficients added")
            print("Equalization filters coefficients added")
        except Exception as e:
            cls._instance.logger.info("Equalization filters coefficients NOT added")
            print("Equalization filters coefficients NOTadded")

        return cls._instance  # Return the instance of the class, not None
 
# ==================================================================================================================================
#__SESSION DEFINITION +...__ 
#===================================================================================================================================
    @classmethod    
    def calibrate(cls):            
        try:
            cls._instance._session.self_cal(option=ni.Option.SELF_CALIBRATE_ALL_CHANNELS)
            print('Running calibration routine...')
            cls._instance.logger.debug('Channels calibrated')
        except Exception as e:
            cls._instance.logger.warning('Calibration failed!')
            raise ValueError("Self calibration failed")
    
    @classmethod            
    def test(cls):
            try:
                cls._instance._session.self_test()
                print('Running test routine...')
                cls._instance.logger.debug('Running test routine...')
            except Exception as e:
                cls._instance.logger.warning("Test failed")
                raise  ValueError("Test failed") from e      

    @classmethod
    def session_reset(cls):
        try: 
            print('Resetting session')
            cls._instance._session.reset()     
            cls._instance.logger.debug("Resetting session")
        except Exception as e:
            cls._instance.logger.warning("Session reset didn't work")
            raise ValueError("Session reset didn't work")

    @classmethod
    def device_reset(cls):

        try: 
            print("Resetting device")
            cls._instance._session.reset_device()     
            cls._instance.logger.debug("Resetting device")
        except Exception as e:
            cls._instance.logger.warning("Resetting device didn't work")
            raise ValueError("Resetting device didn't work")
        
    @classmethod
    def reset_with_def(cls):

        try: 
            print("Resetting with defaults")
            cls._instance._session.reset_with_defaults()    
            cls._instance.logger.debug("Resetting with defaults done")
        except Exception as e:
            cls._instance.logger.warning("Resetting with defaults didn't work")
            raise ValueError("Resetting with defaults didn't work")
        
    @classmethod
    def get_status(cls):
        print(str(cls._instance._session.acquisition_status()))
        cls._instance.logger.warning("Acquisition status: " + str(cls._instance._session.acquisition_status())) 
        return None


    @property
    def available(cls):
        try:
            cls.get_status()=="AcquisitionStatus.COMPLETE"
            print("Ready to listen!")
            cls._instance.logger.info("Ready to listen!")
        except Exception as e:
            print("NOT ready to listen!")
            raise BufferError("NOT ready to listen!")

    '''
    @classmethod
    def disable(cls):
        try:
            print('Disabling')
            cls._instance.disable()
            cls._instance.logger.debug("Disabling worked")
        except Exception as e:
            cls._instance.logger.critical("Disabling didn't work")
            raise ValueError("Disabling didn't work")
    '''         
    @classmethod        
    def commit(cls):
        try:
            print('Committing')
            cls._instance._session.commit()
            cls._instance.logger.debug("Committing worked")
        except Exception as e:
            cls._instance.logger.warning("Committing didn't work")
            raise ValueError("Committing didn't work")
    
    @classmethod    
    def close(cls):
        try:
            print('Closing session')
            cls._instance._session.close()
            cls._instance.logger.debug('Closing session')
            cls._session = None
        except Exception as e:
            cls._instance.logger.error('Could not close current session')
            raise RuntimeError('Could not close current session')
            
    @classmethod    
    def initiate(cls):

        try:
            print('Starting acquisition')
            cls._instance._session.initiate()
            cls._instance.logger.debug("Acquisition started correctly")
        except Exception as e:
            cls._instance.logger.critical("Acquisition didn't start correctly")
            raise ValueError("Acquisition didn't start correctly")
        
# ==================================================================================================================================
#__Channels configuration__
#===================================================================================================================================        

    @classmethod
    def config_vertical(cls):
        try:
            cls._instance.logger.debug("Configuring vertical done")
            print("Configuring vertical done")
            cls._instance._session.configure_vertical(cls._instance.vertical_dic['range'], cls._instance.vertical_dic['coupling'], cls._instance.vertical_dic['offset'], cls._instance.vertical_dic['probe_attenuation'], cls._instance.vertical_dic['enabled'])
        except Exception as e:
            print("Vertical config went wrong")
            cls._instance.logger.error("Vertical config went wrong")
            raise ValueError("Vertical config went wrong")
            
    @classmethod
    def config_chan_char(cls):

        try:
            cls._instance._session.configure_chan_characteristics(cls._instance.chanchar['input_impedance'], cls._instance.chanchar['max_input_frequency'])
            print("Channels characteristics configuration done")
            cls._instance.logger.debug("Channels characteristics configuration done")
        except Exception as e:
            print("Channels characteristics configuration went wrong")
            cls._instance.logger.error("Channels characteristics configuration went wrong")
            raise ValueError("Channels characteristics configuration went wrong")
        
    @classmethod    
    def config_eqfilt_coeff(cls):

        try:
            cls._instance._session.configure_equalization_filter_coefficients(cls._instance.coeff)
            cls._instance.logger.debug("Equalization filter configuration done")
            print("Equalization filter configuration done")
        except Exception as e:
            print("Equalization filter configuration went wrong")
            cls._instance.logger.error("Equalization filter configuration went wrong")
            raise ValueError("Equalization filter configuration went wrong")

    @classmethod    
    def config_hor_timing(cls):

        try:
            cls._instance._session.configure_horizontal_timing(cls._instance.horizontal_dic['min_sample_rate'], cls._instance.horizontal_dic['min_num_pts'], cls._instance.horizontal_dic['ref_position'], cls._instance.horizontal_dic['num_records'], cls._instance.horizontal_dic['enforce_realtime'])
            cls._instance.logger.debug("Horizontal timing configuration done")
            print("Horizontal timing configuration done")
        except Exception as e:
            print("Horizontal timing configuration went wrong")
            cls._instance.logger.error("Horizontal timing configuration went wrong")
            raise ValueError("Horizontal timing configuration went wrong")
                                    
#===================================================================================================================================
#__Waveform processing__
#===================================================================================================================================
    @classmethod
    def add_wfm_proc(cls, meas_function):

        try:
            cls._instance._session.add_waveform_processing(meas_function)
            cls._instance.logger.debug("Waveform processing added correctly")
            print("Waveform processing added correctly")
        except Exception as e:
            print("Adding Waveform processing went wrong")
            cls._instance.logger.error("Adding Waveform processing went wrong")
            raise ValueError("Adding Waveform processing went wrong")
        
    @classmethod    
    def clear_wfm_stats(cls,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):

        try:
            cls._instance._session.clear_waveform_measurement_stats(clearable_measurement_function)
            cls._instance.logger.debug("Waveform stats cleared correctly")
            print("Waveform stats cleared correctly")
        except Exception as e:
            cls._instance.logger.error("Clearing waveform stats went wrong")
            print("Clearing waveform stats went wrong")
            raise ValueError("Clearing waveform stats went wrong")
        
    @classmethod
    def clear_wfm_proc(cls):
        
        try:
            cls._instance._session.clear_waveform_processing()
            cls._instance.logger.debug("Waveform proc cleared correctly")
            print("Waveform proc cleared correctly")
        except Exception as e:
            print("Clearing waveform proc went wrong")
            cls._instance.logger.error("Clearing waveform proc went wrong")
            raise ValueError("Clearing waveform proc went wrong")
        
#===================================================================================================================================
#__Trigger config__ 
#===================================================================================================================================

    @classmethod
    def set_trigger_dic(cls, trigger):
        try:
            cls._instance.trigger = trigger
            cls._instance.logger.info("Trigger dictionary added")
            print("Trigger dictionary added")
        except Exception as e:
            cls._instance.logger.info("Trigger dictionary NOT added")
            print("Trigger dictionary NOT added")

        return cls._instance  # Return the instance of the class, not Noneùù

    @property
    def get_trigger_type(cls):
        print(cls._instance.trigger['trigger_type'])

    @classmethod
    def config_imm_trigger(cls):
        try:
            cls._instance.trigger['trigger_type'] == "IMM"
        except Exception as e:
            raise TypeError("Trigger type is not IMM") from e
        try:
            cls._instance._session.configure_trigger_immediate()
            cls._instance.logger.debug("Immediate trigger configuration done correctly")
            print("Immediate trigger configuration done correctly")
        except Exception as e:
            print("Immediate trigger configuration went wrong")
            cls._instance.logger.error("Immediate trigger configuration went wrong")
            raise ValueError("Immediate trigger configuration went wrong")

    @classmethod
    def config_dig_trigger(cls):
        try:
            cls._instance.trigger['trigger_type'] == "DIG"
        except Exception as e:
            raise TypeError("Trigger type is not DIG") from e
        try:
            cls._instance._session.configure_trigger_digital(cls._instance.trigger['trigger_source'], cls._instance.trigger['slope'], cls._instance.trigger['holdoff'], cls._instance.trigger['delay'])
            cls._instance.logger.debug("Digital trigger configuration done correctly")
            print("Digital trigger configuration done correctly")
        except Exception as e:
            print("Digital trigger configuration went wrong")
            cls._instance.logger.error("Digital trigger configuration went wrong")
            raise ValueError("Digital trigger configuration went wrong")

    @classmethod
    def config_edge_trigger(cls):

        try:
            cls._instance.trigger['trigger_type'] == "EDGE"
        except Exception as e:
            raise TypeError("Trigger type is not EDGE") from e
        
        try:
            cls._instance._session.configure_trigger_edge(cls._instance.trigger['trigger_source'], cls._instance.trigger['level'], cls._instance.trigger['trigger_coupling'], cls._instance.trigger['slope'], cls._instance.trigger['holdoff'], cls._instance.trigger['delay'])
            cls._instance.logger.debug("Edge trigger configuration done correctly")
            print("Edge trigger configuration done correctly")
        except Exception as e:
            print("Edge trigger configuration went wrong")
            cls._instance.logger.error("Edge trigger configuration went wrong")
            raise ValueError("Edge trigger configuration went wrong")

    @classmethod
    def config_software_trigger(cls):

        try:
            cls._instance.trigger['trigger_type'] == "SOF"
        except Exception as e:
            raise TypeError("Trigger type is not SOF") from e
       
        try:
            cls._instance._session.configure_trigger_software(cls._instance.trigger['holdoff'], cls._instance.trigger['delay'])
            cls._instance.logger.debug("Software trigger configuration done correctly")
            print("Software trigger configuration done correctly")
        except Exception as e:
            print("Software trigger configuration went wrong")
            cls._instance.logger.error("Software trigger configuration went wrong")
            raise ValueError("Software trigger configuration went wrong")

#===================================================================================================================================
#__Fetching+reading+storage__
#===================================================================================================================================

    def fetch(cls):
        
        try:
            cls._instance.waveform.extend([cls._instance.channels[i].fetch(num_samples=cls._instance.acq_conf['length'], timeout=cls._instance.acq_conf['timeout'], relative_to=cls._instance.acq_conf['relative_to'], num_records=cls._instance.acq_conf['num_records']) for i in cls._instance.acq_conf['channels']])
            cls._instance.logger.debug('Time from the trigger event to the first point in the waveform record: ' + str(cls._instance._session.acquisition_start_time))
            cls._instance.logger.debug('Actual number of samples acquired in the record: ' + str(cls._instance._session.points_done))
            cls._instance.logger.debug('Number of records that have been completely acquired: ' + str(cls._instance._session.records_done))
            print('Time from the trigger event to the first point in the waveform record: ' + str(cls._instance._session.acquisition_start_time))
            print('Actual number of samples acquired in the record: ' + str(cls._instance._session.points_done))
            print('Number of records that have been completely acquired: ' + str(cls._instance._session.records_done))
            cls._instance.get_status()
        except Exception as e:
            cls._instance.logger.error("Fetching went wrong")
            print("Fetching went wrong")
            raise MemoryError("Fetching went wrong")
        
    
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
            
        cls._instance.logger.debug("Raw data I and Q were collected for trigger acquisition")

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

        cls._instance.logger.debug("Raw data I and Q were stored in an HDF5 file: " + name)
        
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
                    cls._instance.logger.debug("Fetching into...")
                except Exception as e:
                    cls._instance.logger.error("Fetching did not work")
                    raise ImportWarning("Fetching did not work")

            current_pos += cls._instance.acq_conf['samples_per_fetch']

        cls._instance.i_matrix_ch0 = np.array(cls._instance.waveform[0])
        cls._instance.q_matrix_ch0 = np.array(cls._instance.waveform[1])
        cls._instance.i_matrix_ch1 = np.array(cls._instance.waveform[2])
        cls._instance.q_matrix_ch1 = np.array(cls._instance.waveform[3])

        cls._instance.logger.debug('Raw data I and Q were collected for continuous acquisition')