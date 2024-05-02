# NI_PXIe-1071 : 8375, 5170R, 6133

##### https://niscope.readthedocs.io/en/latest/class.html#read ######

import niscope as ni
import time

class digital_trigger:
    def __init__(self, source = 'VAL_PFI_0'):
        self._trig_src      = source
        self._slope         = ni.TriggerSlope.POSITIVE
        self._holdoff       = 0
        self._delay         = 0

    def configure(self, session: ni.Session):
        session.configure_trigger_digital(
            trigger_source  = self._trig_src, 
            slope           = self._slope, 
            holdoff         = self._holdoff, 
            delay           = self._delay
            )

class PXIe5170R:

    def __init__(self, resource_name: str):                         # Initialize a default set up
        
        self._resource_name     = resource_name
        self._voltage_range     = 1
        self._coupling          = ni.VerticalCoupling.DC
        self._sample_rate       = int(250e6)
        self._num_pts           = 500
        self._num_records       = 1
        self._ref_pos           = 50.0
        self._sleep = 1

        try:
            with ni.Session(self._resource_name) as _:
                print("5170R: Available communication!")
        except:
            print(f"Unable to establish a connection.")


    @property
    def available(self):
        try:
            with ni.Session(self._resource_name) as _:
                print("Available communication.")
        except:
            print(f"Unable to establish a connection.")

    @property
    def voltage_range(self):
        return self._voltage_range
    
    @voltage_range.setter
    def voltage_range(self, value):
        self._voltage_range = value

    @property
    def coupling(self):
        return self._coupling
    
    @coupling.setter
    def coupling(self, value: str):
        mapping = {'AC': ni.VerticalCoupling.AC,'DC': ni.VerticalCoupling.DC}
        try:
            self._coupling = mapping[value]
        except:
            print("The available couplings are 'AC' or 'DC'.")

    @property
    def sample_rate(self):
        return self._sample_rate
    
    @sample_rate.setter
    def sample_rate(self, value):
        '''In Hz'''
        self._sample_rate = int(value)
    
    @property
    def num_pts(self):
        return self._num_pts

    @num_pts.setter
    def num_pts(self, value: int):
        self._num_pts = value

    @property
    def num_records(self):
        return self._num_records
    
    @num_records.setter
    def num_records(self, value: int):
        self._num_records = value
    
    @property
    def ref_position(self):
        return self._ref_pos
    
    @ref_position.setter
    def ref_position(self, value):
        self._ref_pos = value
        

    def open(self):
        self._session = ni.Session(self._resource_name)
        self._session.channels[0].configure_vertical(range = self._voltage_range, coupling = self._coupling)
        self._session.configure_horizontal_timing(
            min_sample_rate     = self.sample_rate, 
            min_num_pts         = self._num_pts, 
            ref_position        = self._ref_pos, 
            num_records         = self._num_records, 
            enforce_realtime    = True
            )
        a = digital_trigger()
        a.configure(self._session)
        
    def acquisition(self, trig):
        with self._session.initiate():
            time.sleep(0.1)
            trig()
            time.sleep(0.1)
            print(self._session.acquisition_status())
        return self._session.channels[0].fetch()
            
    
    # def aliasing(self):
    #     self._session.flex_fir_antialias_filter_type('FOURTYEIGHT_TAP_STANDARD')