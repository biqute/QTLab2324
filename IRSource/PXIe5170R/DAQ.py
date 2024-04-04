# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================

import niscope as ni
import hightime
import sys
sys.path.insert(1, r'F:\\LabIV\\QTLab2324\\IRSource\\logs\\sessions')
import logging
import numpy as np
import h5py

class DAQ(object):
    
    logger = logging.getLogger(__name__) #initialize logger
    
    _instance = None

    def __new__(self, device_name, device_address, id, rd, acq_conf, vertical, horizontal, chan_char, coefficients, trigger, dic):
        if self._instance is None:
            try:
                self._instance = super(DAQ, self).__new__(self)
                self._session = ni.Session(device_address, id_query=id, reset_device=rd, options=dic)
                self._devicename = device_name
                
                self.vertical_conf = vertical
                self.horizontal_conf = horizontal
                self.chan_char = chan_char
                self.coeff = coefficients
                
                self.acq_conf = acq_conf
                                
                self.waveform = []
                self.i_matrix_ch0, self.q_matrix_ch0, self.timestamp_ch0 = [], [], []
                self.i_matrix_ch1, self.q_matrix_ch1, self.timestamp_ch1 = [], [], []
                
                self.trigger = trigger
                
                print('Connected to', self._devicename)
                self.logger.debug("Connected to PXIe-5170R")
                
            except Exception as e:
                self.logger.critical("Could not connect to PXIe-5170R")
                raise RuntimeError("Could not connect to PXIe-5170R") from e
    
        return self._instance
    
# ==================================================================================================================================
#__SESSION DEFINITION +...__ 
#===================================================================================================================================
        
    def calibrate(self):            
            try:
                self._session.self_cal(option=ni.Option.SELF_CALIBRATE_ALL_CHANNELS)
                print('Running calibration routine...')
                self.logger.debug('Channels calibrated')
            except Exception as e:
                self.logger.warning('Calibration failed!')
                raise ValueError("Self calibration failed") from e
            
    def test(self):
            try:
                self._session.self_test()
                print('Running test routine...')
                self.logger.debug('Running test routine...')
            except Exception as e:
                self.logger.warning("Test failed")
                raise  ValueError("Test failed") from e      
            
    def reset(self):

        try: 
            print('Resetting session')
            self._session.reset()     
            self.logger.debug("Resetting session")
        except Exception as e:
            self.logger.warning("Session reset didn't work")
            raise ValueError("Session reset didn't work")
            
    def reset_device(self):

        try: 
            print("Resetting device")
            self._session.reset_device()     
            self.logger.debug("Resetting device")
        except Exception as e:
            self.logger.warning("Resetting device didn't work")
            raise ValueError("Resetting device didn't work")
        
    def reset_with_def(self):

        try: 
            print("Resetting with defaults")
            self._session.reset_with_defaults()    
            self.logger.debug("Resetting with defaults done")
        except Exception as e:
            self.logger.warning("Resetting with defaults didn't work")
            raise ValueError("Resetting with defaults didn't work")
        
    def get_status(self):
        print(str(self.session.acquisition_status()))
        self.logger.warning("Acquisition status: " + str(self.session.acquisition_status())) 
        return None
        
    def disable(self):

        try:
            print('Disabling')
            self._hanlde.disable()
            self.logger.debug("Disabling worked")
        except Exception as e:
            self.logger.critical("Disabling didn't work")
            raise ValueError("Disabling didn't work")
            
            
    def commit(self):
        try:
            print('Committing')
            self._session.commit()
            self.logger.debug("Committing worked")
        except Exception as e:
            self.logger.warning("Committing didn't work")
            raise ValueError("Committing didn't work")
        
    def close(self):
        try:
            print('Closing session')
            self._session.close()
            self.logger.debug('Closing session')
        except Exception as e:
            self.logger.error('Could not close current session')
            raise RuntimeError('Could not close current session')
            
        
    def initiate(self):

        try:
            print('Starting acquisition')
            self._session.initiate()
            self.logger.debug("Acquisition started correctly")
        except Exception as e:
            self.logger.critical("Acquisition didn't start correctly")
            raise ValueError("Acquisition didn't start correctly")
        
