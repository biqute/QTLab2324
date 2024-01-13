#class developed in order to communicate with KelvinoxIGH (Gas Handler)

import pyvisa

class GHandler:

    _instance = None
    _gh = None

    def __new__(self, board = 'ASRL1::INSTR'):
        if self._instance is None:
            print('Creating the object')
            self._instance = super(GHandler, self).__new__(self)
            self._gh = pyvisa.ResourceManager().open_resource(board)
            self._path = "C:/Users/kid/SynologyDrive/Lab2023/KIDs/QTLab2324/IRdetection/Instruments/Test_data/" #saves path for data files
            print('GH object created correctly!\n')
        return self._instance

    def set_control(self, mode = "C1"):
        #defines instrument control status
        #C0 = Local & Locked, C1 = Remote & Locked, C2 = Local & Unlocked, C3 = Remote & Unlocked
        return self._gh.write(mode)

    def get_mix_temp(self): #gets the mix chamber temperature
        return self._gh.query('R3')
    
    def get_mix_pow(self): #gets the mix chamber power
        return self._gh.query('R4')
    
    def set_mix_mode(self, mode = "A3"): 
        #sets the mix chamber operation mode
        #A1 = off, A2 = fixed heater power, A3 = temperature control
        return self._gh.write(mode)

    def set_mix_power(self, power_value): #sets the mix chamber power value; values must be between 0000 and 1999
        self._gh.write('M' + str(power_value))
        return
    
    def set_mix_power_exp(self, power_exp): 
        #sets the mix chamber range exponent
        #E1, E2, ... , E5
        return self._gh.write(power_exp)

    def sleep(self, sleep_time_value):
        self._gh.write('W' + str(sleep_time_value))
        return


