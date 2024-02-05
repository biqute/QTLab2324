# [NI-SCOPE Python API](https://niscope.readthedocs.io/en/latest/niscope.html)

## Installation:
```bash
python -m pip install niscope
```

## Usage:
```Python
import niscope
with niscope.Session("Dev1") as session:
    session.channels[0].configure_vertical(range=1.0, coupling=niscope.VerticalCoupling.AC)
    session.channels[1].configure_vertical(range=10.0, coupling=niscope.VerticalCoupling.DC)
    session.configure_horizontal_timing(min_sample_rate=50000000, min_num_pts=1000, ref_position=50.0, num_records=5, enforce_realtime=True)
    with session.initiate():
        waveforms = session.channels[0,1].fetch(num_records=5)
    for wfm in waveforms:
        print('Channel {0}, record {1} samples acquired: {2:,}\n'.format(wfm.channel, wfm.record, len(wfm.samples)))

    # Find all channel 1 records (Note channel name is always a string even if integers used in channel[])
    chan1 = [wfm for wfm in waveforms if wfm.channel == '0']

    # Find all record number 3
    rec3 = [wfm for wfm in waveforms if wfm.record == 3]
```
### Comments:

---
```Python
with niscope.Session("Dev1") as session:
```
- Establishes a session with a specific NI device named `"Dev1"`;
- The `with` statement ensures proper resource management and cleanup.
---
```Python
session.channels[0].configure_vertical(range=1.0, coupling=niscope.VerticalCoupling.AC)
session.channels[1].configure_vertical(range=10.0, coupling=niscope.VerticalCoupling.DC)
```
- [`configure_vertical`](https://niscope.readthedocs.io/en/latest/class.html#configure-vertical):  Configures the most commonly configured properties of the digitizer vertical subsystem, such as the range, offset, coupling, probe attenuation, and the channel;
- Configures vertical settings for channel 0 and 1:
    - [`range`](https://niscope.readthedocs.io/en/latest/class.html#niscope.Session.vertical_range): Sets the absolute value of the voltage range to 1.0 V (from -0.5 V to +0.5 V);
    - [`coupling`](https://niscope.readthedocs.io/en/latest/class.html#niscope.Session.vertical_coupling): Specifies how the digitizer couples the input signal for the channel. Sets the coupling to AC (alternating current).
---
```Python
session.configure_horizontal_timing(min_sample_rate=50000000, min_num_pts=1000, ref_position=50.0, num_records=5, enforce_realtime=True)
```
- [`configure_horizontal_timing`](https://niscope.readthedocs.io/en/latest/class.html#configure-horizontal-timing): Configures the common properties of the horizontal subsystem for a multi-record acquisition in terms of minimum sample rate:
    - [`min_sample_rate`](https://niscope.readthedocs.io/en/latest/class.html#niscope.Session.min_sample_rate): Specify the sampling rate for the acquisition in Samples per second. Sets the minimum sample rate to 50 MHz;
    - `min_num_pts`: The minimum number of points you need in the record for each channel;
    - `ref_position`: The position of the Reference Event in the waveform record specified as a percentage. Sets the reference position (trigger point) to 50% of the record length.
		[**Reference Position:**](https://documentation.help/NI-SCOPE-LabVIEW/Reference_Position.html) Specifies the position of the Reference Event in the waveform record as a percentage of the record. When the digitizer detects a trigger, it waits the length of time the [Trigger Delay](https://documentation.help/NI-SCOPE-LabVIEW/Trigger_Delay.html) property specifies. The event that occurs when the delay time elapses is the Reference Event. The Reference Event is relative to the start of the record and is a percentage of the record length. For example, the value 50.0 corresponds to the center of the waveform record and 0.0 corresponds to the first element in the waveform record;
    - `num_records`: The number of records to acquire. Specifies to acquire 5 records.
    - `enforce_realtime`: Indicates whether the digitizer enforces real-time measurements or allows equivalent-time (RIS) measurements.
---
```Python
with session.initiate():
```
- [`initiate`](https://niscope.readthedocs.io/en/latest/class.html#niscope.Session.initiate): Initiates a waveform acquisition. After calling this method, the digitizer leaves the Idle state and waits for a trigger.
---
```Python
waveforms = session.channels[0,1].fetch(num_records=5)
```
- Fetches acquired waveforms from channels 0 and 1, collecting 5 records for each channel.
- [`fetch`](https://niscope.readthedocs.io/en/latest/class.html#fetch): Returns the waveform from a previously initiated acquisition that the digitizer acquires for the specified channel. This method returns scaled voltage waveforms. This method may return multiple waveforms depending on the number of channels, the acquisition type, and the number of records you specify.
- **NOTE:** If you need faster fetch performance, or to directly interface with [SciPy](https://www.scipy.org/), you can use the [`fetch_into()`](https://niscope.readthedocs.io/en/latest/class.html#fetch-into) method instead of `fetch()`.
