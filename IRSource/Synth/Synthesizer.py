import pyvisa
import numpy as np

class Synthesizer:
    indirizzo = None
    istanza_uno = None
    istanza_due = None
    print('Inserire numero_synth == 1 per il primo synth; numero_synth == 2 per il secondo synth!')

    def __new__(self, numero_synth):
        indirizzo_uno = 'ASRL5::INSTR'
        indirizzo_due = 'ASRL26::INSTR'
        if numero_synth == 1:
            try:
                self.istanza_uno = super(Synthesizer, self).__new__(self)
                synth_uno = pyvisa.ResourceManager()
                synth_uno.list_resources()
                self.indirizzo = synth_uno.open_resource(indirizzo_uno)
                print("Si è connessi al synth_uno!")
                return self.istanza_uno
            except Exception as e:
                raise ValueError("Non è riuscita la connessione con il synth_uno!\n\t    Controllare che il synth_uno sia alimentato!")
        elif numero_synth == 2:
            try:
                self.istanza_due = super(Synthesizer, self).__new__(self)
                synth_due = pyvisa.ResourceManager()
                synth_due.list_resources()
                self.indirizzo = synth_due.open_resource(indirizzo_due)
                print("Si è connessi al synth_due!")
                return self.istanza_due
            except Exception as e:
                raise ValueError("Non è riuscita la connessione con il synth_uno!\n\t    Controllare che il synth_due sia alimentato!")

    '''
    def __new__(self, number):
        if self._instance_uno is None and number==1:
            try: 
                self._instance_uno = super(Synthesizer, self).__new__(self)
                self._synth_uno = pyvisa.ResourceManager().open_resource("COM5")
            except Exception as e:
                raise ConnectionError("Could not connect to first synth")
        if self._instance_due is None and number==2:
            try: 
                self._instance_due = super(Synthesizer, self).__new__(self)
                self._synth_uno = pyvisa.ResourceManager().open_resource("COM26")
            except Exception as e:
                raise ConnectionError("Could not connect to second synth")

        return self._instance_uno, self._instance_due
    '''
    def ask_name(self): #metodo che restituisce il nume dello strumento
        nome = self.indirizzo.query('*IDN?')
        return nome

    def reset(self): #metodo che resetta lo strumento
        self.indirizzo.write('*RST')
        return

    def get_frequency(self): #metodo che restituisce la frequenza impostata in uscita
        frequenza = self.indirizzo.query('FREQ?')
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
        elif status == 0:
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

    def power_sweep(self, pow_min, pow_max, intervallo_pow, frequenza):
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
