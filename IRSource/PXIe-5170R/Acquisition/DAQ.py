# =======================================================================================================================================
# This class  is used to represent a NI-Scope device. It contains methods for DAQ set-up, acquiring data from the scope and plotting it.
# =======================================================================================================================================

import niscope as ni
import hightime

class DAQ(object):
    
# 1. Initialize the session
# A session establishes a connection between digitizers and your application.
# After this connection is established, the digitizer(s) can transmit data to your application.
# Sessions allow the driver to cache previous settings, which greatly improves performance.
    
    _instance = None

    def __new__(self, device_name, device_address, rd, dic, trigger: dict, channels=[0,1], records=3, sample_rate=5e7, length=4000, ref_pos=20.0):
        if self._instance is None:
            try:
                self._instance = super(DAQ, self).__new__(self)
                self._handle = ni.Session(device_address, id_query=id, reset_device=rd, options=dic)

                self._devicename = device_name
                print('Connected to', self._devicename)
                
            except Exception as e:
                raise RuntimeError("Could not connect to NI-DAQ device") from e
            
            self.length   = length
            self.trigger  = trigger
            self.channels = channels
            self.records  = records
            self.waveform = []
            self.i_matrix_ch0, self.q_matrix_ch0, self.timestamp_ch0 = [], [], []
            self.i_matrix_ch1, self.q_matrix_ch1, self.timestamp_ch1 = [], [], []
            
        return self._instance
    
# ==================================================================================================================================
#__SESSION DEFINITION +...__ 
#===================================================================================================================================
        
    def calibrate(self):            
            try:
                self._handle.self_cal(option=ni.Option.SELF_CALIBRATE_ALL_CHANNELS)
                print('Running calibration routine...')
            except Exception as e:
                raise  ValueError("Self calibration failed") from e
            
    def test(self):
            try:
                self._handle.self_test()
                print('Running test routine...')
            except Exception as e:
                raise  ValueError("Test failed") from e      
            
    def reset(self):
        ''' Stops the acquisition, releases routes, and all session properties are reset to their default states.'''
        self._handle.reset()     
        
    def reset_device(self):
        ''' Performs a hard reset of the device. Acquisition stops, all routes are released, RTSI and PFI lines are tristated,
        hardware is configured to its default state, and all session properties are reset to their default state. ''' 
        self._handle.reset_device()
        
    def reset_with_def(self):
        ''' Performs a software reset of the device, returning it to the default state and applying any initial default
        settings from the IVI Configuration Store. '''
        self._handle.reset_with_defaults()
        
    def disable(self):
        ''' Aborts any current operation, opens data channel relays, and releases RTSI and PFI lines. '''
        self._hanlde.disable()
        
    def commit(self):
        self._handle.commit()
        
    def initiate(self):
        ''' Initiates a waveform acquisition.
        After calling this method, the digitizer leaves the Idle state and waits for a trigger. 
        The digitizer acquires a waveform for each channel you enable with'''

        self._handle.initiate()
        
# ==================================================================================================================================
#__Channels and timing__
#===================================================================================================================================        

    def config_chan_char(self, input_impedance, max_input_frequency):
        ''' Configures the properties that control the electrical characteristics of the channel—the input impedance and the bandwidth.
    Parameters:
    input_impedance (float) -->   The input impedance for the channel; NI-SCOPE sets niscope.Session.input_impedance to this value.
    max_input_frequency (float)-->The bandwidth for the channel; NI-SCOPE sets niscope.Session.max_input_frequency to this value.
                                    Pass 0 for this value to use the hardware default bandwidth. 
                                    Pass -1 for this value to achieve full bandwidth.'''
        self._handle.configure_chan_characteristics(input_impedance, max_input_frequency)
        
        
    def config_eqfilt_coeff(self, coefficients):
        ''' Configures the custom coefficients for the equalization FIR filter on the device.
        Parameters: coefficients(list of floats) '''
        self._handle.configure_equalization_filter_coefficients(coefficients)
        
    def config_hor_timing(self, min_sample_rate, min_num_pts, ref_position, num_records, enforce_realtime):
        '''
Configures the common properties of the horizontal subsystem for a multirecord acquisition in terms of minimum sample rate.
Parameters:
    min_sample_rate (float) - The sampling rate for the acquisition. Refer to niscope.Session.min_sample_rate for more information.
    min_num_pts (int) - The minimum number of points you need in the record for each channel; call niscope.Session.ActualRecordLength()
    to obtain the actual record length used.
    Valid Values: Greater than 1; limited by available memory
    Note
    One or more of the referenced methods are not in the Python API for this driver.
    ref_position (float) --> The position of the Reference Event in the waveform record specified as a percentage.
    num_records (int) --> The number of records to acquire
    enforce_realtime (bool) --> Indicates whether the digitizer enforces real-time measurements or allows equivalent-time
    (RIS) measurements; not all digitizers support RIS—refer to Features Supported by Device for more information.
    Default value: True/Defined Values/True—Allow real-time acquisitions only/False—Allow real-time and equivalent-time acquisitions
'''
        self._handle.configure_horizontal_timing(min_sample_rate, min_num_pts, ref_position, num_records, enforce_realtime)
                                    
