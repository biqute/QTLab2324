import pyvisa

#righe di codice da scrivere per collegarsi ai due sintetizzatori, dopo aver importato la classe
'''
synth_uno = Synthesizer.Synthesizer(1)
synth_due = Synthesizer.Synthesizer(2)
synth_uno.connettore()
synth_due.connettore()
'''

class Synthesizer:
    def __init__(self): #nell'inizializzazione del sintetizzatore occorre specificare se si sta costruendo la classe per il sintetizzatore uno o due
        self.indirizzo = None

    def connettore(self, porta): #metodo che serve per potersi connettere al sintetizzatore scelto 
            try:
                self.indirizzo = pyvisa.ResourceManager().open_resource(porta)
            except Exception:
                raise ConnectionRefusedError(f'Could not connect to board {porta}')

    def ask_name(self): #metodo che restituisce il nume dello strumento
        nome_strumento = self.indirizzo.query('*IDN?')
        return nome_strumento

    def reset(self): #metodo che resetta lo strumento
        self.indirizzo.write('*RST')
        return

    def get_frequency(self): #metodo che restituisce la frequenza impostata in uscita
        frequenza = self.indirizzo.query('FREQ?')
        return frequenza

    def set_frequency(self, frequenza): #metodo che imposta la frequenza in uscita dal sintetizzatore
    #N.B. Occorre scrivere la frequenza 'frequenza' con anche l'unità di misura e l'ordine di gandezza in simboli:
    #     si deve scrivere, accanto al valore numerico: GHz, MHz, KHz, Hz, ...
    #     L'ordine di grandezza di default sono i milli Hertz: mlHz, quindi se non si specifica nulla, vengono considerati milli Hertz
        self.indirizzo.write('FREQ ' + str(frequenza) +  'GHz')
        return

    #METODO INUTILE PERCHE' I SINTETIZZATORI NON HANNO LA POSSIBILITA' DI AVERE UNA POTENZA VARIBAILE
    def get_power(self): #metodo che restituisce la potenza impostata in uscita
        potenza = self.indirizzo.query('POW?')
        return potenza

    #METODO INUTILE PERCHE' I SINTETIZZATORI NON HANNO LA POSSIBILITA' DI AVERE UNA POTENZA VARIBAILE
    def set_power(self, potenza): #metodo che imposta la potenza in uscita, il valore è in dBm
        #N.B. Eventualmente si può inserire anche la potenza con un segno meno
        self.indirizzo.write('POW ' + str(potenza))
        return
    
    def get_temperature(self): #metodo che restituisce la temperatura del sintetizzatore in gradi Celsius
        temperatura = self.indirizzo.query('DIAG:MEAS?')
        return temperatura

    def outp_frequency_on(self): #metodo che abilita la fuoriuscita della frequenza dal sintetizzatore
        self.indirizzo.write('OUTP:STAT ON')
        return

    def outp_frequency_off(self): #metodo che disabilita la fuoriuscita della frequenza dal sintetizzatore
        self.indirizzo.write('OUTP:STAT OFF')
        return

    def frequency_status(self): #se la frequenza è abilitata lo strumento ritorna 1(ON), altrimenti 0(OFF)
        status = self.indirizzo.write('OUTP:STAT?')
        if status == 1:
            return 'ON'
        elif status == 0:
            return 'OFF'

    def frequency_sweep_fast(self, freq_min, freq_max, N): #metodo che imbastisce uno sweep in frequenza veloce
    #Per sweep veloce si intende uno sweep in cui bisogna fornire il numero N di frequenze, tra la massima e la minima, da cosiderare nello sweep
    #Bisogna fornire la frequenza minima (feq_min), la frequenza massima (freq_max), il numero di punti (N)
    #nello sweep, la potenza (potenza) da fissare durente lo sweep
        tempo_attesa = 0.5 #il tempo da attendere tra una misurazione e l'altra dello sweep, in secondi
        N_sweep = 1 #numero di volte con cui eseguire l'intero sweep in frequenza (il numero 0 fa partire un numero infinito di sweep)
        self.indirizzo.write('SWE:FAST:FREQ:SETUP ' + str(freq_min) + ',' + str(freq_max) + ',' + str(N) + ',15,' + str(tempo_attesa) + 's,' + str(N_sweep) + ',0,0,RUN')
        return

    def start_frequency_sweep_fast(self): #metodo che fa partire il fast sweep in frequenza
        N_sweep = 1 #numero di volte con cui eseguire l'intero sweep in frequenza (il numero 0 fa partire un numero infinito di sweep)
        self.indirizzo.write('SWE:FAST:FREQ:STAR ' + str(N_sweep))
        return

    def frequency_sweep(self, freq_min, freq_max, intervallo_freq): #metodo che imbastisce uno sweep in frequenza
    #A differenza dello sweep fast, qui si deve fornire il valore di frequenza 'intervallo_freq' da uare come intervallo per passare da una frequenza minore ad una maggiore
        tempo_attesa = '0.5'
        N_sweep = 1
        self.indirizzo.write('SWE:NORM:FREQ:SETUP ' + str(freq_min) + ',' + str(freq_max) + ',' + str(intervallo_freq) + ',15,' + str(tempo_attesa) + 's,' + str(N_sweep) + ',0,0,RUN')
        return

    def start_frequency_sweep(self): #metodo che fa partire lo sweep in frequenza
        N_sweep = 1
        self.indirizzo.write('SWE:NORM:FREQ:STAR ' + str(N_sweep))
        return

    def stop_sweep(self): #metodo che ferma lo sweep, sia che si tratti di uno sweep normale, che di un fast sweep; si aper sweep in frequenza che per sweep in potenza
        self.indirizzo.write('SWE:STOP')
        return