# ==================================================================================================================================
#__Channels configuration__
#===================================================================================================================================        

    def config_vertical(self):
        try:
            self.logger.debug("Configuring vertical done")
            self._session.configure_vertical(self.vertical_conf['range'], self.vertical_conf['coupling'], self.vertical_conf['offset'], self.vertical_conf['probe_attenuation'], self.vertical_conf['enabled'])
        except Exception as e:
            self.logger.error("Vertical config went wrong")
            raise ValueError("Vertical config went wrong")
            

    def config_chan_char(self):

        try:
            self.logger.debug("Channels characteristics configuration done")
            self._session.configure_chan_characteristics(self.chan_char['input_impedance'], self.chan_char['max_input_frequency'])
        except Exception as e:
            self.logger.error("Channels characteristics configuration went wrong")
            raise ValueError("Channels characteristics configuration went wrong")
        
        
    def config_eqfilt_coeff(self):

        try:
            self.logger.debug("Equalization filter configuration done")
            self._session.configure_equalization_filter_coefficients(self.coeff)
        except Exception as e:
            self.logger.error("Equalization filter configuration went wrong")
            raise ValueError("Equalization filter configuration went wrong")
        
    def config_hor_timing(self):

        try:
            self.logger.debug("Horizontal timing configuration done")
            self._session.configure_horizontal_timing(self.horizontal_conf['min_sample_rate'], self.horizontal_conf['min_num_pts'], self.horizontal_conf['ref_position'], self.horizontal_conf['num_records'], self.horizontal_conf['enforce_realtime'])
        except Exception as e:
            self.logger.error("Horizontal timing configuration went wrong")
            raise ValueError("Horizontal timing configuration went wrong")
                                    
#===================================================================================================================================
#__Waveform processing__
#===================================================================================================================================

    def add_wfm_proc(self, meas_function):

        try:
            self.logger.debug("Waveform processing added correctly")
            self._session.add_waveform_processing(meas_function)
        except Exception as e:
            self.logger.error("Adding Waveform processing went wrong")
            raise ValueError("Adding Waveform processing went wrong")
        
        
    def clear_wfm_stats(self,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):

        try:
            self.logger.debug("Waveform stats cleared correctly")
            self._session.clear_waveform_measurement_stats(clearable_measurement_function)
        except Exception as e:
            self.logger.error("Clearing waveform stats went wrong")
            raise ValueError("Clearing waveform stats went wrong")
        

    def clear_wfm_proc(self):
        
        try:
            self.logger.debug("Waveform proc cleared correctly")
            self._session.clear_waveform_processing()
        except Exception as e:
            self.logger.error("Clearing waveform proc went wrong")
            raise ValueError("Clearing waveform proc went wrong")
        
#===================================================================================================================================
#__Trigger config__ 
#===================================================================================================================================

    def config_imm_trigger(self):
        try:
            self.logger.debug("Immediate trigger configuration done correctly")
            self._session.configure_trigger_immediate()
        except Exception as e:
            self.logger.error("Immediate trigger configuration went wrong")
            raise ValueError("Immediate trigger configuration went wrong")


    def config_dig_trigger(self):

        try:
            self.logger.debug("Digital trigger configuration done correctly")
            self._session.configure_trigger_digital(self.trigger['trigger_source'], self.trigger['slope'], self.trigger['holdoff'], self.trigger['delay'])
        except Exception as e:
            self.logger.error("Digital trigger configuration went wrong")
            raise ValueError("Digital trigger configuration went wrong")


    def config_edge_trigger(self):
        
        try:
            self.logger.debug("Edge trigger configuration done correctly")
            self._session.configure_trigger_edge(self.trigger['trigger_source'], self.trigger['level'], self.trigger['trigger_coupling'], self.trigger['slope'], self.trigger['holdoff'], self.trigger['delay'])
        except Exception as e:
            self.logger.error("Edge trigger configuration went wrong")
            raise ValueError("Edge trigger configuration went wrong")


    def config_software_trigger(self):
       
        try:
            self.logger.debug("Software trigger configuration done correctly")
            self._session.configure_trigger_software(self.trigger['holdoff'], self.trigger['delay'])
        except Exception as e:
            self.logger.error("Software trigger configuration went wrong")
            raise ValueError("Software trigger configuration went wrong")

