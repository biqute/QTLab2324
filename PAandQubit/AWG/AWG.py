# MANUAL: https://www.keysight.com/it/en/assets/9018-03714/service-manuals/9018-03714.pdf?success=true
# pag 212

import pyvisa
import matplotlib.pyplot as plt
import numpy as np


ip = '192.168.40.11'
rm = pyvisa.ResourceManager()
resource = rm.open_resource(f"GPIB0::10::INSTR")

# print(resource.query('*IDN?'))



# resource.write('SOUR1:APPL:PULS [{<frequency>|MIN|MAX|DEF} [,{<amplitude>|MIN|MAX|DEF} [,{<offset>|MIN|MAX|DEF}]]]')
# resource.write('SOUR1:FREQ 2000')
# resource.write('SOUR1:VOLT 0.2')

# resource.write('OUTP1 1')

resource.write('SOUR1:FUNC PULS')
# SIN, SQU, TRI, RAMP, PULS, PRBS, NOIS, ARB, or DC