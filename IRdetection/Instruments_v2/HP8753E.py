import pyvisa
import struct
import time
import matplotlib.pyplot as plt
import numpy as np
import h5_and as h5
from scipy.signal import find_peaks


class HP8753E:
    def __init__(self, board='GPIB0::16::INSTR', num_points = 1601):
        self._vna = pyvisa.ResourceManager().open_resource(board)
        self._path = None #save path for data files
        self._params = {}
        self._vna.write('FORM2')
        
        self._vna.write('POIN ' + str(num_points)) #sets the number of points
        self.points = num_points

        self.freqs = np.zeros(num_points)

        print('VNA object created correctly!\n')
        print('Default number of points for a sweep: ' + str(self.points))


    def set_NA(self,ch=1,net="B"):
        self._vna.write('CHAN' + str(ch)) #sets channel
        self._vna.write('MEAS ' + net) #sets 
        return 

    def ask_name(self): #Returns the name of the instrument
        return self._vna.query('*IDN?')
        
    def reset(self): #Presets the instrument
        self._vna.write('*RST')
        return

    def set_points(self, npt): #sets the number of points in the sweep
        self._vna.write('POIN ' + str(npt))
        self._params["points"] = npt
        return
    
    def set_start(self, start): #sets the start frequency to measure
        self._vna.write('STAR ' + str(start))
        self._params["start"] = start
        return
    
    def set_stop(self, stop): #sets the stop frequency to measure
        self._vna.write('STOP ' + str(stop))
        self._params["stop"] = stop
        return

    def set_center(self, center): #sets the center frequency to measure
        self._vna.write('CENT ' + str(center))
        self._params["center"] = center
        return

    def set_span(self, span): #sets the span frequency
        self._vna.write('SPAN ' + str(span))
        self._params["span"] = span
        return

    def set_save_path(self,path):
        self._path = path
        return

    def set_IFBW(self, IFBW): #sets the if band width
        self._vna.write('IFBW ' + str(IFBW))
        self._params["if-band-width"] = IFBW
        return
    
    def set_power(self, power): #sets the power 
        self._vna.write('POWE ' + str(power))
        self._params["power"] = power
        return      

    def set_displayed_data_format(self, fmt):
        #Set the format for the displayed data 
        #(POLA, LINM, LOGM, PHAS, DELA, SMIC, SWR, REAL, IMAG)
        self._vna.write(fmt)
        return
    
    def data_outp_fmt(self, fmt):
        #Set the format by which data will be outputted by the VNA.
        #(OUTPPRE<1> ... <4>, OUTPRAW<1> ... <4>, OUTPCALC<01> ... <12>, OUTPDATA, OUTPFORM)
        self._vna.write(fmt)
        return 
    
    def set_format(self, fmt):
        #Set how data will be structured.
        #(FORM1,FORM2,FORM3,FORM4,FORM5). 
        #FORM2: data are structured this way: '#A'/'numbytes'/'data' 2bytes/2bytes/8 bytes for every point
        self._vna.write(fmt)
        return

    def get_IQF_single_meas(self,  data_fmt = 'FORM2', out_fmt = 'OUTPRAW1', percorso=r'C:\Users\kid\SynologyDrive\Lab2023\KIDs\QTLab2324\IRdetection\Test_data'):
        #Get imaginary and real data and also the frequency they correspond to
        self.set_save_path(path=percorso)  
        start = float(self._vna.query('STAR?'))
        span = float(self._vna.query('SPAN?'))
        f_n = [start + (i-1) * span/self.points  for i in range(self.points)] #Get the value corresponding frequency
        f_n = np.array(f_n)

        self._vna.write('AUTO') #auto scale the active channel
        self._vna.write('SING')
        self._vna.write('OPC')
        self.set_format(data_fmt) #Set the data format (FORM2 is default so watch out for the header!)
        self._vna.write(out_fmt) #Write to the VNA to display structured data (OUTPFORM is default)

        _ = self._vna.read_bytes(2)
        h2 = self._vna.read_bytes(2)
        bytesnum = int.from_bytes(h2, "big")
        raw = self._vna.read_bytes(bytesnum)
        format = '>' + str(bytesnum//4) + 'f' #>  stands for big-endian number; f is for floating point type
        x = struct.unpack(format, raw) #Now...data are stored in binary code IEEE...to get them as ordinary numbers we have to use struct.unpack 
        #and as format we have to pass the correct one for FORM2 type of data

        i = np.array(x[::2])
        q = np.array(x[1::2]) #This is done becouse we know that i and q values occupy, respectively, odd and even positions
        thisdict = {"I": i, "Q":q, "F":f_n}
        h5.dic_to_h5(self._path, thisdict)
        return i, q, f_n
    
    def compute_S21(self, I, Q): #Returns S21 module and phase
        modS21 = []
        phaseS21 = []
        for i in range(len(I)):
            modS21.append(np.sqrt(np.pow(I[i],2) + np.pow(Q[i],2)))
            phaseS21.append(np.arctan(Q[i]/I[i]))
        
        return modS21, phaseS21        
    
    '''
    def plot_current_S21(self, I, Q):
        modS21, phaseS21 = self.compute_S21(I, Q)
        fmin = self._vna.query('STAR?')
        
        fig, ax = plt.subplots(1,2)
        ax[0].plot(x,modS21,color='k')
        ax[0].set(xlabel='$\\nu$ [GHz]', ylabel='|S21|')
        ax[1].plot(x,phaseS21,color='k')
        ax[1].set(xlabel='$\\nu$ [GHz]', ylabel='$\Phi$')
        plt.show()
        return
    
    def find_peak(self, n_std=5):
        d = self.get_data_as_dic()
        ii, d = find_peaks(-d['ydata'],height=-np.mean(d['ydata'])+n_std*np.std(d['ydata']))
        freq = d['xdata'][ii]
        heights = d['peak_heights']
        return freq, heights
    
    def F_sweep(self, npt=1601, ctr=2e6, sp=2e6, bw=100, pw=-20, f_min=1e6, f_max=1e9, f1='FORM2', f2='OUTPFORM'):
        #This function has to:
        #1) Make a F(frequency) sweep given a series of initial parameters
        #2) Return I,Q,F data as a hdf5 file
        self.set_par(npt=npt, center=ctr, span=sp, IFBW=bw, power=pw) #Set initial parameters
        self.set_f_range(fmin=f_min, f_max=f_max)
        start = self._vna.query('STAR')
        stop  = self._vna.query('STOP')
        freqs = list(np.arange(start, stop, self.points))
        for freq in freqs:
            I, Q, F = self.get_IQ(data_fmt=f1, out_fmt=f2)
            time.sleep(2)
            dic = {'I': I, 'Q':Q, 'F':F}
            file = h5.dic_to_h5(self._path, dic)
        return
    '''