import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import tkinter
from scipy.signal import find_peaks
import h5_and.py as h5

class HP8753E():

    def __init__(self,name='GPIB0::16::INSTR'):
        resources = pyvisa.ResourceManager('@py')
        self._vna = resources.open_resource(name)
        self._sleep = 0.5     #sleep between commands
        self._path = None     #save path for data files
        self._params = {}
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

    def set_NA(self,ch="1",net="B",sweep_type = "CONT"):
        self._vna.write('CHAN'+ch)
        time.sleep(self._sleep)
        self._vna.write('NA')
        time.sleep(self._sleep)
        self._vna.write('MEAS '+net)
        time.sleep(self._sleep)
        self._vna.write(sweep_type) #set continuous sweep
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
        self._vna.write('BW '+str(bw))
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

    def start_single_measure(self,npt=800,center=5e6,span=100,IFBW=300,power=-20):
        self.set_point(npt)
        time.sleep(self._sleep)
        self.set_center(center)
        time.sleep(self._sleep)
        self.set_span(span)
        self._params["span"] = span
        time.sleep(self._sleep)
        self.set_IFBW(IFBW)
        self._params["IFBW"] = IFBW
        time.sleep(self._sleep)
        self.set_power(power)
        self._params["power"] = power
        time.sleep(self._sleep)
        self.set_scale()
        return

    def get_data(self):
        dtype = 'float'
        ydata = self._vna.query('OUTPDTRC?').strip().split(',')
        ydata = np.array(ydata)
        ydata = ydata[np.arange(int(len(ydata)/2))*2].astype(dtype) #FIXME?
        xdata = self._vna.query('OUTPSWPRM?').strip().split(',')
        xdata = np.array(xdata).astype(dtype)
        return xdata, ydata
        
    def get_data_as_dic(self):
        dtype = 'float'
        ydata = np.array(self._vna.query('OUTPDTRC?').strip().split(','))
        ydata = ydata[np.arange(int(len(ydata)/2))*2].astype(dtype)
        xdata = np.array(self._vna.query('OUTPSWPRM?').strip().split(',')).astype(dtype)
        dic = dict()
        dict.update({"ydata": ydata})
        dict.update({"xdata": xdata})
        return dic

    def get_data_as_hdf5(self):
        dic = self.get_data_as_dic()
        f = h5.dic_to_h5()
        return f

    def plot_data(self):
        x,y = self.get_data()
        plt.plot(x,y,color='k')
        plt.show()
        return

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
        bw = float(self._vna.query('BW?').strip())
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
        return npt, center, sweep_time, span, bw, power, freq_min, freq_max

    def find_peak(self, n_std=5):
        x, y = self.get_data()
        ii, dic = find_peaks(-y,height=-np.mean(y)+n_std*np.std(y))
        freq = x[ii]
        heights = dic['peak_heights']
        return freq, heights
       
    def routine(self):
        centers = np.arange(1.5e6,14e6, 0.01e6)
        count = 0;
        for i in centers:
            self.start_single_measure(npt=800,center=i,span=8000,IFBW=300,power=-20)
            freq, heights = find_peak()
            if (freq.size() > 0):
                count  = count + 1
                x,y = self.get_data()
                save_data_txt('Peak'+str(count));
                freq_max_index = freq.index(max(heights))
                start_single_measure(npt=800,center=i,span=100,IFBW=100,power=-20)
                new_center = freq(freq_max_index)    
                save_data_txt('Zommed_peak'+str(count))
                plot_data('Zommed_peak'+str(count))
        return

