# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================
import sys
sys.path.insert(1,r'C:\Users\oper\SynologyDrive\Lab2023\Qubit\QTLab2324')
from datetime import datetime
import wave
import niscope as ni
from niscope.errors import DriverError
import numpy as np
import h5py
from Decorators import utils
date = datetime.now().strftime("%m-%d-%Y")

class DAQ():

    _instance = None
    
    def __init__(self):
        self._session = None
        self._status = None
        self._channels = []
        self._waveform = []
        self._acq_conf = {}
        self._i_matrix_ch0, self._q_matrix_ch0, self._timestamp_ch0 = [], [], []
        self._i_matrix_ch1, self._q_matrix_ch1, self._timestamp_ch1 = [], [], []
        self._devicename      = None
        self._acq_conf        = None
        self._eq_conf         = None
        self._trigger_dic     = None
        self._trigger_type    = None
        self._vertical_conf   = {}
        self._horizontal_conf = {}

            
    @property
    def devicename(self):
        print(f'Actual device name | {self._devicename}')
        return self._devicename
    
    @devicename.setter
    def devicename(self, dv):
        self._devicename = dv

    @devicename.deleter
    def devicename(self):
        del self._devicename
#===================================================================================================================================
#__Card__ configuration__ 
#===================================================================================================================================            
    
    @property
    def acq_conf(self):
        return self._acq_conf

    @acq_conf.setter
    def acq_conf(self, config):
        self._acq_conf = config
    
    
    @property
    def vertical_conf(self):
        return self._vertical_conf
    
    @vertical_conf.setter
    def vertical_conf(self, vc):
        self._vertical_conf = vc
            
    @property
    def horizontal_conf(self):
        return self._horizontal_conf
    
    @horizontal_conf.setter
    def horizontal_conf(self,hc):
        self._horizontal_conf = hc
        
            
    @property
    def chan_conf(self):
        return self.chan_conf
    
    @chan_conf.setter
    def chan_conf(self, cc):
        self._chan_conf =  cc
        
    @property
    def eq_conf(self):
        return self._eq_conf
    
    @eq_conf.setter
    def eq_coeff(self, value):
        self._eq_conf = value

    def set_eq_coeff(self):
        self._session.configure_equalization_filter_coefficients(self._eq_coeff)
        

    def get_status(self):
        print(f'Current acquisition status : {self.session.acquisition_status()}')
        return self._session.acquisition_status()      

        
#===================================================================================================================================
#__Trigger config__ 
#===================================================================================================================================

    @property
    def trigger_type(self):
        print(f'Actual trigger type | {self._trigger_type}')
        return self._trigger_type
    
    @trigger_type.setter
    def trigger_type(self):
        self._trigger_type = self._trigger_dic['trigger_type']
        
    @property
    def trigger_dic(self):
        return self._trigger_dic
    
    @trigger_dic.setter
    def trigger_dic(self, dic):
        self._trigger_dic = dic
        self._trigger_type = dic['trigger_type']
    
    def config_trigger(self):
        if(self._trigger_type == "IMM"):
            self._session.configure_trigger_immediate()
        elif (self._trigger_type == "DIG"):
            self._session.configure_trigger_digital(self._trigger_dic['trigger_source'], self._trigger_dic['slope'], self._trigger_dic['holdoff'], self._trigger_dic['delay'])
        elif (self._trigger_type == "EDGE"):
            self._session.configure_trigger_edge(self._trigger_dic['trigger_source'], self._trigger_dic['level'], self._trigger_dic['trigger_coupling'], self._trigger_dic['slope'], self._trigger_dic['holdoff'], self._trigger_dic['delay'])
        elif (self._trigger_type == 'SOF'):
            self._session.configure_trigger_software(self._trigger_dic['holdoff'], self._trigger_dic['delay'])

