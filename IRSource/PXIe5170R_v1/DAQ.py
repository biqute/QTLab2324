# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================

import niscope as ni
import hightime
import sys
sys.path.insert(1, r'F:\\LabIV\\QTLab2324\\IRSource\\logs\\sessions')
import logging

class DAQ(object):
    
    logger = logging.getLogger(__name__) #initialize logger
    
    _instance = None

    def __new__(self, device_name, device_address, rd, dic, trigger: dict, channels=[0,1], records=3, sample_rate=5e7, length=4000, ref_pos=20.0):
        if self._instance is None:
            try:
                self._instance = super(DAQ, self).__new__(self)
                self._session = ni.Session(device_address, id_query=id, reset_device=rd, options=dic)

                self._devicename = device_name
                print('Connected to', self._devicename)
                self.logger.debug("Connection to PXIe-5170R success")
                
            except Exception as e:
                raise RuntimeError("Could not connect to PXIe-5170R") from e
            
            self.length   = length
            self.trigger  = trigger
            self.channels = channels
            self.records  = records
            self.sample_rate = sample_rate
            self.pos_ref = ref_pos
            self.waveform = []
            self.encorceRT = True
            self.i_matrix_ch0, self.q_matrix_ch0, self.timestamp_ch0 = [], [], []
            self.i_matrix_ch1, self.q_matrix_ch1, self.timestamp_ch1 = [], [], []

        if trigger["trigger_type"] == 'CONTINUOS':
            self.config_software_trigger()
        else:
            self.session.trigger_type       = getattr(ni.TriggerType, trigger["trigger_type"])
            self.session.trigger_source     = trigger["trigger_source"]
            self.session.trigger_slope      = getattr(ni.TriggerSlope, trigger["trigger_slope"])
            self.session.trigger_level      = float(trigger["trigger_level"])
            self.session.trigger_delay_time = float(trigger["trigger_delay"])

        self.get_status()
            
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
                self.logger.debug('Calibration failed!')
                raise ValueError("Self calibration failed") from e
            
    def test(self):
            try:
                self._session.self_test()
                print('Running test routine...')
                self.logger.debug('Running test routine...')
            except Exception as e:
                self.logger.debug("Test failed")
                raise  ValueError("Test failed") from e      
            
    def reset(self):

        try: 
            print('Resetting session')
            self._session.reset()     
            self.logger.debug("Resetting session")
        except Exception as e:
            self.logger.debug("Session reset didn't work")
            raise ValueError("Session reset didn't work")
            
    def reset_device(self):

        try: 
            print("Resetting device")
            self._session.reset_device()     
            self.logger.debug("Resetting device")
        except Exception as e:
            self.logger.debug("Resetting device didn't work")
            raise ValueError("Resetting device didn't work")
        
    def reset_with_def(self):

        try: 
            print("Resetting with defaults")
            self._session.reset_with_defaults()    
            self.logger.debug("Resetting with defaults done")
        except Exception as e:
            self.logger.debug("Resetting with defaults didn't work")
            raise ValueError("Resetting with defaults didn't work")
        
    def get_status(self):
        self.logger.debug("Acquisition status: " + str(self.session.acquisition_status())) 
        return None
        
    def disable(self):

        try:
            print('Disabling')
            self._hanlde.disable()
            self.logger.debug("Disabling worked")
        except Exception as e:
            self.logger.debug("Disabling didn't work")
            raise ValueError("Disabling didn't work")
            
            
    def commit(self):
        try:
            print('Committing')
            self._session.commit()
            self.logger.debug("Committing worked")
        except Exception as e:
            self.logger.debug("Committing didn't work")
            raise ValueError("Committing didn't work")
            
        
    def initiate(self):

        try:
            print('Starting acquisition')
            self._session.initiate()
            self.logger.debug("Acquisition started correctly")
        except Exception as e:
            self.logger.debug("Acquisition didn't start correctly")
            raise ValueError("Acquisition didn't start correctly")
        
