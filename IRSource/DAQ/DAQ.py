# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================

from datetime import datetime
import niscope as ni
import numpy as np
import h5py

date = datetime.now().strftime("%m-%d-%Y")

class DAQ():

    _instance = None
    
    def __init__(self):
        self._session = None
        self._status = None
        self._channels = []
        self._waveform = []
        self._acq_conf = {}
        self.i_matrix_ch0, self.q_matrix_ch0, self.timestamp_ch0 = [], [], []
        self.i_matrix_ch1, self.q_matrix_ch1, self.timestamp_ch1 = [], [], []
        self._devicename   = None
        self._acq_conf     = None
        self._eq_conf      = None
        self._trigger_dic  = None
        self._trigger_type = None

    def __new__(cls):
        if cls._instance is None:
            try:
                print(f"Calling {cls.__new__} method")
                cls = super(DAQ,cls).__new__(cls)
            except Exception:
                raise TimeoutError('Could not create new class instance')
#===================================================================================================================================
#__Card__ configuration__ 
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
        self._session.configure_horizontal_timing(self.horizontal_dic['min_sample_rate'], self.horizontal_dic['min_num_pts'], self.horizontal_dic['ref_position'], self.horizontal_dic['num_records'], self.horizontal_dic['enforce_realtime'])
            
    @property
    def chan_conf(self):
        return self.chan_conf
    
    @chan_conf.setter
    def chan_conf(self, cc):
        self.chan_conf =  cc
        self._session.configure_chan_characteristics(self.chan_conf['input_impedance'], self.chan_conf['max_frequency'])
        
    @property
    def eq_conf(self):
        return self._eq_conf
    
    @eq_conf.setter
    def eq_coeff(self):
        self._session.configure_equalization_filter_coefficients(self.coeff)

    def get_status(self):
        print(f'Current acquisition status : {self.session.acquisition_status()}')
        return self._session.acquisition_status()      

        
#===================================================================================================================================
#__Trigger config__ 
#===================================================================================================================================

    @property
    def trigger_type(self):
        print(f'Actual trigger type | {self.trigger_type}')
        return self._trigger_type
    
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
            self._session.configure_trigger_immediate()
        elif (self.trigger_type == "DIG"):
            self._session.configure_trigger_digital(self._trigger_dic['trigger_source'], self._trigger_dic['slope'], self._trigger_dic['holdoff'], self._trigger_dic['delay'])
        elif (self.trigger_type == "EDGE"):
            self._session.configure_trigger_edge(self._trigger_dic['trigger_source'], self._trigger_dic['level'], self._trigger_dic['trigger_coupling'], self._trigger_dic['slope'], self._trigger_dic['holdoff'], self._trigger_dic['delay'])
        elif (self.trigger_type == 'SOF'):
            self._session.configure_trigger_software(self._trigger_dic['holdoff'], self._trigger_dic['delay'])

#===================================================================================================================================
#__Session__ configuration__ 
#===================================================================================================================================

    @property
    def devicename(self):
        print(f'Actual device name | {self._devicename}')
        return self._devicename
     
    @property              
    def session(self):  
        print(f'Actual _session | {self._session}')   
        return self._session
    
    @property              
    def status(self):     
        print(f'Actual status | {self._status} ')
        return self._status
    
    @status.setter
    def status(self):
        self._status = self._session.acquisition_status()
    
    @status.getter
    def status(self):
        return self._session.acquisition_status()
    
    @session.setter                  
    def _session(self):            
        self._session = ni._session(self.devicename)
    
    @session.deleter 
    def session(self):
        self._session.close()
    
    def reset(self):
        self._session.reset()
    
    def calibrate(self):            
        self._session.self_cal(option=ni.Option.SELF_CALIBRATE_ALL_CHANNELS)
    
    def test(self):
        self._session.self_test()    

    def device_reset(self):
        self._session.reset_device()     
        
    def reset_with_def(self):
        self._session.reset_with_defaults()    
    
    def commit(self):
        self._session.commit()

    @property 
    def channels(self):
        print(f'Actual channels list | {self._channels}')
        return self._channels
    
    @channels.setter 
    def channels(self):
        self._channels = self._session.channels
        
    def get_enabled(self):
        return self._session.enabled_channels

    def enable_channels(self):
        for i in range(self._session.channel_count):
            self._channels[i].channel_enabled = True
                
#===================================================================================================================================
#__Waveform processing__
#===================================================================================================================================

    @property
    def waveform(self):
        print(f'Actual waveforms | {self._waveform}')
        return self._waveform
    
    @waveform.deleter
    def waveform(self):
        print('Deleting waveforms...')
        self._waveform = []

    @waveform.setter
    def waveform(self, wf):
        self._waveform = wf   
    
    def add_wfm_proc(self, meas_function):
        self._session.add_waveform_processing(meas_function)
        
    def clear_wfm_stats(self,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):
        self._session.clear_waveform_measurement_stats(clearable_measurement_function)
    
    def clear_wfm_proc(self):
        self._session.clear_waveform_processing()


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
        self.waveform.extend([self._channels[i].fetch(num_samples=self._acq_conf['lenght'], timeout=timeout, relative_to=self._acq_conf['relative_to'], num_records=self._acq_conf['num_records']) for i in self._channels])
        
    
    def fill_matrix(self, return_data=False):
        for i in range(self.acq_conf['num_records']):
            self.i_matrix_ch0.append(np.array(self._waveform[0][i].samples))
            self.q_matrix_ch0.append(np.array(self._waveform[1][i].samples))
            self.timestamp_ch0.append(self._waveform[0][i].absolute_initial_x)
            try:
                self.i_matrix_ch1.append(np.array(self._waveform[2][i].samples))
                self.q_matrix_ch1.append(np.array(self._waveform[3][i].samples))
                self.timestamp_ch1.append(self._waveform[2][i].absolute_initial_x)
            except Exception:
                pass
        if return_data:
            return self._i_matrix, self._q_matrix, self._timestamp
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
            except Exception:
                pass