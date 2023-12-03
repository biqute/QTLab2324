import pyvisa
import struct
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import h5_and as h5
#from myhdf5 import h5_and as h5
#import h5py

'''
Structs converts between Python values and C structs serialized 
into Python bytes objects. For example, it can be used to 
handle binary data stored in files or coming in from network connections.
'''

class HP9753E:
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
        self._vna.write('CHAN1;') 
        '''What channel are we looking into?'''
        self._vna.write('S21;')
        '''What S matrix coefficient are we looking for?'''
        self._vna.write('POIN '+ str(num_points)+';')        
        '''set number of points'''

        self.points = num_points

        self.freqs = np.zeros(num_points)

        print('VNA object created correctly!\n')
        print('Default number of points for a sweep: ' + str(self.points))

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
    
    def set_par(self, npt, center, span, IFBW, power):
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
        (OUTPPRE, OUTPRAW, OUTPCALC, OUTPDATA, OUTPFORM)
        '''
        self.vna.write(fmt)
    
    def set_format(self, fmt):
        '''
        Set how data will be structured.
        (FORM1,FORM2,FORM3,FORM4,FORM5)
        FORM2: data are structured this way:
            '#A'/'numbytes'/'data'
            2bytes/2bytes/8 bytes for every point
        '''
        self._vna.write(fmt)


    def get_IQF(self, data_fmt = 'FORM2', out_fmt = 'OUTPFORM'):
        '''Get imaginary and real data and also the frequency they correspond to.'''

        self.set_format(data_fmt+';')                       #Set the data format (FORM2 is default so watch out for the header!)
        self.output_data_format('DISPDATA;'+out_fmt+';')    #Write to the VNA to display structured data (OUTPFORM is default),
                                                            #This has to be done after the frequency sweep is completed...how can we know?
        t = int(1/self._vna.query('IFBW'))*self.points + 2  #Time required for frequency sweep
        time.sleep(t)
        start = self._vna.query('STAR')
        span = self._vna.query('SPAN')
        f_n = [(start + (i-1) * span/(i-1))  for i in range(self.points)] #Get the value corresponding frequency

        #Now we begin to read the header
        ftb = self._vna.read_bytes(2)                       #First two bytes #A
        try:
            ('#' in ftb)
        except: 
            print('# is not in the file!', ftb)

        bytes_num = self._vna.read_bytes(2)                 #Second two bytes (number of bytes stored in the VNA's buffer)
        try:
            bytes_num is int
        except:
            print('Second two bytes do not represent an integer!', bytes_num)
        
        raw_bytes = self._vna.read_bytes(bytes_num)

        #This method will read at most the number of bytes specified. Returns a byte class object see
        #https://docs.python.org/3/library/stdtypes.html#bytes documentation

        no_header = raw_bytes[4:] #We are not interested in the header!
        #Now...data are stored in binary code IEEE...to get them as ordinary numbers we have to use struct.unpack
        #and as format we have to pass the correct one for FORM2 type of data

        format = '>' + str(bytes_num) + 'f'
        #>  stands for big-endian number
        #f is for floating point type
        x = struct.unpack(format, no_header)

        q = list(x)
        i = q.copy()

        '''Creates a copy of amp_i'''

        del i[1::2]
        del q[0::2]
        '''Slycing operation;
        1=Start index
        :: = Every second element
        2=Stop index
        This is done becouse we assume that i and q values occupy
        respectively odd and even positions
        '''
        return i, q, f_n
    
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
        '''This function has to:
            1) Make a F(frequency) sweep given a series of initial parameters
            2) Return I,Q,F data as a hdf5 file
        '''
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