# ==================================================================================================================================
#__Channels configuration__
#===================================================================================================================================        

    def config_vertical(self, range, coupling, offset, probe_attenuation, enabled):
        try:
            self.logger.debug("Configuring vertical done")
            self._session.configure_vertical(range, coupling, offset, probe_attenuation, enabled)
        except Exception as e:
            self.logger.debug("Vertical config went wrong")
            raise ValueError("Vertical config went wrong")
            

    def config_chan_char(self, input_impedance, max_input_frequency):

        try:
            self.logger.debug("Channels characteristics configuration done")
            self._session.configure_chan_characteristics(input_impedance, max_input_frequency)
        except Exception as e:
            self.logger.debug("Channels characteristics configuration went wrong")
            raise ValueError("Channels characteristics configuration went wrong")
        
        
    def config_eqfilt_coeff(self, coefficients):

        try:
            self.logger.debug("Equalization filter configuration done")
            self._session.configure_equalization_filter_coefficients(coefficients)
        except Exception as e:
            self.logger.debug("Equalization filter configuration went wrong")
            raise ValueError("Equalization filter configuration went wrong")
        
    def config_hor_timing(self, min_sample_rate, min_num_pts, ref_position, num_records, enforce_realtime):

        try:
            self.logger.debug("Horizontal timing configuration done")
            self._session.configure_horizontal_timing(min_sample_rate, min_num_pts, ref_position, num_records, enforce_realtime)
        except Exception as e:
            self.logger.debug("Horizontal timing configuration went wrong")
            raise ValueError("Horizontal timing configuration went wrong")
                                    
#===================================================================================================================================
#__Waveform processing__
#===================================================================================================================================

    def add_wfm_proc(self, meas_function):

        try:
            self.logger.debug("Waveform processing added correctly")
            self._session.add_waveform_processing(meas_function)
        except Exception as e:
            self.logger.debug("Adding Waveform processing went wrong")
            raise ValueError("Adding Waveform processing went wrong")
        
        
    def clear_wfm_stats(self,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):

        try:
            self.logger.debug("Waveform stats cleared correctly")
            self._session.clear_waveform_measurement_stats(clearable_measurement_function)
        except Exception as e:
            self.logger.debug("Clearing waveform stats went wrong")
            raise ValueError("Clearing waveform stats went wrong")
        

    def clear_wfm_proc(self):
        
        try:
            self.logger.debug("Waveform proc cleared correctly")
            self._session.clear_waveform_processing()
        except Exception as e:
            self.logger.debug("Clearing waveform proc went wrong")
            raise ValueError("Clearing waveform proc went wrong")
        
#===================================================================================================================================
#__Trigger config__ 
#===================================================================================================================================

    def config_dig_trigger(self,trigger_source, slope=ni.TriggerSlope.POSITIVE, holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0)):

        try:
            self.logger.debug("Digital trigger configuration done correctly")
            self._session.configure_trigger_digital(trigger_source, slope, holdoff, delay)
        except Exception as e:
            self.logger.debug("Digital trigger configuration went wrong")
            raise ValueError("Digital trigger configuration went wrong")


    def config_edge_trigger(self, trigger_source, level, trigger_coupling, slope=ni.TriggerSlope.POSITIVE, holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0)):
        
        try:
            self.logger.debug("Edge trigger configuration done correctly")
            self._session.configure_trigger_edge(trigger_source, level, trigger_coupling, slope, holdoff, delay)
        except Exception as e:
            self.logger.debug("Edge trigger configuration went wrong")
            raise ValueError("Edge trigger configuration went wrong")


    def config_software_trigger(self,holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0)):
       
        try:
            self.logger.debug("Software trigger configuration done correctly")
            self._session.configure_trigger_software(holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0))
        except Exception as e:
            self.logger.debug("Software trigger configuration went wrong")
            raise ValueError("Software trigger configuration went wrong")

#===================================================================================================================================
#__Fetching and reading__
#===================================================================================================================================

    def fetch(self, num_samples=None, relative_to=ni.FetchRelativeTo.PRETRIGGER, offset=0, record_number=0, num_records=None, timeout=hightime.timedelta(seconds=5.0)):
        
        try:
            self._session.fetch(num_samples, relative_to, offset, record_number, num_records, timeout) 
            self.logger.debug("Fetching done correctly")       
        except Exception as e:
            self.logger.debug("Fetching went wrong")
            raise ValueError("Fetching went wrong")
        
    def read(self,num_samples=0, relative_to=ni.FetchRelativeTo.PRETRIGGER, offset=0, record_number=0, num_records=0, timeout=hightime.timedelta(seconds=5.0)):
       
        try:
            self.logger.debug("Reading done correctly")
            self.waveform.extend([self._session.channels[i].read(num_samples, num_records, timeout=5) for i in self.channels])
        except Exception as e:
            self.logger.debug("Reading went wrong")
            raise ValueError("Reading went wrong")