#===================================================================================================================================
#__Fetching+reading+storage__
#===================================================================================================================================

    def fetch(self):
        
        try:
            self.waveform.extend([self.channels[i].fetch(num_samples=self.acq_conf['length'], timeout=self.acq_conf['timeout'], relative_to=self.acq_conf['relative_to'], num_records=self.acq_conf['num_records']) for i in self.acq_conf['channels']])
            self.logger.debug('Time from the trigger event to the first point in the waveform record: ' + str(self._session.acquisition_start_time))
            self.logger.debug('Actual number of samples acquired in the record: ' + str(self._session.points_done))
            self.logger.debug('Number of records that have been completely acquired: ' + str(self._session.records_done))
            self.get_status()
        except Exception as e:
            self.logger.error("Fetching went wrong")
            raise MemoryError("Fetching went wrong")
        
    
    def fill_matrix(self, return_data=False):
        for i in range(self.records):
            self.i_matrix_ch0.append(np.array(self.waveform[0][i].samples))
            self.q_matrix_ch0.append(np.array(self.waveform[1][i].samples))
            self.timestamp_ch0.append(self.waveform[0][i].absolute_initial_x)
            try:
                self.i_matrix_ch1.append(np.array(self.waveform[2][i].samples))
                self.q_matrix_ch1.append(np.array(self.waveform[3][i].samples))
                self.timestamp_ch1.append(self.waveform[2][i].absolute_initial_x)
            except:
                pass
            
        self.logger.debug("Raw data I and Q were collected for trigger acquisition")

        if return_data:
            return self.i_matrix, self.q_matrix, self.timestamp
        else:
            return None

    
    def storage_hdf5(self, name):
        with h5py.File(name, 'w') as hdf:
            hdf.create_dataset('i_signal_ch0', data=self.i_matrix_ch0, compression='gzip', compression_opts=9)
            hdf.create_dataset('q_signal_ch0', data=self.q_matrix_ch0, compression='gzip', compression_opts=9)
            hdf.create_dataset('i_signal_ch1', data=self.i_matrix_ch1, compression='gzip', compression_opts=9)
            hdf.create_dataset('q_signal_ch1', data=self.q_matrix_ch1, compression='gzip', compression_opts=9)
            
            try:
                hdf.create_dataset('timestamp_ch0', data=self.timestamp_ch0, compression='gzip', compression_opts=9)
                hdf.create_dataset('timestamp_ch1', data=self.timestamp_ch1, compression='gzip', compression_opts=9)
            except:
                pass

        self.logger.debug("Raw data I and Q were stored in an HDF5 file: " + name)
        
#===================================================================================================================================
# CONTINUOUS ACQUISITION
#===================================================================================================================================

    def continuous_acq(self):
            
        current_pos = 0
        self.waveform = [np.ndarray(self.acq_conf['total_samples'], dtype=np.float64) for c in self.channels]

        self.get_status()

        while current_pos < self.acq_conf['total_samples']:
            for channel, wfm in zip(self.acq_conf['channels'], self.waveform):
                try:
                    self._session.channels[channel].fetch_into(wfm[current_pos:current_pos + self.acq_conf['samples_per_fetch']], relative_to=self.acq_conf['relative_to'], offset=self.acq_conf['offset'], record_number=self.acq_conf['record_number'], num_records=self.acq_conf['num_records'])
                    self.logger.debug("Fetching into...")
                except Exception as e:
                    self.logger.error("Fetching did not work")
                    raise ImportWarning("Fetching did not work")

            current_pos += self.acq_conf['samples_per_fetch']

        self.i_matrix_ch0 = np.array(self.waveform[0])
        self.q_matrix_ch0 = np.array(self.waveform[1])
        self.i_matrix_ch1 = np.array(self.waveform[2])
        self.q_matrix_ch1 = np.array(self.waveform[3])

        self.logger.debug('Raw data I and Q were collected for continuous acquisition')