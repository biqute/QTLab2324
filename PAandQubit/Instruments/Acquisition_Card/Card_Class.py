# NI_PXIe-1071 : 8375, 5170R, 6133

##### https://niscope.readthedocs.io/en/latest/class.html#read ######

import niscope as ni

class PXIe5170R:

    def __init__(self, resource_name: str = 'PXI1Slot2'):

        self._resource_name     = resource_name
        self._voltage_range     = 1
        self._coupling          = 'DC'
        self._sample_rate       = int(250e6)
        self._num_pts           = 500
        self._num_records       = 1
        self._ref_pos           = 50.0
        self._sleep = 1

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
    def voltag_range(self, value):
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
        self._sample_rate = value
    
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
        

    def acquisition(self):
        with ni.Session(self._resource_name) as session:
            session.configure_vertical(range = self._voltage_range, coupling = self._coupling)
            session.configure_horizontal_timing(
                min_sample_rate     = self.sample_rate, 
                min_num_pts         = self._num_pts, 
                ref_position        = self._ref_pos, 
                num_records         = self._num_records, 
                enforce_realtime    = True
                )