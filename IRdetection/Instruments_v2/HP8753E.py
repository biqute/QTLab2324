import pyvisa
import struct
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
#from myhdf5 import h5_and as h5
#import h5py

'''
Structs converts between Python values and C structs serialized 
into Python bytes objects. For example, it can be used to 
handle binary data stored in files or coming in from network connections.
'''

class HP8753E:
    def __init__(self, board='GPIB0::16::INSTR', num_points = 1601):
        self._vna = pyvisa.ResourceManager().open_resource(board)
        self._sleep = 0.5     #sleep between commands
        self._path = None     #save path for data files
        self._params = {}
        self._vna.write('FORM2;')
        '''
            IEEE 32-bit floating-point format, 8 bytes-per-data
            point. The data is preceded by a 4 bit header.
            Each number consists of a l-bit sign, an
            &bit biased exponent, and a 23-bit mantissa. FORM2
            is the format of choice if your computer supports
            single-precision floating-point numbers
        '''
        self._vna.write('CHAN1') 
        '''What channel are we looking into?'''
        self._vna.write('S21;')
        '''What S matrix coefficient are we looking for?'''
        self._vna.write('POIN '+ str(num_points)+';')        
        '''set number of points'''

        self.points = num_points

        self.freqs = np.zeros(num_points)

        print('VNA object created correctly!\n')
        print('Default number of points for a sweep: ' + str(self.points))

    def ask_name_read_oat(self):
        '''Reading bytes one at a time, if the instrument times out at
        the first char, then it did not respond'''
        self._vna.write('*IDN?')
        while True:
            print(self._vna.read_bytes(1))
        return

    def ask_name(self):
        '''Who am I?'''
        self._vna.query('*IDN?')
        return

    def reset(self):
        self._vna.write('*RST')
        return

    def set_sleep(self,time):
        self._sleep = time
        return  

    def set_NA(self,ch="1",net="B",sweep_type = "CONT"):
        self._vna.write('CHAN'+ch) #set channel
        time.sleep(self._sleep)
        self._vna.write('MEAS '+net) #set 
        time.sleep(self._sleep)
        self._vna.write(sweep_type) #set continuous sweep mode
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
    
    def set_scale(self,tipo='AUTO'):
        self._vna.write(tipo)
        return        

    def set_power(self,power):
        self._vna.write("POWE "+str(power))
        return

    def set_save_path(self,path):
        self._path = path
        return
    
    def set_par(self):
        npt = input('How many points?')
        self.set_point(npt)
        time.sleep(self._sleep)
        center = input('Frequency center')
        self.set_center(center)
        time.sleep(self._sleep)
        span = input('Frequency span')
        self.set_span(span)
        self._params["span"] = span
        time.sleep(self._sleep)
        IFBW = input('IFBW?')
        self.set_IFBW(IFBW)
        self._params["IFBW"] = IFBW
        time.sleep(self._sleep)
        power = input('Power (dBm)?')
        self.set_power(power)
        self._params["power"] = power
        time.sleep(self._sleep)
        self.set_scale()
        return

    def set_f_range(self, f_min, f_max):
        ''''Set the range of frequencies for the next scan from start_f to stop_f'''
        self._vna.write('LINFREQ;')
        self._vna.write('STAR '+str(f_min)+' GHZ;')  #Start freq in GHz
        self._vna.write('STOP '+str(f_max)+' GHZ;')  #Stop  freq in GHz
        self._vna.write('CONT;')
        self.freqs = np.linspace(f_min, f_max, self.points)

    def set_cdt_type(self, fmt):
        ''' Set the format for the displayed data 
        (POLA, LINM, LOGM, PHAS, DELA, SMIC, SWR, REAL, IMAG)
        '''
        self._vna.write(fmt)
    
    def data_outp_fmt(self, fmt):
        '''
        Set the format by which data will be outputted by the VNA.
        (OUTPPRE, OUTPRAW, OUTPDATA, )
        '''
        self.vna.write(fmt)


    def get_IQ(self, data_fmt = 'FORM2', out_fmt = 'formatted data'):
        '''Get data'''

        self.set_format(data_fmt)
        self.output_data_format(out_fmt)
        
        num_bytes = 8*int(int(float(self.points)))+4
        #time.sleep(2)
        raw_bytes = self._vna.read_bytes(num_bytes)
        #This method will read at most the number of bytes specified.
        trimmed_bytes = raw_bytes[4:]
        #We are not interested in the header!
        format = '>' + str(2*int(float(self.points))) + 'f'
        x = struct.unpack(format, trimmed_bytes)
        '''Returns a tuple maybe we can try to not trim bytes using
        x = struct.unpack_from(format, /, buffer=raw_bytes, offset=4)
        '''

        amp_q = list(x)
        amp_i = amp_q.copy()

        '''Creates a copy of amp_i'''

        del amp_i[1::2]
        del amp_q[0::2]
        '''Slycing operation;
        1=Start index
        :: = Every second element
        2=Stop index
        This is done becouse we assume that i and q values occupy
        respectively odd and even positions
        '''
        i = list(amp_i)
        q = list(amp_q)

        return i, q
    
    def compute_S21(self, I, Q):
        '''Returns S21 module and phase'''
        modS21 = []
        phaseS21 = []
        for i in range(len(I)):
            modS21.append(np.sqrt(np.pow(I[i],2) + np.pow(Q[i],2)))
            phaseS21.append(np.arctan(Q[i]/I[i]))
        
        return modS21, phaseS21        
    
    def plot_current_S21(self, I, Q):
        modS21, phaseS21 = self.compute_S21(I, Q)
        fmin = self._vna.query('STAR?')
        fmax = self._vna.query('STOP?')
        passo = (fmax-fmin)/self.points
        x = list(np.arange(fmin, fmax, passo))
        fig, ax = plt.subplots(1,2)
        ax[0].plot(x,modS21,color='k')
        ax[0].set(xlabel='$\\nu$ [GHz]', ylabel='|S21|')
        ax[1].plot(x,phaseS21,color='k')
        ax[1].set(xlabel='$\\nu$ [GHz]', ylabel='$\Phi$')
        plt.show()
        return
'''
    def find_peak(self, n_std=5):
        d = self.get_data_as_dic()
        ii, d = find_peaks(-d['ydata'],height=-np.mean(d['ydata'])+n_std*np.std(d['ydata']))
        freq = d['xdata'][ii]
        heights = d['peak_heights']
        return freq, heights
        
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

    def power_sweep(self):
        path = input('Where do you want to save the upcoming files?')
        fmin = input('Frequency start (Hz)') 
        fmax = input('Frequency stop  (Hz)')
        pn   = input('Frequency precision')
        self.set_save_path(path=path)
        self.set_frequencies(fmin, fmax) 
        centers = np.arange(fmin, fmax, pn)
        count = 0
        self.set_par()
        for centroid in centers:
            self.start_single_measure(npt=800,center=centroid,span=100,IFBW=100,power=-20)
            d = self.get_data_as_dic()
            freq_max_index = d['xdata'].index(max(d['ydata']))
            file_name = 'Scansione_1.hdf5'
            if ((max(d['ydata'])-np.mean(d['ydata']))/np.std(d['ydata']) < 3):
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
'''
