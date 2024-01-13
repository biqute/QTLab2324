# NI_PXIe-1071 : 8375, 5170R, 6133 (8 inputs)

##### https://niscope.readthedocs.io/en/latest/class.html#read ######




import pyvisa
import numpy as np
import time
import h5py 



class NIPXIe:

# 1.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def __init__(self):

        self._resource = None
        self._connect_success = False
        self._sleep = 1

        try:
            rm = pyvisa.ResourceManager()
            self._resource = rm.open_resource("PXI0::1::BACKPLANE")
            self._connect_success = True
            print("Connection successful!")
        except pyvisa.Error as e:
            print(f"Unable to establish a connection: {e}")

# 1.2 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def get_name(self):
        if self._connect_success:
            print(self._resource.query('*IDN?'))
        else:
            print("Error: No active connection.")
        
# 1.3 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def reset(self):
        if self._connect_success:
            self._resource.write('*RST')
            time.sleep(self._sleep)
        else:
            print("Error: No active connection.")

# 1.4 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def clear(self):
        if self._connect_success:
            self._resource.write('*CLS')     
            time.sleep(self._sleep)
        else:
            print("Error: No active connection.")