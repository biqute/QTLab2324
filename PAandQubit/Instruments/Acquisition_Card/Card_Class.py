# NI_PXIe-1071 : 8375, 5170R, 6133

##### https://niscope.readthedocs.io/en/latest/class.html#read ######

import niscope as ni
from niscope.errors import DriverError
import time
import sys

class digital_trigger:
    def __init__(self, source = 'VAL_PFI_0'):
        self._trig_src      = source
        self._slope         = ni.TriggerSlope.POSITIVE
        self._holdoff       = 0
        self._delay         = 0

    def configure(self, session: ni.Session):
        # session.acq_arm_source = 'NISCOPE_VAL_IMMEDIATE'
        session.configure_trigger_digital(
            trigger_source  = self._trig_src, 
            slope           = self._slope, 
            holdoff         = self._holdoff, 
            delay           = self._delay
            )

class edge_trigger:
    def __init__(self, source = '0'):
        self._trig_src      = source
        self._slope         = ni.TriggerSlope.POSITIVE
        self._holdoff       = 0
        self._delay         = 0
        self._level         = 0
        self._coupling      = ni.TriggerCoupling.DC
    
    def configure(self, session: ni.Session):
        session.configure_trigger_edge(
            trigger_source      = self._trig_src,
            trigger_coupling    = self._coupling,
            level               = self._level,
            slope               = self._slope,
            holdoff             = self._holdoff,
            delay               = self._delay 
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

        self._device_name = "PXIe_5170R"
        try:
            with ni.Session(self._resource_name) as _:
                print(f"{self._device_name}:    Connection successful!")
        except ni.Error as e:
            print(f"{self._device_name}:    Unable to establish a connection: {e}")


    @property
    def available(self):
        try:
            with ni.Session(self._resource_name) as _:
                print("Available communication.")
        except:
            print(f"Unable to establish a connection.")

    def close(self):
        ni.Session(self._resource_name).close()
        print(f"{self._device_name}: Session closed")
        
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
        

    def open(self, trigger_channel = '0'):
        self._session = ni.Session(self._resource_name)
        self._session.channels[0].configure_vertical(range = self._voltage_range, coupling = self._coupling)
        self._session.channels[1].configure_vertical(range = self._voltage_range, coupling = self._coupling)
        self._session.channels[2].configure_vertical(range = self._voltage_range, coupling = self._coupling)
        self._session.channels[3].configure_vertical(range = self._voltage_range, coupling = self._coupling)
        self._session.configure_horizontal_timing(
            min_sample_rate     = self.sample_rate, 
            min_num_pts         = self._num_pts, 
            ref_position        = self._ref_pos, 
            num_records         = self._num_records, 
            enforce_realtime    = True
            )
        
        a = edge_trigger(str(trigger_channel))
        a.configure(self._session)
        
    def acquisition(self, trig):
        with self._session.initiate():
            trig()
            # print(self._session.acquisition_status())
            try:
                return self._session.channels[0,1,2,3].fetch()#relative_to = ni.FetchRelativeTo.TRIGGER)
            except DriverError:
                print('DriverError in ni.session.channels.fetch()')
                sys.exit(0)
            