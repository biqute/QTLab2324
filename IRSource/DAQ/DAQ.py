# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================

import niscope as ni
import numpy as np
import h5py
from datetime import datetime
from Session_handler import Session_handler
date = datetime.now().strftime("%m-%d-%Y")


class DAQ():
    _instance = None
    _device = None
    

    def __new__(cls, devicename):
        if cls._instance is None:
            try: 
                cls = super(DAQ, cls).__new__(cls)
                print('Instance correctly created!')
            except Exception:
                raise ValueError("Could not create object instance")
        return cls
    
    

    def __init__(self,devicename):
                
        if not self._device:
            self._device = devicename
            self.eq_coeff = None
            self.chan_conf = None
            self.vertical_conf = None
            self.horizontal_conf = None
            self.acq_conf = None
            self.waveform = []
            self.channels = []
            self.i_matrix_ch0, self.q_matrix_ch0, self.timestamp_ch0 = [], [], []
            self.i_matrix_ch1, self.q_matrix_ch1, self.timestamp_ch1 = [], [], []
            self.trigger_dic = None
            self.trigger_type = None
            
#===================================================================================================================================
#__Channels configuration__
#===================================================================================================================================            


    @property
    def vertical_conf(self):
        return self.vertical_conf
    
    @vertical_conf.setter
    def vertical_conf(self, vc):
        self.vertical_conf = vc
        
            
    @property
    def horizontal_conf(self):
        return self.horizontal_conf
    
    @horizontal_conf.setter
    def horizontal_conf(self,hc):
        self.horizontal_conf = hc
        self.sh.session.configure_horizontal_timing(self.horizontal_dic['min_sample_rate'], self.horizontal_dic['min_num_pts'], self.horizontal_dic['ref_position'], self.horizontal_dic['num_records'], self.horizontal_dic['enforce_realtime'])
            
    @property
    def chan_conf(self):
        return self.chan_conf
    
    @chan_conf.setter
    def chan_conf(self, cc):
        self.chan_conf =  cc
        self.sh.session.configure_chan_characteristics(self.chan_conf['input_impedance'], self.chan_conf['max_frequency'])
        
    @property
    def eq_conf(self):
        return self.eq_conf
    
    @eq_conf.setter
    def eq_coeff(self):
        self.sh.session.configure_equalization_filter_coefficients(self.coeff)

    def get_status(self):
        print(f'Current acquisition status : {self.session.acquisition_status()}')
        return self.sh.session.acquisition_status()      

        
#===================================================================================================================================
#__Trigger config__ 
#===================================================================================================================================

    @property
    def trigger_type(self):
        return self.trigger_type
    
    @trigger_type.setter
    def trigger_type(self):
        self.trigger_type = self.trigger_dic['trigger_type']
        
    @property
    def trigger_dic(self):
        return self.trigger_dic
    
    @trigger_dic.setter
    def trigger_dic(self, dic):
        self.trigger_dic = dic
    
    def config_trigger(self):
        if(self.trigger_type == "IMM"):
            self.sh.session.configure_trigger_immediate()
        elif (self.trigger_type == "DIG"):
            self.sh.session.configure_trigger_digital(self.trigger['trigger_source'], self.trigger['slope'], self.trigger['holdoff'], self.trigger['delay'])
        elif (self.trigger_type == "EDGE"):
            self.sh.session.configure_trigger_edge(self.trigger['trigger_source'], self.trigger['level'], self.trigger['trigger_coupling'], self.trigger['slope'], self.trigger['holdoff'], self.trigger['delay'])
        elif (self.trigger_type == 'SOF'):
            self.sh.session.configure_trigger_software(self.trigger['holdoff'], self.trigger['delay'])
    
#===================================================================================================================================
#__Fetching+reading+storage__
#===================================================================================================================================

    #def fetch(self):
        
    #    for channel in self.enabled():
    #        self.waveform.extend([channel.fetch(num_samples=self.acq_conf['length'], timeout=self.acq_conf['timeout'], relative_to=self.acq_conf['relative_to'], num_records=self.acq_conf['num_records']) for i in self.acq_conf['channels']])
    #        print('Time from the trigger event to the first point in the waveform record: ' + str(self._session.acquisition_start_time))
    #        print('Actual number of samples acquired in the record: ' + str(self._session.points_done))
    #        print('Number of records that have been completely acquired: ' + str(self._session.records_done))

    def fetch(self, timeout=10):
        self._session.initiate()
        self.waveform.extend([self.channels[i].fetch(num_samples=self.acq_conf['lenght'], timeout=timeout, relative_to=self.acq_conf['relative_to'], num_records=self.acq_conf['num_records']) for i in self.channels])
        
    
    def fill_matrix(self, return_data=False):
        for i in range(self.acq_conf['num_records']):
            self.i_matrix_ch0.append(np.array(self.waveform[0][i].samples))
            self.q_matrix_ch0.append(np.array(self.waveform[1][i].samples))
            self.timestamp_ch0.append(self.waveform[0][i].absolute_initial_x)
            try:
                self.i_matrix_ch1.append(np.array(self.waveform[2][i].samples))
                self.q_matrix_ch1.append(np.array(self.waveform[3][i].samples))
                self.timestamp_ch1.append(self.waveform[2][i].absolute_initial_x)
            except:
                pass
            
        #self.logger.debug("Raw data I and Q were collected for trigger acquisition")

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

        #self.logger.debug("Raw data I and Q were stored in an HDF5 file: " + name)
        
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
                    #self.logger.debug("Fetching into...")
                except Exception as e:
                    #self.logger.error("Fetching did not work")
                    raise ImportWarning("Fetching did not work")

            current_pos += self.acq_conf['samples_per_fetch']

        self.i_matrix_ch0 = np.array(self.waveform[0])
        self.q_matrix_ch0 = np.array(self.waveform[1])
        self.i_matrix_ch1 = np.array(self.waveform[2])
        self.q_matrix_ch1 = np.array(self.waveform[3])

        #self.logger.debug('Raw data I and Q were collected for continuous acquisition')