#===================================================================================================================================
#__Waveform processing__
#===================================================================================================================================

    def add_wfm_proc(self, meas_function):
        ''' Adds one measurement to the list of processing steps that are completed before the measurement. '''
        self._handle.add_waveform_processing(meas_function)
        
    def clear_wfm_stats(self,clearable_measurement_function=ni.ClearableMeasurement.ALL_MEASUREMENTS):
        ''' Clears the waveform stats on the channel and measurement you specify. If you want to clear all of the measurements,
use ALL_MEASUREMENTS in the clearableMeasurementFunction parameter. '''
        self._handle.clear_waveform_measurement_stats(clearable_measurement_function)

    def clear_wfm_proc(self):
        ''' Clears the list of processing steps assigned to the given channel. The processing is added using the 
niscope.Session.add_waveform_processing() method, where the processing steps are completed in the same order 
in which they are registered. The processing measurements are streamed, so the result of the first processing step 
is used as the input for the next step. The processing is also done before any other measurements.'''
        self._handle.clear_waveform_processing()
        


#===================================================================================================================================
#__Trigger__ 
#===================================================================================================================================

    def config_dig_trigger(self,trigger_source, slope=ni.TriggerSlope.POSITIVE, holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0)):
        '''
Configures the common properties of a digital trigger.

When you initiate an acquisition, the digitizer waits for the start trigger, which is configured through the 
niscope.Session.acq_arm_source (Start Trigger Source) property. The default is immediate. 
Upon receiving the start trigger the digitizer begins sampling pretrigger points. 
After the digitizer finishes sampling pretrigger points, the digitizer waits for a reference (stop) trigger that you 
specify with a method such as this one. Upon receiving the reference trigger the digitizer finishes the acquisition 
after completing posttrigger sampling. With each Configure Trigger method, you specify configuration parameters such 
as the trigger source and the amount of trigger delay.

Parameters:
trigger_source (str) -> Specifies the trigger source. Refer to niscope.Session.trigger_source for defined values.
slope (niscope.TriggerSlope) -> Specifies whether you want a rising edge or a falling edge to trigger the digitizer.
holdoff (hightime.timedelta, datetime.timedelta, or float in seconds) -> The length of time the digitizer waits 
after detecting a trigger before enabling NI-SCOPE to detect another trigger.
delay (hightime.timedelta, datetime.timedelta, or float in seconds) -> How long the digitizer waits after receiving the trigger
to start acquiring data. Refer to niscope.Session.trigger_delay_time for more information.
'''
        self._handle.configure_trigger_digital(trigger_source, slope, holdoff, delay)


    def config_edge_trigger(self, trigger_source, level, trigger_coupling, slope=ni.TriggerSlope.POSITIVE, holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0)):
        '''
Configures common properties for analog edge triggering.

The default is immediate. Upon receiving the start trigger the digitizer begins sampling pretrigger points.
After the digitizer finishes sampling pretrigger points, the digitizer waits for a reference (stop) trigger
that you specify with a method such as this one. Upon receiving the reference trigger the digitizer finishes
the acquisition after completing posttrigger sampling. 

Parameters: 
trigger_source (str) -> Specifies the trigger source. Refer to niscope.Session.trigger_source for defined values.

level (float) -> The voltage threshold for the trigger. Refer to niscope.Session.trigger_level for more information.

trigger_coupling (niscope.TriggerCoupling) -> Applies coupling and filtering options to the trigger signal. Refer to niscope.Session.trigger_coupling for more information.

slope (niscope.TriggerSlope) -> Specifies whether you want a rising edge or a falling edge to trigger the digitizer. Refer to niscope.Session.trigger_slope for more information.

holdoff (hightime.timedelta, datetime.timedelta, or float in seconds) -> The length of time the digitizer waits after detecting a trigger before enabling NI-SCOPE to detect another trigger. Refer to niscope.Session.trigger_holdoff for more information.

delay (hightime.timedelta, datetime.timedelta, or float in seconds) -> How long the digitizer waits after receiving the trigger to start acquiring data. Refer to niscope.Session.trigger_delay_time for more information.
'''
        self._handle.configure_trigger_edge(trigger_source, level, trigger_coupling, slope, holdoff, delay)


    def config_software_trigger(self,holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0)):
        '''
Configures common properties for software triggering.
When you initiate an acquisition, the digitizer waits for the start trigger, which is configured through the 
niscope.Session.acq_arm_source (Start Trigger Source) property. The default is immediate. Upon receiving the 
start trigger the digitizer begins sampling pretrigger points. After the digitizer finishes sampling pretrigger points,
the digitizer waits for a reference (stop) trigger that you specify with a method such as this one. Upon receiving the 
reference trigger the digitizer finishes the acquisition after completing posttrigger sampling. With each Configure Trigger method,
you specify configuration parameters such as the trigger source and the amount of trigger delay.

Parameters:
holdoff (hightime.timedelta, datetime.timedelta, or float in seconds) -> The length of time the digitizer waits after detecting a trigger before enabling NI-SCOPE to detect another trigger. Refer to niscope.Session.trigger_holdoff for more information.
delay (hightime.timedelta, datetime.timedelta, or float in seconds) -> How long the digitizer waits after receiving the trigger to start acquiring data. Refer to niscope.Session.trigger_delay_time for more information.
'''
        self._handle.configure_trigger_software(holdoff=hightime.timedelta(seconds=0.0), delay=hightime.timedelta(seconds=0.0))


