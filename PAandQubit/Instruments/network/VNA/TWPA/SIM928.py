# Stanford_Research_Systems,SIM900,s/n152741,ver3.6


#########################################################################################################
#              Methods               :              Description
#                                    :
#       [1. Basic methods]           :
# 1.1 | __init__ ................... : initializes object attributes in a class.
# 1.2 | get_name ................... : Returns the instrument identification.
# 1.3 | reset ...................... : Sets the instrument to a defined default status.
# 1.4 | clear ...................... : Clear status.
#                                    :
#                                    :
#                                    :
#########################################################################################################à



import pyvisa
import time


class SIM928:

# 1.1 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def __init__(self):

        self._resource = None
        self._connect_success = False
        self._sleep = 1

        try:
            rm = pyvisa.ResourceManager()
            self._resource = rm.open_resource("ASRL34::INSTR")
            self._connect_success = True
            print("Connection successful!")
        except pyvisa.Error as e:
            print(f"Unable to establish a connection: {e}")

# 1.2 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def get_name(self):
        print(self._resource.query('*IDN?'))
        
# 1.3 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def reset(self):
        self._resource.write('*RST')
        time.sleep(self._sleep)

# 1.4 ----------------------------------------------------------------------------------------------------------------------------------------------- #

    def clear(self):
        self._resource.write('*CLS')     
        time.sleep(self._sleep)




    def module_connect(self, slot: int, name: str):                 #connessione a uno degli 8 slot
        self._resource.write(f'CONN {slot}, "{name}"')     

    def set_voltage(self, voltage: float):
        """Input : Volt"""
        self._resource.write(f'VOLT {voltage}') 

    def output_on(self):
        """Turn the output on."""
        self._resource.write("OPON")

    def output_off(self):
        """Turn the output on."""
        self._resource.write("OPOF")

    

   