import pyvisa
import numpy as np


class AFG310:


    _instance = None
    _diodo = None

    def __new__(self, board = 'GPIB0::1::INSTR'):  #NOME PORTA INGRESSO COMPUTER
        if self._instance is None:

            self._instance = super(AFG310, self).__new__(self)
            self._diodo = pyvisa.ResourceManager().open_resource(board)

            self._diodo.write('MODE1; :OUTP1 ON; :SOUR1')   #accende la porta 1
            self._diodo.write('SOUR:VOLT:AMPL 1')           #fissa ampiezza del segnale             
            #self._diodo.write(':AM:STAT OFF;FM:STAT OFF;FSK:STAT OFF') 
            '''ATTENZIONE AGLI SPAZI, SONO IMPORTANTI, quando si inseriscono dei valori di grandezze fisiche si mettono dopo uno spazio, se selezionano ad esempio un canale dell'afg no'''

            print('AFG object created correctly!\n')

        return self._instance 
    

'''Pag 136, bisogna capire il tipo di segnale
    così come l'outp state
    da pag 137 iniziano i comandi seri'''

#funzioni importanti

def set_mode(self, mode = 'TRIG', n = '0' ): #CONT = continuo, TRIG: fa un ciclo dopo il trigger esterno, BURS: fa n cicli dopo un trigger
    if mode == 'BURS' or mode == 'burs':
        self._diodo.write(':MODE1 BURS;BCO ' + n ) #n va da 0 a 60'000, oppure INF
    else: self._diodo.write(':MODE1 ' + mode )
    return

def pulse(self, freq = 0, tempo = 0):    #freq è la frequenza con cui si ripete un ciclo in Hz
    
    if freq == 0 and tempo == 0:
        self.set_freq(1e5)             #tempo è la durata dell'impulso, noi la vorremmo la minor possibile, in s
        ratio = 1
        self.func('SQU')
        self._diodo.write(f'SOUR:PULS:DCYC {ratio}')
    else:
        self.set_freq(freq)             #tempo è la durata dell'impulso, noi la vorremmo la minor possibile, in s
        ratio = tempo*freq*100
        self.func('SQU')
        self._diodo.write(f'SOUR:PULS:DCYC {ratio}')
    return




def reset(self):
    self._diodo.write('*RST')
    self._diodo.write('OUTP1 1')
    self._diodo.write('MODE1;OUTP1:STAT ON;SOUR1;SOUR:VOLT:AMPL 1')
    return

def trigger(self):
    self._diodo.write('*TRG')
    return


#funzioni accessorie

def set_func(self, type, phase = 0):      #f = SIN, SQUare, TRIangle, RAMP, PULSe, PRNoise, DC, USER1/2/3/3, EMEMory
    self._diodo.write(f':FUNC {type}')
    if phase != 0:
        self._diodo.write(f':FUNC:PHAS {phase}')
    return

def set_freq(self, freq):
    self._diodo.write(':FREQ '+ str(freq))
    return

def sweep(self, time):
    self._diodo.write(f':SWE:TIME {time}')  #numero decimale da 1ms a 500 s
    return
#pag 193 vedi insieme
#funzioni utili fino a 180
#da 194 esempi di comandi




'''
1. creo la variabile diodo, che avrà inizialmente settati il canale di uscita e l'ampiezza del segnale
2. set_mode() se senza argomento, setta la modalità burst
3. con pulse(f,t) seleziono la funzione pulse, con una certa ratio e frequenza, che aspetterà il trigger per partire
4. trigger() fa partire il diodo

 ++ se voglio cambiare funzione conviene fare reset() e usare set_func() e set_freq()

'''