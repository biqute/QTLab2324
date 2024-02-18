#This is the original, it has to be copied in VNA_HANDLER folder
#We have to understand relative imports!

import pyvisa
import struct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvas
import numpy as np
import h5py as h5
import sys
sys.path.insert(1, 'C://Users//kid//SynologyDrive//Lab2023//KIDs//QTLab2324//IRdetection//Instruments//Gas_Handler22')
import handler
from datetime import datetime
import pandas as pd
import time


class HP8753E:

    _instance = None
    _vna = None
    _I = []
    _Q = []
    _F = []
    _modS21 = []
    _LOGMAG = []
    _T = None
    _T_max = None
    _T_min = None
    _N_t = None
    _freqs = []
    def __new__(self, board = 'GPIB0::16::INSTR', num_points = 1601 ):
        if self._instance is None:
            print('Creating the object')
            self._instance = super(HP8753E, self).__new__(self)
            self._vna = pyvisa.ResourceManager().open_resource(board)
            self._path = "C:\\Users\\kid\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRdetection\\Instruments\\Test_data\\" #saves path for data files
            self._params = {}
            self._params["start"] = 5.2e9
            self._params["stop"] = 6e9
            self._params["center"] = 5.347e9
            self._params["span"] = 2e7
            self._params["points"] = num_points
            self._params["IFBW"] = 300
            self._params["power"] = -40
            self._params["power_start"] = -35
            self._params["power_stop"] = -20
            self._params["T"] = self._T
            self._vna.write('FORM2')
            self._vna.write('POIN ' + str(num_points)) #sets the number of points
            self._points = num_points
            self._freqs = np.zeros(num_points)
            print('VNA object created correctly!\n')
            print('Default number of points for a sweep: ' + str(self._points))
        return self._instance

    def autoscale(self):
        self._vna.write('AUTO')
        return

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

    def set_T(self, T):
        self._T = T
        return

    def set_mode(self, mode = 'CONT'): #sets the measurement mode
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

    def set_center(self, center): #sets the center frequency to measure
        self._vna.write('CENT ' + str(center))
        self._params["center"] = center
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
        #Sets the format for the displayed data 
        #(POLA, LINM, LOGM, PHAS, DELA, SMIC, SWR, REAL, IMAG)
        self._vna.write(fmt)
        self._params['data_fmt'] = str(fmt)
        return
    
    def data_outp_fmt(self, fmt):
        #Sets the format by which data will be outputted by the VNA.
        #(OUTPPRE<1> ... <4>, OUTPRAW<1> ... <4>, OUTPCALC<01> ... <12>, OUTPDATA, OUTPFORM)
        self._vna.write(fmt)
        self._params['data_elab'] = str(fmt)
        return 
    
    def set_format(self, fmt):
        #Sets how data will be structured.
        #(FORM1,FORM2,FORM3,FORM4,FORM5). 
        #FORM2: data are structured this way: '#A'/'numbytes'/'data' 2bytes/2bytes/8 bytes for every point
        self._vna.write(fmt)
        return

    def set_params(self, pw = -40, bw = 300, pt = 1601, center = 5.34e9, span = 2e7): 
        self.set_IFBW(bw)
        self.set_points(pt)
        self.set_power(pw)
        self.set_center(center)
        self.set_span(span)

    def get_IQF_center(self, data_fmt = 'FORM2', out_fmt = 'OUTPRAW1'):

        span = self._params['span']
        start = self._params['center'] - span/2

        f_n = [start + (i-1) * span/self._points  for i in range(self._points)] #Get the value corresponding frequency
        f_n = np.array(f_n)
        self._vna.write('AUTO') #auto scale the active channel
        self._vna.write('OPC?;SING;')
        self.set_format(data_fmt) #Sets the data format (FORM2 is default so watch out for the header!)
        self._vna.write(out_fmt) #Writes to the VNA to display structured data (OUTPFORM is default)
        _ = self._vna.read_bytes(2)
        h2 = self._vna.read_bytes(2)
        bytesnum = int.from_bytes(h2, "big")
        raw = self._vna.read_bytes(bytesnum)
        format = '>' + str(bytesnum//4) + 'f' #>  stands for big-endian number; f is for floating point type
        x = struct.unpack(format, raw) #Now...data are stored in binary code IEEE...to get them as ordinary numbers we have to use struct.unpack 
        #and as format we have to pass the correct one for FORM2 type of data

        i = np.array(x[::2])
        q = np.array(x[1::2]) #This is done becouse we know that i and q values occupy respectively, odd and even positions

        self._I = i
        self._Q = q
        self._F = f_n
        return i, q, f_n

    def get_S21F(self, data_fmt = 'FORM2', out_fmt = 'OUTPFORM'):

        span = self._params['span']
        start = self._params['center'] - span/2
        self.set_displayed_data_format('LOGM')

        f_n = [start + (i-1) * span/self._points  for i in range(self._points)] #Get the value corresponding frequency
        f_n = np.array(f_n)

        try:
            self._vna.write('AUTO') #auto scale the active channel
            self._vna.write('OPC?;SING;')
        except:
            print('Problema con self._vna.write(SING)!! Riprovo...')
            self.set_params(pw=self._params['power'], bw=self._params['IFBW']-100, pt=self._params['points'], center=self._params['center'], span=self._params['span'])
            time.sleep(3)

        self.set_format(data_fmt) #Sets the data format (FORM2 is default so watch out for the header!)
        self._vna.write(out_fmt) #Writes to the VNA to display structured data (OUTPFORM is default)
        _ = self._vna.read_bytes(2)
        h2 = self._vna.read_bytes(2)
        bytesnum = int.from_bytes(h2, "big")
        raw = self._vna.read_bytes(bytesnum)
        format = '>' + str(bytesnum//4) + 'f' #>  stands for big-endian number; f is for floating point type
        x = struct.unpack(format, raw) #Now...data are stored in binary code IEEE...to get them as ordinary numbers we have to use struct.unpack 
        #and as format we have to pass the correct one for FORM2 type of data

        self._modS21 = np.array(x[::2])
        self._F = f_n
        
        return self._modS21, f_n


    def get_IQF_single_meas(self,  data_fmt = 'FORM2', out_fmt = 'OUTPFORM'):
        #Gets imaginary and real data and also the frequency they correspond to
        start = self._params['start']
        span = self._params['span']
        f_n = [start + (i-1) * span/self._points  for i in range(self._points)] #Get the value corresponding frequency
        f_n = np.array(f_n)

        self._vna.write('AUTO') #auto scale the active channel
        self._vna.write('OPC?;SING;')
        self.set_format(data_fmt) #Sets the data format (FORM2 is default so watch out for the header!)
        self._vna.write(out_fmt) #Writes to the VNA to display structured data (OUTPFORM is default)

        _ = self._vna.read_bytes(2)
        h2 = self._vna.read_bytes(2)
        bytesnum = int.from_bytes(h2, "big")
        raw = self._vna.read_bytes(bytesnum)
        format = '>' + str(bytesnum//4) + 'f' #>  stands for big-endian number; f is for floating point type
        x = struct.unpack(format, raw) #Now...data are stored in binary code IEEE...to get them as ordinary numbers we have to use struct.unpack 
        #and as format we have to pass the correct one for FORM2 type of data

        i = np.array(x[::2])
        q = np.array(x[1::2]) #This is done becouse we know that i and q values occupy respectively, odd and even positions

        self._I = i
        self._Q = q
        self._F = f_n
        return i, q, f_n
    
    def abs_S21(self, I, Q): #Returns S21 module 
        I = np.array(I)
        Q = np.array(Q)
        return 20*np.log10(np.sqrt(I**2 + Q**2))   

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
        plt.close()        
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
        plt.close()
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
        plt.close()
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
        plt.close()        
        return FigArray

    def plot_S21(self, s21, f):  #converts |S21| pyplot figure in numpy array
        fig = plt.figure(figsize=(10,8))
        plt.plot(f,s21,color='k')
        plt.title('S21 Absolute value')
        plt.xlabel('$\\nu$ [GHz]')
        plt.ylabel('|S21|')
        canvas = FigureCanvas(fig)
        canvas.draw()
        FigArray = np.array(canvas.renderer.buffer_rgba())
        plt.close()        
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
        plt.close()
        return FigArray        

    def create_run_s21(self, num, s21, f):

        with h5.File(str(self._path) + "S21_" + str(num) + ".hdf5", "w") as run:

            dati = run.create_group('raw_data')
            for key, value in self._params.items():
                if (value is None):
                    dati.attrs[str(key)] = 0
                elif (type(value)==str):
                    dati.attrs[str(key)] = value
                else:
                    dati.attrs[str(key)] = float(value)

            dati.create_dataset('S21', data= np.array(s21))
            dati.create_dataset('f', data= np.array(f))

            plots = run.create_group('plot')
            ImageDataset1 = plots.create_dataset(name="S21_abs", data = self.plot_S21(s21, f), dtype = 'uint8', chunks = True, compression = 'gzip', compression_opts = 9)
            ImageDataset1.attrs["CLASS"] = np.string_("IMAGE")
            ImageDataset1.attrs["IMAGE_VERSION"] = np.string_("1.2")
            ImageDataset1.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_TRUECOLOR")
            ImageDataset1.attrs["INTERLACE_MODE"] = np.string_("INTERLACE_MODE")
            ImageDataset1.attrs["IMAGE_MINMAXRANGE"] = np.uint8(0.255)

        run.close()
        return 

    def create_run_file(self, num, i, q, f):

        with h5.File(str(self._path) + "Sample_" + str(num) + ".h5", "w") as run:

            dati = run.create_group('raw_data')
            for key, value in self._params.items():
                if (value is None):
                    dati.attrs[str(key)] = 0
                else:
                    dati.attrs[str(key)] = float(value)

            dati.create_dataset('i', data= np.array(i))
            dati.create_dataset('q', data= np.array(q))
            dati.create_dataset('f', data= np.array(f))

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
    
    def check_stability(self, window, disc):
        check = False
        fridge = handler.FridgeHandler()
        fig, ax = plt.subplots(1, 2, figsize=(10,5))

        data = []
        mav = []

        for i in range(10):
            time.sleep(1.5)
            data.append(fridge.read('R32'))

        counter = 0
        count = 0
        mav = [np.mean(data)]
        while(counter < disc):
            value = fridge.read('R32')
            if (data[-1] - value)<10:
                count = count + 1
                data.pop(0)
                data.append(value)
                mav.append(np.mean(data))

                ax[0].scatter(count, value, color='black', s=1, marker='o', label='raw data')
                ax[1].scatter(count, np.mean(data), color='red', s=1,  marker='x', label='moving average')
                ax[0].set_xlim([count-window,count])
                ax[1].set_xlim([count-window,count])
                ax[0].set_xlabel('cycle unit')
                ax[0].set_ylabel('raw data')
                ax[1].set_xlabel('cycle unit')
                ax[1].set_ylabel('moving average')
                plt.pause(0.01)
                time.sleep(2.5)

                if ((mav[count]-mav[count-1])<np.std(data)):
                        counter += 1
                check = True
        return check, mav, data

    def check_stable(self, temp, secs, average, fig, ax):

        check = True
        fridge = handler.FridgeHandler()
        window = 50 # Temperature samples for computing moving average
        count = window
        value = float(fridge.read('R2'))
        temp.append(value)
        temp.pop(0)
        av = np.mean(temp)
        average.append(av)
        count += 1
        secs.append(count)
        secs.pop(0)
        ax.scatter(secs, temp, color='black', s=1, marker='o', label='raw data')
        ax.scatter(count, av, color='red', marker='x', s=1, label='moving average')
        ax.set_xlim([count-window,count])
        plt.pause(0.05)
        if (abs(average[count-window]-average[count-1-window]) > 1):
            check = False
            return False
        plt.legend()
        plt.show()
        return check

    
    def set_T_max(self, tmax):
        self._T_max = tmax
        
    def set_T_min(self, tmin):
        self._T_min = tmin
        
    def set_N_t(self, n):
        self._N_t = n
    
    def T_sweep(self):
        
        fridge = handler.FridgeHandler()
        
        '''
            T_min = minimum temperature in mK
            T_max = maximum temperature in mK
            N_t = number of temperature samples
            error = interval in which temperature value can float
        '''
        self.set_save_path("C:\\Users\\kid\\SynologyDrive\\Lab2023\\KIDs\\QTLab2324\\IRdetection\\Instruments\\Test_data\\Temp-sweep\\")
        step = int((self._T_max - self._T_min)/self._N_t)
        temps = np.arange(self._T_min, self._T_max, step=step)
        run = 0
        
        for T in temps:
            fridge.set_mixc_temp(T)
            check, temp, secs, average = self.check_stability(50,20)
            if (check==True and fridge.check_press()==True):  
                self._params['T'] = T
                run = run + 1
                fig = plt.figure()
                ax = fig.add_subplot()
                while(self.check_stable(temp, secs, average, fig, ax)==True):    
                    for f in self._freqs:
                        self.set_start(f - self.params['span']/2)
                        I, Q, F = self.get_IQF_single_meas()
                        self.create_run_file(str(run)+"_"+str(f), i=I, q=Q, f=F)
            else: fridge.send_alert()
        return 