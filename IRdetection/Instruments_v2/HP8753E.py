import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import h5_and as h5
import h5py


class HP8753E():
    def __init__(self,name='GPIB0::16::INSTR'):
        resources = pyvisa.ResourceManager()
        self._vna = resources.open_resource(name)
        self._sleep = 0.5     #sleep between commands
        self._path = None     #save path for data files
        self._params = {}
        self._channel = 'CHAN1'
        self._data_format = 'OUTPRE2'
        self._Scoeff = 'S21'       
        return

    def set_S_coeff(self, coeff):
        self._vna.write(str(coeff))

    def set_data_format(self, formato):
        self._vna.write(str(formato))
        
    def set_channel(self, canale):
        #What channel should we look at?
        self._vna.write(str(canale))

    def get_path(self):
        print('Current path: ', self._path)
        return    

    def reset(self):
        self._vna.write('*RST')
        return

    def set_sleep(self,time):
        self._sleep = time
        return    

    def get_name(self):
        print(self._vna.query('*IDN?'))    
        return

    def set_point(self,npt):
        self._vna.write('POIN '+str(npt))
        return

    def set_center(self,freq):    #freq in Hz
        self._vna.write('CENT '+str(freq))
        return

    def set_span(self,df):
        self._vna.write('SPAN '+str(df))
        return        

    def set_IFBW(self,bw):
        self._vna.write('IFBW '+str(bw))
        return        

    def set_frequencies(self,fmin,fmax):
        self._vna.write('STAR '+str(fmin))
        time.sleep(self._sleep)
        self._vna.write('STOP '+str(fmax))
        pass

    def set_scale(self,tipo='AUTO'):
        self._vna.write(tipo)
        return        

    def set_power(self,power):
        self._vna.write("POWE "+str(power))
        return

    def set_save_path(self,path):
        self._path = path
        return
 
    def set_par(self, npt=801, center=1e6, span=1e6, IFBW=100, power=-20):
        #npt = float(input('How many points?'))
        self.set_point(npt)
        time.sleep(self._sleep)
        #center = float(input('Frequency center'))
        self.set_center(center)
        time.sleep(self._sleep)
        #span = float(input('Frequency span'))
        self.set_span(span)
        self._params["span"] = span
        time.sleep(self._sleep)
        #IFBW = float(input('IFBW?'))
        self.set_IFBW(IFBW)
        self._params["IFBW"] = IFBW
        time.sleep(self._sleep)
        #power = float(input('Power (dBm)?'))
        self.set_power(power)
        self._params["power"] = power
        time.sleep(self._sleep)
        self.set_scale()
        return

    def set_data_output(self,tipo):
        self._vna.write(str(tipo))

    def output_data_format(self, format):
        if format == 'pre raw data':
            #This format is SamplerCal+Input Ratioing+Averaging
            self._vna.write('OUTPPRE') 
        elif format == 'raw data':
            self._vna.write('OUTPRAW')
        elif format == 'error correction':
            self._vna.write('OUTPCALC')
        elif format == 'error corrected':
            self._vna.write('OUTPDATA')
        elif format == 'formatted data':
            self._vna.write('OUTPFORM')
        return


    def get_data(self, format):
        self.output_data_format(format)
        data = self._vna.query()
        return data
        
    def get_data_as_dic(self):
        dtype = 'float'
        ydata = np.array(self._vna.query('OUTPDTRC?').strip().split(','))
        ydata = ydata[np.arange(int(len(ydata)/2))*2].astype(dtype)
        xdata = np.array(self._vna.query('OUTPSWPRM?').strip().split(',')).astype(dtype)
        dic = dict()
        dict.update({"ydata": ydata})
        dict.update({"xdata": xdata})
        return dic

    def get_data_as_hdf5(self, path):
        dic = self.get_data_as_dic()
        f = h5.dic_to_h5(path, dic)
        return f

    def plot_data(self):
        fig = plt.figure(figsize=(10,10))
        d = self.get_data_as_dic()
        plt.plot(d['xdata'],d['ydata'],color='k')
        plt.xlabel('$\\nu$ [GHz]')
        plt.ylabel('P [dBm]')
        plt.show()
        return

    def save_plot(self, stringa=None):
        fig = plt.figure(figsize=(10,10))
        d = self.get_data_as_dic()
        plt.plot(d['xdata'],d['ydata'],color='k')
        plt.xlabel('$\\nu$ [GHz]')
        plt.ylabel('P [dBm]')
        plt.grid(visible=True)
        plt.title(stringa)
        return fig

    def save_data_txt(self,name=None):
        save_path = ''
        if name is not None:
            save_path = name + '_'
        save_path += time.strftime("%y:%m:%d:%H:%M:%S") + '.dat'
        if self._path is not None:
            save_path = self._path + save_path
        self.get_init_par()
        lista = list(self._params.items())
        x,y = self.get_data()
        with open(save_path, "w") as f:
            for j in range(len(lista)):
                f.write("#"+str(lista[j][0])+"\t"+str(lista[j][1]))
                f.write('\n')
            f.write('\n')
            for i in range(len(y)):
                f.write(str(x[i])+"\t"+str(y[i]))
                f.write('\n')   
            f.close()
        return

    def get_init_par(self):
        npt = float(self._vna.query('POIN?').strip())
        self._params["npt"] = npt
        center = float(self._vna.query('CENT?').strip())
        self._params["center"] = center
        sweep_time = float(self._vna.query('SWET?').strip())
        self._params["sweep"] = sweep_time
        span = float(self._vna.query('SPAN?').strip())
        self._params["span"] = span
        bw = float(self._vna.query('IFBW?').strip())
        self._params["bw"] = bw
        power = float(self._vna.query('POWE?').strip())
        self._params["power"] = power
        freq_min = float(self._vna.query('STAR?').strip())
        self._params["fmin"] = freq_min
        freq_max = float(self._vna.query('STOP?').strip())  
        self._params["fmax"] = freq_max
        print("Npoints: ", npt)    
        print("Center: ", center)
        print("Sweep time: ", sweep_time)
        print("Span: ", span)
        print("IF BW: ", bw)
        print("Power: ", power)
        print("(freq_min, freq_max): ", freq_min, freq_max)   
        vec = [npt, center, sweep_time, span, bw, power, freq_min, freq_max]   
        return vec

    def find_peak(self, n_std=5):
        d = self.get_data_as_dic()
        ii, d = find_peaks(-d['ydata'],height=-np.mean(d['ydata'])+n_std*np.std(d['ydata']))
        freq = d['xdata'][ii]
        heights = d['peak_heights']
        return freq, heights
       
    def P_sweep(self):

        #Questa funzione permette di:
            #  effettuare uno scan in frequenze tra fmin e fmax
            # crea un file hdf5 ogni volta che viene rivelata una deviazione dalla media maggiore di 5 sigma 
            # per ogni picco trovato crea un gruppo che contiene i relativi dati
        path = input('Where do you want to save the upcoming files?')
        fmin = float(input('Frequency start (Hz)'))
        fmax = float(input('Frequency stop  (Hz)'))
        pn   = float(input('Frequency precision'))
        self.set_save_path(path=path)
        self.set_frequencies(fmin, fmax) 
        centers = np.arange(fmin, fmax, pn)
        count = 0
        self.set_par()
        for centroid in centers:
            self.set_par(npt=800,center=centroid,span=100,IFBW=100,power=-20)
            d = self.get_data_as_dic()
            freq_max_index = d['xdata'].index(max(d['ydata']))
            file_name = 'Scansione_1.hdf5'
            if ((max(d['ydata'])-np.mean(d['ydata']))/np.std(d['ydata']) < 3):
                count = 0
                with h5py.File(path+file_name,'w') as hf:
                    print('Start_single_measure worked!!')
                    count = count + 1
                    group_name = 'Peak'+str(count)+str(freq_max_index)
                    group_name_plt = 'Peak_plot_'+str(count)+str(freq_max_index)
                    group_1 = hf.create_group(group_name)
                    group_2 = hf.create_group(group_name_plt)
                    self.plot_data(group_name)
                    group_1.create_dataset(group_name, data=d)
                    f = self.save_plot(group_name_plt)
                    group_2.create_dataset(group_name_plt, data=f)
                    hf.close()
        return

        def IQ_meas():

            # Questa funzione serve per:
                # leggere I e Q
                # Calcolare |S21|
                # Calcolare la fase

            return I, Q

        def T_sweep():
            
            #Questa funzione serve per
                #Comunicazione con gas handler 
                #Fare uno sweep in temperatura
                #Quando la temperatura è stabile chiamo funzione 
                    #per sweep in freqeuenza
                #
            return


