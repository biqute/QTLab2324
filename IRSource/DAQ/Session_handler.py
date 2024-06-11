import niscope as ni
from IRSource.DAQ import DAQ

class Session_handler(DAQ):
    
    def __init__(self,devicename):
        self._session = None
        self._status = None
        self._channels = []
        try:
            print(f'Inheriting from {Session_handler} class')
            self._card = super().__init__(devicename)
            self._devicename = self.card._device
        except Exception:
            print(f'Could no inherit from {Session_handler} class')

#===================================================================================================================================
#__Session__ configuration__ 
#===================================================================================================================================

    @property
    def devicename(self):
        print(f'Actual device name | {self._devicename}')
        return self._devicename
     
    @property              
    def session(self):  
        print(f'Actual session | {self._session}')   
        return self._session
    
    @property              
    def status(self):     
        print(f'Actual status | {self._status} ')
        return self._status
    
    @status.setter
    def status(self):
        self._status = self.session.acquisition_status()
    
    @status.getter
    def status(self):
        return self.session.acquisition_status()
    
    @session.setter                  
    def session(self):            
        self.session = ni.Session(self.devicename)
    
    @session.deleter 
    def session(self):
        self.session.close()
    
    def reset(self):
        self.session.reset()
    
    def calibrate(self):            
        self.session.self_cal(option=ni.Option.SELF_CALIBRATE_ALL_CHANNELS)
    
    def test(self):
        self.session.self_test()    

    def device_reset(self):
        self.session.reset_device()     
        
    def reset_with_def(self):
        self.session.reset_with_defaults()    
    
    def commit(self):
        self.session.commit()

    @property 
    def channels(self):
        return self._channels
    
    @channels.setter 
    def channels(self):
        self._channels = self.session.channels
        
    def get_enabled(self):
        return self.session.enabled_channels

    def enable_channels(self):
        for i in range(self.session.channel_count):
            self.session.channels[i].channel_enabled = True
            
    def get_status(self):
        print(str(self.session.acquisition_status()))
        return self.session.acquisition_status()
    
#===================================================================================================================================
#__Waveform processing__
#===================================================================================================================================
    
    def add_wfm_proc(self, meas_function):
        self.session.add_waveform_processing(meas_function)
        
    def clear_wfm_stats(self,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):
        self.session.clear_waveform_measurement_stats(clearable_measurement_function)
    
    def clear_wfm_proc(self):
        self.session.clear_waveform_processing()