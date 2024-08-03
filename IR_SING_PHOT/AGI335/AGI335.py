import pyvisa

class AGI335:

    _board = None
    _pulser = None
    _frequency = 1
    _function = 'SQU'
    _duty_cycle = 50
    _offset = 0.5
    _output = 0

    def __init__(self):
        print('OBJECT INSTANCE CREATED')
        return 
        
    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        try:
            board in pyvisa.ResourceManager().list_resources()
            print('VALID BOARD')
            self._board = board
        except: 
            raise ConnectionError('BOARD IS NOT VALID')
        
    def connect(self):
        self._pulser = pyvisa.ResourceManager().open_resource(self._board)

    def idn(self):
        return str(self._pulser.query('*IDN?'))

    @property
    def is_connected(self):
        return 'Agilent' in self.idn()

    @property
    def frequency(self):
        return self.frequency

    @frequency.setter
    def frequency(self, f):
        self._pulser.write('FREQ '+str(f))

    @frequency.getter
    def frequency(self):
        return self._pulser.query('FREQ?')

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, func):
        self._pulser.write('FUNC '+str(func))

    @function.getter
    def function(self):
        return self._pulser.query('FUNC?')

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output='OFF'):
        self._pulser.write('OUTP '+str(output))
    
    @output.getter
    def output(self):
        if '0' in self._pulser.query('OUTP?'):
            return 'OFF'
        else:
            return 'ON'

    @property
    def duty_cycle(self):
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, percent):
        self._pulser.write('FUNC:PULS:DCYC '+str(percent))

    @duty_cycle.getter
    def duty_cycle(self):
        return float(self._pulser.query('FUNC:PULS:DCYC?'))

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, V):
        self._pulser.write('VOLT '+str(V))

    @voltage.getter
    def voltage(self):
        return float(self._pulser.query('VOLT?'))

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self,offset):
        self._pulser.write('VOLT:OFFS '+str(offset))

    @offset.getter
    def offset(self):
        return self._pulser.query('VOLT:OFFS?')

    @property
    def trigger_mode(self):
        return self.trigger_mode

    @trigger_mode.setter
    def trigger_mode(self,mode):
        self._pulser.write('TRIG:SOUR '+str(mode))

    @trigger_mode.getter
    def trigger_mode(self):
        return self._pulser.query('TRIG:SOUR?')

    def execute_trigger(self):
        #For remote triggering BUS mode has to be selected
        self._pulser.write('*TRG')