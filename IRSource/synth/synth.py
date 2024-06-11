from typing import Any
from pyvisa import ResourceManager as rm
import pyvisa
import functools
from Decorators import utils

class synth:
    def __init__(self, board): 
        try:     
            self.board = board
            self.address = rm.open_resource(board) 
            self.frequency = '1GHz'
            self.name = None
            self.power = '15'
            self.outpt_status = 'OFF'
        except pyvisa.VisaIOError:
            raise ("Requested port is wrong or not available")
        
    def __new__(cls, *args, **kwargs):
        try:
            print('Creating new synth class instance')
            instance = super().__new__(cls)
            return instance
        except Exception as e:
            print('Could not create new synth class instance')
            
    def __name__(self):
        if self.name is None:
            self.set_name()
            
    @property
    def board(self):
        return self.board
            
    @property
    def frequency(self):
        return self.frequency
    
    @property 
    def name(self):
        return self.name
    
    @property 
    def power(self):
        return self.power
    
    @property
    def outpt_status(self):
        return 
    
    @utils.caller
    @frequency.setter
    def frequency(self, f): 
        #metodo che imposta la frequenza in uscita dal sintetizzatore
        #N.B. Occorre scrivere la frequenza 'frequenza' con anche l'unità di misura e l'ordine di gandezza in simboli:
        #     si deve scrivere, accanto al valore numerico: GHz, MHz, KHz, Hz, ...
        #     L'ordine di grandezza di default sono i milli Hertz: mlHz, quindi se non si specifica nulla, vengono considerati milli Hertz
        self.address.write('FREQ ' + str(f))
    
    @utils.caller
    @frequency.getter
    def frequency(self): #metodo che restituisce la frequenza impostata in uscita
        f = self.address.query('FREQ?')
        return f
    
    @utils.caller
    @name.setter
    def name(self): #metodo che restituisce il nume dello strumento
        self.name = self.address.query('*IDN?')
    
    @utils.caller
    @name.getter
    def name(self): #metodo che restituisce il nume dello strumento
        nome_strumento = self.address.query('*IDN?')
        return nome_strumento

    @utils.caller
    def reset(self): #metodo che resetta lo strumento
        self.address.write('*RST')
        return  
    
    #METODO INUTILE PERCHE' I SINTETIZZATORI NON HANNO LA POSSIBILITA' DI AVERE UNA POTENZA VARIBAILE
    @utils.caller
    @power.setter
    def power(self, potenza): #metodo che imposta la potenza in uscita, il valore è in dBm
        #N.B. Eventualmente si può inserire anche la potenza con un segno meno
        self.address.write('POW ' + str(potenza))
        return  

    #METODO INUTILE PERCHE' I SINTETIZZATORI NON HANNO LA POSSIBILITA' DI AVERE UNA POTENZA VARIBAILE
    @utils.caller
    @power.getter
    def power(self): #metodo che restituisce la potenza impostata in uscita
        potenza = self.address.query('POW?')
        return potenza
    
    @utils.caller
    def get_temperature(self): #metodo che restituisce la temperatura del sintetizzatore in gradi Celsius
        temperatura = self.address.query('DIAG:MEAS?')
        return temperatura

    @utils.caller
    @outpt_status.setter
    def outpt_status(self,cmd): #metodo che abilita la fuoriuscita della frequenza dal sintetizzatore
        self.address.write('OUTP:STAT '+str(cmd))
        return

    @utils.caller
    @outpt_status.getter
    def outpt_status(self): #se la frequenza è abilitata lo strumento ritorna 1(ON), altrimenti 0(OFF)
        status = self.address.write('OUTP:STAT?')
        if status == 1:
            return 'ON'
        elif status == 0:
            return 'OFF'

    @utils.caller
    def frequency_sweep_fast(self, freq_min, freq_max, N): #metodo che imbastisce uno sweep in frequenza veloce
        tempo_attesa = 0.5 #il tempo da attendere tra una misurazione e l'altra dello sweep, in secondi
        N_sweep = 1 #numero di volte con cui eseguire l'intero sweep in frequenza (il numero 0 fa partire un numero infinito di sweep)
        self.address.write('SWE:FAST:FREQ:SETUP ' + str(freq_min) + ',' + str(freq_max) + ',' + str(N) + ',15,' + str(tempo_attesa) + 's,' + str(N_sweep) + ',0,0,RUN')
        return

    @utils.caller
    def start_frequency_sweep_fast(self): #metodo che fa partire il fast sweep in frequenza
        N_sweep = 1 #numero di volte con cui eseguire l'intero sweep in frequenza (il numero 0 fa partire un numero infinito di sweep)
        self.address.write('SWE:FAST:FREQ:STAR ' + str(N_sweep))
        return

    @utils.caller
    def frequency_sweep(self, freq_min, freq_max, intervallo_freq): #metodo che imbastisce uno sweep in frequenza
    #A differenza dello sweep fast, qui si deve fornire il valore di frequenza 'intervallo_freq' da uare come intervallo per passare da una frequenza minore ad una maggiore
        tempo_attesa = '0.5'
        N_sweep = 1
        self.address.write('SWE:NORM:FREQ:SETUP ' + str(freq_min) + ',' + str(freq_max) + ',' + str(intervallo_freq) + ',15,' + str(tempo_attesa) + 's,' + str(N_sweep) + ',0,0,RUN')
        return

    @utils.caller
    def start_frequency_sweep(self): #metodo che fa partire lo sweep in frequenza
        N_sweep = 1
        self.address.write('SWE:NORM:FREQ:STAR ' + str(N_sweep))
        return

    @utils.caller
    def stop_sweep(self): #metodo che ferma lo sweep, sia che si tratti di uno sweep normale, che di un fast sweep; si aper sweep in frequenza che per sweep in potenza
        self.address.write('SWE:STOP')
        return
