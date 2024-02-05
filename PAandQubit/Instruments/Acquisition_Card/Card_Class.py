# NI_PXIe-1071 : 8375, 5170R, 6133 (8 inputs)

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

        self._session = None
        self._connect_success = False
        self._sleep = 1


    
    def available(self):
        try:
            ni.Session(self._dev_name)
            self._connect_success = True
            print("Connection successful!")
        except:
            print(f"Unable to establish a connection.")


    def voltag_range(self, voltage_range):
        self._voltage_range = voltage_range



    def coupling():
    def sample_rate():
    def num_pts():
    def num_records():
    def fetch(self, ):
        with ni.Session(self._dev_name) as session: # Name of the device
        session.channels[0].configure_vertical(range = voltage_range, coupling=ni.VerticalCoupling.AC)
        session.configure_horizontal_timing(min_sample_rate = 250e6, min_num_pts = n_pts, ref_position = 50.0, num_records = n_recs, enforce_realtime = True)
    with session.initiate(): # After calling this method, the digitizer leaves the Idle state and waits for a trigger
        waveforms = session.channels[0].fetch()
    for wfm in waveforms:
         print('Channel {0}, record {1} samples acquired: {2:,}\n'.format(wfm.channel, wfm.record, len(wfm.samples)))

a = waveforms[0].samples.tolist()

plt.plot(a)
    