#This is the original, it has to be copied in VNA_HANDLER folder
#We have to understand relative imports!

import pyvisa
import struct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvas
import numpy as np
import h5py as h5
from pathlib import Path
from Gas_Handler22 import handler
from datetime import datetime
import time


class HP8753E:

    _instance = None
    _vna = None
    _I = []
    _Q = []
    _F = []
    _T = None
    def __new__(self, board = 'GPIB0::16::INSTR', num_points = 1601 ):
        if self._instance is None:
            print('Creating the object')
            self._instance = super(HP8753E, self).__new__(self)
            self._vna = pyvisa.ResourceManager().open_resource(board)
            self._path = "C:\\Users\\kid\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRdetection\\Instruments\\Test_data\\" #saves path for data files
            self._params = {}
            self._params["start"] = 1e9
            self._params["center"] = 2e8
            self._params["span"] = 1e8
            self._params["points"] = num_points
            self._params["IFBW"] = 100
            self._params["power"] = -20
            self._params["power_start"] = -20
            self._params["power_stop"] = 0
            self._params["T"] = self._T
            self._vna.write('FORM2')
            self._vna.write('POIN ' + str(num_points)) #sets the number of points
            self._points = num_points
            self._freqs = np.zeros(num_points)
            print('VNA object created correctly!\n')
            print('Default number of points for a sweep: ' + str(self._points))
        return self._instance

    def check_status(self):
        msg = 'All is fine'
        self._vna.write('OUTPSTAT')
        _ = self._vna.read_bytes(2)
        check = self._vna.read_bytes(1)
        if check == 1:
            self._vna.write('OUTPERRO')
            msg = self._vna.read_bytes()
        return check, msg

    def set_chan(self, chan = 'S21'): #sets the channel to measure
        c = self._vna.write(chan)
        return 

    def set_mode(self, mode = 'SING'): #sets the measurement mode
        self._vna.write(mode)
        return

    def set_power_start(self, start):
        self._params['power_start'] = start

    def set_power_stop(self, stop):
        self._params['power_stop'] = stop
    
    def set_MEAS(self, net = "B"): #sets measurement
        self._vna.write('MEAS'+ net)
        return

    def ask_name(self): #returns the name of the instrument
        return self._vna.query('*IDN?')
        
    def reset(self): #presets the instrument
        self._vna.write('*RST')
        return

    def set_points(self, npt): #sets the number of points in the sweep
        self._vna.write('POIN' + str(npt))
        self._params["points"] = npt
        return

    def get_points(self):
        return self._points
    
    def set_start(self, start): #sets the start frequency to measure
        self._vna.write('STAR ' + str(start))
        self._params["start"] = start
        return

    def get_start(self):
        return self._params["start"]
    
    def set_stop(self, stop): #sets the stop frequency to measure
        self._vna.write('STOP ' + str(stop))
        self._params["stop"] = stop
        return

    def get_stop(self):
        return self._params["stop"]

    def set_center(self, center): #sets the center frequency to measure
        self._vna.write('CENT ' + str(center))
        self._params["center"] = center
        return

    def get_center(self):
        return self._params["center"]

    def set_span(self, span): #sets the span frequency
        self._vna.write('SPAN ' + str(span))
        self._params["span"] = span
        return

    def get_span(self):
        return self._params["span"]

    def set_save_path(self,path):
        self._path = path
        return

    def get_save_path(self):
        return self._path

    def set_IFBW(self, IFBW): #sets the if band width
        self._vna.write('IFBW ' + str(IFBW))
        self._params["IFBW"] = IFBW
        return

    def get_IFBW(self):
        return self._params["IFBW"]
    
    def set_power(self, power): #sets the power 
        self._vna.write('POWE ' + str(power))
        self._params["power"] = power
        return      

    def get_power(self):
        return self._params['power']

    def set_displayed_data_format(self, fmt):
        #Set the format for the displayed data 
        #(POLA, LINM, LOGM, PHAS, DELA, SMIC, SWR, REAL, IMAG)
        self._vna.write(fmt)
        self._params['data_fmt'] = str(fmt)
        return
    
    def data_outp_fmt(self, fmt):
        #Set the format by which data will be outputted by the VNA.
        #(OUTPPRE<1> ... <4>, OUTPRAW<1> ... <4>, OUTPCALC<01> ... <12>, OUTPDATA, OUTPFORM)
        self._vna.write(fmt)
        self._params['data_elab'] = str(fmt)
        return 
    
    def set_format(self, fmt):
        #Set how data will be structured.
        #(FORM1,FORM2,FORM3,FORM4,FORM5). 
        #FORM2: data are structured this way: '#A'/'numbytes'/'data' 2bytes/2bytes/8 bytes for every point
        self._vna.write(fmt)
        return

    def set_params(self, pw = -1, bw = 1e3, pt = 1601, start = 2e9, span = 1e8):
        self.set_IFBW(bw)
        self.set_points(pt)
        self.set_power(pw)
        self.set_start(start)
        self.set_span(span)
        

    def get_IQF_single_meas(self,  data_fmt = 'FORM2', out_fmt = 'OUTPRAW1'):
        #Get imaginary and real data and also the frequency they correspond to
        start = float(self._vna.query('STAR?'))
        span = float(self._vna.query('SPAN?'))
        f_n = [start + (i-1) * span/self._points  for i in range(self._points)] #Get the value corresponding frequency
        f_n = np.array(f_n)

        self._vna.write('AUTO') #auto scale the active channel
        self._vna.write('OPC?;SING;')
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

        self._I = i
        self._Q = q
        self._F = f_n
        return i, q, f_n
    
    def abs_S21(self, I, Q): #Returns S21 module 
        modS21 = []
        for i in range(len(I)):
            modS21.append(np.sqrt(pow(I[i],2) + pow(Q[i],2)))     

        return modS21     

    def phase_S21(self, I, Q): #Returns S21 phase
        phaseS21 = []
        for i in range(len(I)):
            phaseS21.append(np.arctan(Q[i]/I[i]))
        
        return phaseS21    
    
    def plot_current_S21(self, I, Q, f):
        modS21, phaseS21 = self.compute_S21(I, Q)
        
        fig, ax = plt.subplots(1,2)
        ax[0].plot(f,modS21,color='k')
        ax[0].set(xlabel='$\\nu$ [GHz]', ylabel='|S21|')
        ax[1].plot(f,phaseS21,color='k')
        ax[1].set(xlabel='$\\nu$ [GHz]', ylabel='$\Phi$')        
        return

    def plot_I(self, i, f):  #converts |S21| pyplot figure in numpy array
        fig = plt.figure(figsize=(10,8))
        plt.plot(f,i,color='k')
        plt.title('I')
        plt.xlabel('$\\nu$ [GHz]')
        #plt.ylabel('')
        canvas = FigureCanvas(fig)
        canvas.draw()
        FigArray = np.array(canvas.renderer.buffer_rgba())
        return FigArray

    def plot_Q(self,q, f):  #converts |S21| pyplot figure in numpy array
        fig = plt.figure(figsize=(10,8))
        plt.plot(f,q,color='k')
        plt.title('Q')
        plt.xlabel('$\\nu$ [GHz]')
        #plt.ylabel('')
        canvas = FigureCanvas(fig)
        canvas.draw()
        FigArray = np.array(canvas.renderer.buffer_rgba())
        return FigArray

    def plot_S21_abs(self, abs, f):  #converts |S21| pyplot figure in numpy array
        fig = plt.figure(figsize=(10,8))
        plt.plot(f,abs,color='k')
        plt.title('S21 Absolute value')
        plt.xlabel('$\\nu$ [GHz]')
        plt.ylabel('|S21|')
        canvas = FigureCanvas(fig)
        canvas.draw()
        FigArray = np.array(canvas.renderer.buffer_rgba())
        
        return FigArray

    def plot_S21_phase(self, phase, f): #converts S21 phase pyplot figure in numpy array
        fig = plt.figure(figsize=(10,8))
        plt.plot(f, phase, color='k')
        plt.title('S21 Phase')
        plt.xlabel('$\\nu$ [GHz]')
        plt.ylabel('$\Phi$')
        canvas = FigureCanvas(fig)
        canvas.draw()
        FigArray = np.array(canvas.renderer.buffer_rgba())
        return FigArray        

    def create_run_file(self, num, i, q, f):

        run = h5.File(str(self._path) + "Sample_" + str(num) + ".h5", "w")

        dati = run.create_group('raw_data')
        for key, value in self._params.items():
            dati.attrs[str(key)] = value
        dati.create_dataset('i', data= i)
        dati.create_dataset('q', data= q)
        dati.create_dataset('f', data= f)

        plots = run.create_group('plot')
        ImageDataset1 = plots.create_dataset(name="S21_abs", data = self.plot_S21_abs(self.abs_S21(i,q), f), dtype = 'uint8', chunks = True, compression = 'gzip', compression_opts = 9)
        ImageDataset1.attrs["CLASS"] = np.string_("IMAGE")
        ImageDataset1.attrs["IMAGE_VERSION"] = np.string_("1.2")
        ImageDataset1.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_TRUECOLOR")
        ImageDataset1.attrs["INTERLACE_MODE"] = np.string_("INTERLACE_MODE")
        ImageDataset1.attrs["IMAGE_MINMAXRANGE"] = np.uint8(0.255)

        ImageDataset2 = plots.create_dataset(name="S21_phase", data=self.plot_S21_phase(self.phase_S21(i,q), f), dtype = 'uint8', chunks = True, compression = 'gzip', compression_opts = 9)
        ImageDataset2.attrs["CLASS"] = np.string_("IMAGE")
        ImageDataset2.attrs["IMAGE_VERSION"] = np.string_("1.2")
        ImageDataset2.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_TRUECOLOR")
        ImageDataset2.attrs["INTERLACE_MODE"] = np.string_("INTERLACE_MODE")
        ImageDataset2.attrs["IMAGE_MINMAXRANGE"] = np.uint8(0.255)

        ImageDataset3 = plots.create_dataset(name="I", data=self.plot_I(i, f), dtype = 'uint8', chunks = True, compression = 'gzip', compression_opts = 9)
        ImageDataset3.attrs["CLASS"] = np.string_("IMAGE")
        ImageDataset3.attrs["IMAGE_VERSION"] = np.string_("1.2")
        ImageDataset3.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_TRUECOLOR")
        ImageDataset3.attrs["INTERLACE_MODE"] = np.string_("INTERLACE_MODE")
        ImageDataset3.attrs["IMAGE_MINMAXRANGE"] = np.uint8(0.255)

        ImageDataset4 = plots.create_dataset(name="Q", data=self.plot_Q(q, f), dtype = 'uint8', chunks = True, compression = 'gzip', compression_opts = 9)
        ImageDataset4.attrs["CLASS"] = np.string_("IMAGE")
        ImageDataset4.attrs["IMAGE_VERSION"] = np.string_("1.2")
        ImageDataset4.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_TRUECOLOR")
        ImageDataset4.attrs["INTERLACE_MODE"] = np.string_("INTERLACE_MODE")
        ImageDataset4.attrs["IMAGE_MINMAXRANGE"] = np.uint8(0.255)

        run.close()
        return 

    def check_T_stable(self, T, error, interval):
        
        fridge = handler.FridgeHandler()
        
        '''
            T = temperature to check 
            error = interval in which temperature value can float
            interval = seconds to sample temperature T
            We need to have a real time plot for mixing chamber temperature
            We need to have a real time plot for 1K Pot pressure
        '''
        check = True
        t0 = datetime.now() # reference time
        current = datetime.now() # current time
        temp, secs = [], []
        counter = 0
        while ((current-t0).total_seconds() < 120):
            t = float(fridge.read('R2').strip('R+'))
            sec = (current-t0).total_seconds() #seconds passed since t0
            temp.append(t)
            secs.append(sec)
            if (t-error < T or t+error>T):
                counter = counter + 1
                                
            if (counter > 4):
                msg = 'Mixing chamber temperature is out of control!'
                fridge.send_alert(msg=msg)
                check = False
                
        return check, temp, secs
    
    def T_sweep(self, T_min, T_max, N_t, error):
        
        fridge = handler.FridgeHandler()
        
        '''
            T_min = minimum temperature in mK
            T_max = maximum temperature in mK
            N_t = number of temperature samples
            error = interval in which temperature value can float
        '''
        step = (T_max - T_min)/N_t
        temps = np.arange(T_min, T_max, step=step)
        run = 0
        
        for (i,T) in enumerate(temps):
            check, temp , _  = self.check_T_stable(T, error)
            if (check==True):    
                self._params['T'] = np.mean(np.array(temp))
                run = run + 1
                I, Q, F = self.get_IQF_single_meas()
                self.create_run_file(run, i=I, q=Q, f=F)
            else:
                time.sleep(600) #If anything goes wrong go to sleep for 600 secs