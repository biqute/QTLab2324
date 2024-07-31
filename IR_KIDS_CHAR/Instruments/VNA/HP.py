import pyvisa
import numpy as np
import struct


class HP:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource("GPIB0::16::INSTR")       

        #self.inst.write("HOLD;")        #takes instrument out of free-run mode
        self.inst.write("FORM2;")        #outputs number in 4bytes mode (float?) with 4-byte header

        self.inst.write("S21;")

        self.inst.write("AVERFACT16;")       #turns on sample averaging
        self.inst.write("AVEROON;")       #turns on sample averaging
        self.inst.write("AVERREST;")       #turns on sample averaging
        self.inst.write("IFBW1000;")

    def autoscale(self):
        self.inst.write("AUTO;")

    def set_elec_delay(self,delay):
        self.inst.write("ELED["+str(delay)+"];")

    def check_status(self):
        msg = "All is fine"
        self.inst.write("OUTPSTAT;")
        _ = self.inst.read_bytes(2)
        check = self.inst.read_bytes(1)
        if check == 1:
            self.inst.write("OUTPERRO;")
            msg = self.inst.read_bytes()
        return check, msg

    def set_IFBW(self, bw):
        self.inst.write("IFBW"+str(bw)+";")

    def set_sweep_mode(self, mode="LINFREQ"):
        #LINFREQ,LOGFREQ,LISFREQ
        self.inst.write(str(mode)+";")

    def set_chan(self, chan = "S21"): #sets the channel to measure
        self.inst.write(chan+";")
        return 

    def set_mode(self, mode = "CONT"): #sets the measurement mode
        self.inst.write(mode+";")
        return
    
    def set_meas(self, net = "B"): #sets measurement
        self.inst.write("MEAS"+ net + ";")
        return

    def ask_name(self): #returns the name of the instrument
        return self.inst.query("*IDN?")
        
    def reset(self): #presets the instrument
        self.inst.write("*RST")
        return

    def set_center(self, center): #sets the center frequency to measure
        self.inst.write("CENT " + str(center))
        return

    def set_points(self, npt): #sets the number of points in the sweep
        self.inst.write("POIN " + str(npt)+";")
        return

    def get_points(self):
        return self.inst.query("POIN?")
    
    def set_start(self, start): #sets the start frequency to measure
        self.inst.write("STAR " + str(start)+";")
        return

    def get_start(self):
        self.inst.query("STAR?;")       #set start frequency
    
    def set_stop(self, stop): #sets the stop frequency to measure
        self.inst.write("STOP "+str(stop)+" GHZ;")        #set stop frequency
        return

    def get_stop(self):
        return self.inst.query("STOP?;")

    def get_center(self):
        return self.inst.query("CENT?;")

    def set_span(self, span): #sets the span frequency
        self.inst.write("SPAN " + str(int(span)))+" MHZ;"
        return

    def get_span(self):
        return self.inst.query("SPAN?;")

    def set_average(self, status):
        self.inst.write("AVERO"+str(status)+"ON;")

    def set_average_fact(self, factor):
        self.inst.write("AVERFACT"+str(factor)+";")

    def set_smoothing(self, status):
        self.inst.write("SMOOO"+str(status)+"ON;")

    def set_smoothing_fact(self, status):
        self.inst.write("SMOOAPER"+str(status)+";")

    def set_sweep_freq(self, start_f,stop_f):
        self.set_sweep_mode()
        self.set_points(1601)
        self.set_start(start_f)
        self.set_stop(stop_f)
        self.set_mode()                       #set number of points

    def set_sweep_center(self, center,span):
        self.set_sweep_mode()
        self.set_points(1601)
        self.set_center(center)
        self.set_span(span)
        self.set_mode()

    def get_request_from_format_out(self, format):
        if format == "raw data array 1":
            msg = "OUTPRAW1;"
        elif format == "raw data array 2":
            msg = "OUTPRAW2;"
        elif format == "raw data array 3":
            msg = "OUTPRAW3;"
        elif format == "raw data array 4":
            msg = "OUTPRAW4;"
        elif format == "error-corrected data":
            msg = "OUTPDATA;"
        elif format == "error-corrected trace memory":
            msg = "OUTPMEMO;"
        elif format == "formatted data":
            msg = "DISPDATA;OUTPFORM"
        elif format == "formatted memory":
            msg = "DISPMEMO;OUTPFORM"
        elif format == "formatted data/memory":
            msg = "DISPDDM;OUTPFORM"
        elif format == "formatted data-memory":
            msg = "DISPDMM;OUTPFORM"
        return msg

    def set_data_format(self, format):
        fmt = self.get_request_from_format_out(format)
        self.inst.write(str(fmt)+";")

    def set_format(self, format):
        if format == "polar":
            write_string = "POLA;"
        elif format == "log magnitude":
            write_string = "LOGM;"
        elif format == "phase":
            write_string = "PHAS;"
        elif format == "delay":
            write_string = "DELA;"
        elif format == "smith chart":
            write_string = "SMIC;"
        elif format == "linear magnitude":
            write_string = "LINM;"
        elif format == "standing wave ratio":
            write_string = "SWR;"
        elif format == "real":
            write_string = "REAL;"
        elif format == "imaginary":
            write_string = "IMAG;"

        self.inst.write(write_string)

    def get_IQF_center(self, span, start, data_fmt = 'FORM2', out_fmt = 'OUTPRAW1'):

        self.set_span(span)
        self.set_start(start)
        f_n = [start + (i-1) * span/self._points  for i in range(self._points)] #Get the value corresponding frequency
        f_n = np.array(f_n)
        self.inst.write('AUTO') #auto scale the active channel
        self.inst.write('OPC?;SING;')
        self.set_format(data_fmt) #Sets the data format (FORM2 is default so watch out for the header!)
        self.inst.write(out_fmt) #Writes to the VNA to display structured data (OUTPFORM is default)
        _ = self.inst.read_bytes(2)
        h2 = self.inst.read_bytes(2)
        bytesnum = int.from_bytes(h2, "big")
        raw = self.inst.read_bytes(bytesnum)
        format = '>' + str(bytesnum//4) + 'f' #>  stands for big-endian number; f is for floating point type
        x = struct.unpack(format, raw) #Now...data are stored in binary code IEEE...to get them as ordinary numbers we have to use struct.unpack 
        #and as format we have to pass the correct one for FORM2 type of data

        i = np.array(x[::2])
        q = np.array(x[1::2]) #This is done becouse we know that i and q values occupy respectively, odd and even positions

        self._I = i
        self._Q = q
        self._F = f_n
        return i, q, f_n

    def get_sweep_data(self):

        self.set_mode("SING")
        num_points = 1061
        self.inst.write("OUTPRAW1;")
        num_bytes = 8*int(num_points)+4
        raw_bytes = self.inst.read_bytes(num_bytes)

        #print(raw_bytes)

        trimmed_bytes = raw_bytes[4:]
        tipo=">"+str(2*num_points)+"f"
        x = struct.unpack(tipo, trimmed_bytes)
        #x.byteswap()
        
        #del x[1::2]
        return list(x)

    def save_sweep_data(self, filename, format_data="linear magnitude"):
        amp_q = self.get_sweep_data(format_data)
        amp_i = amp_q.copy()
        del amp_i[1::2]
        del amp_q[0::2]

        self.inst.write("STAR?")
        start = float(self.inst.read("\n"))
        self.inst.write("STOP?")
        stop = float(self.inst.read("\n"))
        self.inst.write("POIN?")
        num_points = int(float(self.inst.read("\n")))

        freq = list(np.linspace(start, stop, num_points))
        del freq[0]

        zipped_data = zip(freq, amp_i, amp_q)

        with open(filename, "w") as file:
            for el in zipped_data:
                file.write(f"{el[0]},\t{el[1]},\t{el[2]}\n")