#===================================================================================================================================
#__Fetching__
#===================================================================================================================================

    def  fetch(self, num_samples=None, relative_to=ni.FetchRelativeTo.PRETRIGGER, offset=0, record_number=0, num_records=None, timeout=hightime.timedelta(seconds=5.0)):
        '''
Returns the waveform from a previously initiated acquisition that the digitizer acquires for the specified channel.
This method returns scaled voltage waveforms.
This method may return multiple waveforms depending on the number of channels, the acquisition type, 
and the number of records you specify.

Parameters:
num_samples (int) – The maximum number of samples to fetch for each waveform. If the acquisition finishes with fewer points than requested, some devices return partial data if the acquisition finished, was aborted, or a timeout of 0 was used. If it fails to complete within the timeout period, the method raises.
relative_to (niscope.FetchRelativeTo) – Position to start fetching within one record.
offset (int) – Offset in samples to start fetching data within each record. The offset can be positive or negative.
record_number (int) – Zero-based index of the first record to fetch.
num_records (int) – Number of records to fetch. Use -1 to fetch all configured records.
timeout (hightime.timedelta, datetime.timedelta, or float in seconds) – The time to wait for data to be acquired; using 0 for this parameter tells NI-SCOPE to fetch whatever is currently available. Using -1 seconds for this parameter implies infinite timeout.

Return type: list of WaveformInfo
Returns: 
Returns a list of class instances with the following timing and scaling information about each waveform:
relative_initial_x (float) the time (in seconds) from the trigger to the first sample in the fetched waveform
absolute_initial_x (float) timestamp (in seconds) of the first fetched sample. This timestamp is comparable between records and acquisitions; devices that do not support this parameter use 0 for this output.
x_increment (float) the time between points in the acquired waveform in seconds
channel (str) channel name this waveform was acquired from
record (int) record number of this waveform
gain (float) the gain factor of the given channel; useful for scaling binary data with the following formula:
offset (float) the offset factor of the given channel; useful for scaling binary data with the following formula:
samples (array of float) floating point array of samples. Length will be of the actual samples acquired
'''
        self._handle.fetch()
        
        
    def read(self,num_samples=None, relative_to=ni.FetchRelativeTo.PRETRIGGER, offset=0, record_number=0, num_records=None, timeout=hightime.timedelta(seconds=5.0)):
        '''
Initiates an acquisition, waits for it to complete, and retrieves the data.
With niscope.Session.read(), you enable all channels specified with channelList before the acquisition;
in the other method, you enable the channels with niscope.Session.configure_vertical().
This method may return multiple waveforms depending on the number of channels, the acquisition type, and the number of 
records you specify.

Parameters:
num_samples (int) – The maximum number of samples to fetch for each waveform. If the acquisition finishes with fewer points than requested, some devices return partial data if the acquisition finished, was aborted, or a timeout of 0 was used. If it fails to complete within the timeout period, the method raises.
relative_to (niscope.FetchRelativeTo) – Position to start fetching within one record.
offset (int) – Offset in samples to start fetching data within each record. The offset can be positive or negative.
record_number (int) – Zero-based index of the first record to fetch.
num_records (int) – Number of records to fetch. Use -1 to fetch all configured records.
timeout (hightime.timedelta, datetime.timedelta, or float in seconds) – The time to wait for data to be acquired; using 0 for this parameter tells NI-SCOPE to fetch whatever is currently available. Using -1 seconds for this parameter implies infinite timeout.

Return type: list of WaveformInfo

Returns:
Returns a list of class instances with the following timing and scaling information about each waveform:
relative_initial_x (float) the time (in seconds) from the trigger to the first sample in the fetched waveform
absolute_initial_x (float) timestamp (in seconds) of the first fetched sample. This timestamp is comparable between records and acquisitions; devices that do not support this parameter use 0 for this output.
x_increment (float) the time between points in the acquired waveform in seconds
channel (str) channel name this waveform was acquired from
record (int) record number of this waveform
gain (float) the gain factor of the given channel; useful for scaling binary data with the following formula:
offset (float) the offset factor of the given channel; useful for scaling binary data with the following formula:
samples (array of float) floating point array of samples. Length will be of the actual samples acquired
'''
        self._handle.read(num_samples, relative_to, offset, record_number, num_records, timeout)