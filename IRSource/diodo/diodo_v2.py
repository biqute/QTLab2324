import pyvisa



class AFG310:

    _board = None
    _amplitude = None
    _diode = None
    _mode = None
    _func = None
    _freq = None

    def __init__(self):
        print('Creating object instance...')
        
    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board
        self._diode.write('MODE1; :OUTP1 ON; :SOUR1')   #accende la porta 1

    def connect(self):
        pyvisa.ResourceManager().open_resource(self._board)        

    @property
    def amplitude(self):
        return self._amplitude
    
    @amplitude.setter
    def amplitude(self, amp):
        self._amplitude = amp
        self._diode.write('SOUR:VOLT:AMPL '+str(amp))    #fissa ampiezza del segnale             

    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, mode = 'TRIG', n = '0' ): #CONT = continuo, TRIG: fa un ciclo dopo il trigger esterno, BURS: fa n cicli dopo un trigger
        if mode == 'BURS':
            self._diodo.write(f':MODE1 BURS;BCO {n}:' ) #n va da 0 a 60'000, oppure INF
        else:
            self._diodo.write(f':MODE1 {mode}:')

    @property
    def func(self):
        return self._func
    
    @func.setter
    def func(self, type, phase = 0):         #f = SIN, SQUare, TRIangle, RAMP, PULSe, PRNoise, DC, USER1/2/3/3, EMEMory
        self._diodo.write(f':FUNC {type}')
        if phase != 0:
            self._diodo.write(f':FUNC:PHAS {phase}')

    @property
    def freq(self):
        return self._freq
    
    @freq.setter
    def freq(self, ni):
        self._freq = ni


    def reset(self):
        self._diodo.write('*RST')
        self._diodo.write('OUTP1 1')
        self._diodo.write('MODE1;OUTP1:STAT ON;SOUR1;SOUR:VOLT:AMPL 1')
        

    def trigger(self):
        self._diodo.write('*TRG')

    def sweep(self, time):
        self._diodo.write(f':SWE:TIME {time}')  #numero decimale da 1ms a 500 s
        return

    def pulse(self, tempo = 0):    #inserisco il tempo di durata del segnale, in s

        if tempo<1:    
            if tempo == 0:
                self.set_freq(16e6)    #tempo è la durata dell'impulso, noi la vorremmo la minor possibile, in s
                ratio = 1
                self.func('SQU')
                self._diodo.write(f'SOUR:PULS:DCYC {ratio}')
            else:
                self.set_freq(1/(100*tempo))             #tempo è la durata dell'impulso, noi la vorremmo la minor possibile, in s
                ratio = 1
                self.func('SQU')
                self._diodo.write(f'SOUR:PULS:DCYC {ratio}')
        
        else:
            self.set_freq(1e-2)    #tempo è la durata dell'impulso, noi la vorremmo la minor possibile, in s
            ratio = tempo/100
            self.func('SQU')
            self._diodo.write(f'SOUR:PULS:DCYC {ratio}')
        return


'''
1. creo la variabile diodo, che avrà inizialmente settati il canale di uscita e l'ampiezza del segnale
2. set_mode() se senza argomento, setta la modalità burst
3. con pulse(f,t) seleziono la funzione pulse, con una certa ratio e frequenza, che aspetterà il trigger per partire
4. trigger() fa partire il diodo

 ++ se voglio cambiare funzione conviene fare reset() e usare set_func() e set_freq()

'''