#===================================================================================================================================
#__Session__ configuration__ 
#===================================================================================================================================
     
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
    def session(self, devicename):            
        self._session = ni.Session(devicename)
    
    @session.deleter 
    def session(self):
        self._session.close()
        del self._session
    
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
        print(f'Channels list in class member| {self._channels}')
        return self._channels
    
    @channels.setter 
    def channels(self):
        self._channels = self._session.channels

    @channels.getter
    def channels(self, retrieve=True):
        if retrieve:
            print(f'Actual channels in session | {self._session.channels}')
            return self._session.channels

        
    def get_enabled(self):
        return self._session.enabled_channels

    def enable_channels(self):
        if self._session is not None:
            for i in range(self._session.channel_count):
                try:
                    self._channels[i].channel_enabled = True
                except Exception:
                    print(f'Not working on channel n°{i}')

                
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
        del self._waveform 

    @waveform.setter
    def waveform(self, wf):
        self._waveform = wf   

    @property
    def record_lenght(self):
        return self._acq_conf['min_num_points']
    
    @record_lenght.getter
    def record_lenght(self, retrieve_info):
        if retrieve_info:
            return self._session.horz_min_num_pts
        
    @property
    def num_records(self):
        return self._acq_conf['num_records']
    
    @num_records.getter
    def num_records(self, retrieve_info):
        if retrieve_info:
            return self._session.horz_record_length

    
    def add_wfm_proc(self, meas_function):
        self._session.add_waveform_processing(meas_function)
        
    def clear_wfm_stats(self,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):
        self._session.clear_waveform_measurement_stats(clearable_measurement_function)
    
    def clear_wfm_proc(self):
        self._session.clear_waveform_processing()


#===================================================================================================================================
#__Acquiring data__
#===================================================================================================================================
    
    def configure_channels(self):
        self._session.channels[0].configure_vertical(range = self._vertical_conf['range'], coupling = self._vertical_conf['coupling'])
        self._session.channels[1].configure_vertical(range = self._vertical_conf['range'], coupling = self._vertical_conf['coupling'])
        self._session.channels[2].configure_vertical(range = self._vertical_conf['range'], coupling = self._vertical_conf['coupling'])
        self._session.channels[3].configure_vertical(range = self._vertical_conf['range'], coupling = self._vertical_conf['coupling'])
        self._session.configure_horizontal_timing(self.horizontal_conf['sample_rate'], self.horizontal_conf['min_num_pts'], self.horizontal_conf['ref_position'], self.horizontal_conf['num_records'], self.horizontal_conf['enforce_realtime'])        

    @utils.exec_time
    def fetch(self, trig):
        with self._session.initiate():
            trig()
            try:
                return self._session.channels[0,1,2,3].fetch()
            except DriverError:
                print(f'DriverError in {ni.Session}')

    def acquire(self):
        try:
            self._waveform = (self._session.channels[0,1].fetch(num_samples=self._acq_conf['length'], timeout=self._acq_conf['timeout'], relative_to=self._acq_conf['relative_to'], num_records=self._acq_conf['num_records']))
        except DriverError:
            print(f'DriverError in {ni.Session.channels}')

    @utils.exec_time
    def single_acquisition(self, trigger):
        total_samples = int(self._acq_conf['acq_time'] * self._acq_conf['sample_rate'])
        with self._session as session:
            trigger()
            self.configure_channels()
            with session.initiate():
                wf_info = []
                waveforms = session.channels[0,1,2,3].fetch(num_samples=total_samples, relative_to=self._acq_conf['relative_to'], offset=self._acq_conf['offset'], record_number=self._acq_conf['num_records'], timeout=self._acq_conf['timeout'])
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
        self.waveform(waveforms)
        return waveforms, wf_info
                    

    @utils.exec_time
    def acquisition(self):
        self._i_matrix_ch0.append(np.array(self.session.channels[self.channels[0]].read(num_samples=self._acq_conf['length'], timeout=5)[0].samples).mean())
        self._q_matrix_ch0.append(np.array(self.session.channels[self.channels[1]].read(num_samples=self._acq_conf['length'], timeout=5)[0].samples).mean())
        self._i_matrix_ch1.append(np.array(self.session.channels[self.channels[2]].read(num_samples=self._acq_conf['length'], timeout=5)[0].samples).mean())
        self._q_matrix_ch1.append(np.array(self.session.channels[self.channels[3]].read(num_samples=self._acq_conf['length'], timeout=5)[0].samples).mean())

        return None

    def fill_matrix(self, return_data=False):
        for i in range(self.acq_conf['num_records']):
            self._i_matrix_ch0.append(np.array(self._waveform[0][i].samples))
            self._q_matrix_ch0.append(np.array(self._waveform[1][i].samples))
            self._timestamp_ch0.append(self._waveform[0][i].absolute_initial_x)
            try:
                self._i_matrix_ch1.append(np.array(self._waveform[2][i].samples))
                self._q_matrix_ch1.append(np.array(self._waveform[3][i].samples))
                self._timestamp_ch1.append(self._waveform[2][i].absolute_initial_x)
            except Exception:
                pass
        if return_data:
            return self._i_matrix_ch0, self._q_matrix_ch0, self._timestamp_ch0
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