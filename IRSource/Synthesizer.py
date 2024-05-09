import pyvisa
import numpy as np

class Synthesizer:
    _instance = None
    _synth = None
    print('numero == 1 per il primo synth; numero == 2 per il secondo synth')

    def __new__(self, numero_synth):
        indirizzo_uno = 'COM5'
        indirizzo_due = 'COM26'
        if self._instance is None:
            if numero_synth == 1:
                self._instance = super(Synthesizer, self).__new__(self)
                self._synth = pyvisa.ResourceManager().open_resource(indirizzo_uno)
                print('Si è connessi correttamente al sintetizzatore numero 1!\n')
                return self._instance
            else if numero_synth == 2:
                self._instance = super(Synthesizer, self).__new__(self)
                self._synth = pyvisa.ResourceManager().open_resource(indirizzo_due)
                printf('Si è connessi correttamente al sintetizzatore numero 2!\n')
                return self._instance
    
    def ask_name(self): #metodo che restituisce il nume dello strumento
        nome_strumento = self._synth.query('*IDN?')
        return nome_strumento

    def reset(self): #metodo che resetta lo strumento
        self._synth.write('*RST')
        return

    def get_frequency(self): #metodo che restituisce la frequenza impostata in uscita
        frequenza = self._synth.query('FREQ?')
        return frequenza

    def set_frequency(self, frequenza): #metodo che imposta la frequenza in uscita dal sintetizzatore
    #N.B. Occorre scrivere la frequenza 'frequenza' con anche l'unità di misura e l'ordine di gandezza in simboli
    #     ossia si deve scrivere, accanto al valore numerico: GHz, MHz, KHz, Hz, ...
    #     L'ordine di grandezza di default sono i milli Hertz: mlHz, quindi se non si specifica nulla, vengono considerati milli Hertz
        self._synth.write('FREQ ' + str(frequenza))
        return

    def get_power(self): #metodo che restituisce la potenza impostata in uscita
        potenza = self._synth.query('POW?')
        return potenza

    def set_power(self, potenza): #metodo che imposta la potenza in uscita, il valore è in dBm
        #N.B. Eventualmente si può inserire anche la potenza con un segno meno
        self._synth.write('POW ' + str(potenza))
        return
    
    def start_frequency(self): #metodo che abilita la fuoriusita della frequenza dal sintetizzatore
        self._synth.write('OUTP:STAT ON')
        return

    def stop_frequency(self): #metodo che disabilita la fuoriuscita della frequenza dal sintetizzatore
        self._synth.write('OUTP:STAT OFF')
        return

    def frequency_status(self): #se la frequenza è abilitata lo strumento ritorna 1(ON), altrimenti 0(OFF)
        status = self._synth.write('OUTP:STAT?')
        if status == 1:
            return 'ON'
        else if status == 0:
            return 'OFF'

    def frequency_sweep_fast(self, freq_min, freq_max, N, potenza): #metodo che imbastisce uno sweep in frequenza veloce
    #Per sweep veloce si intende uno sweep in cui bisogna fornire il numero N di frequenze, tra la massima e la minima, da cosiderare nello sweep
    #Bisogna fornire la frequenza minima (feq_min), la frequenza massima (freq_max), il numero di punti (N)
    #nello sweep, la potenza (potenza) da fissare durente lo sweep
        tempo_attesa = 0.5 #il tempo da attendere tra una misurazione e l'altra dello sweep, in secondi
        N_sweep = 1 #numero di volte con cui eseguire l'intero sweep in frequenza (il numero 0 fa partire un numero infinito di sweep)
        self._synth.write('SWE:FAST:FREQ:SETUP ' + str(freq_min) + ',' + str(freq_max) + ',' + str(N) + ',' + str(potenza) + ',' + str(tempo_attesa) + 's,' + str(N_sweep) + ',0,0')
        return

    def start_frequency_sweep_fast(self): #metodo che fa partire il fast sweep in frequenza
        N_sweep = 1 #numero di volte con cui eseguire l'intero sweep in frequenza (il numero 0 fa partire un numero infinito di sweep)
        self._synth.write('SWE:FAST:FREQ:STAR ' + str(N_sweep))
        return

    def frequency_sweep(self, freq_min, freq_max, intervallo_freq, potenza): #metodo che imbastisce uno sweep in frequenza
    #A differenza dello sweep fast, qui si deve fornire il valore di frequenza 'intervallo_freq' da uare come intervallo per passare da una frequenza minore ad una maggiore
        tempo_attesa = 0.5
        N_sweep = 1
        self._synth.write('SWE:NORM:FREQ:SETUP ' + str(freq_min) + ',' + str(freq_max) + ',' + str(intervallo_freq) + ',' + str(potenza) + ',' + str(tempo_attesa) + 's,' + str(N_sweep) + ',0,0')
        return

    def start_frequency_sweep(self): #metodo che fa partire lo sweep in frequenza
        N_sweep = 1
        self._synth.write('SWE:NORM:FREQ:STAR ' + str(N_sweep))
        return

    def power_sweep_fast(self, pow_min, pow_max, N, frequenza):
        tempo_attesa = 0.5
        N_sweep = 1
        self._synth.write('SWE:FAST:POW:SETUP  ' + str(pow_min) + ',' + str(pow_max) + ',' + str(N) + ',' + str(frequenza) + ',' + str(tempo_attesa) + ',' + str(N_sweep) + ',0,0')
        return

    def start_power_sweep_fast(self):
        N_sweep = 1
        self._synth.write('SWE:FAST:POW:STAR ' + str(N_sweep))
        return

    def power_sweep(self, pow_min, pw_max, intervallo_pow, frequenza):
        tempo_attesa = 0.5
        N_sweep = 1
        self._synth.write('SWE:NORM:POW:SETUP ' + str(pow_min) + ',' + str(pow_max) + ',' + str(intervallo_pow) + ',' + str(frequenza) + ',' + str(tempo_attesa) + ',' + str(N_sweep) + ',0,0') 
        return

    def start_power_sweep(self):
        N_sweep = 1
        self._synth.write('SWE:NORM:POW:STAR ' + str(N_sweep))
        return

    def stop_sweep(self): #metodo che ferma lo sweep, sia che si tratti di uno sweep normale, che di un fast sweep; si aper sweep in frequenza che per sweep in potenza
        self._synth.write('SWE:STOP')
        return
