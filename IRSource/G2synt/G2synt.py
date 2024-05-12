import numpy as np
import serial
import time


## serial version
class synt(object):
    #uses serial class to interface
    #All functions here use commands which must be sent as STRINGS encoded as BYTES 
    #b'str' encodes 'str' into bytes; bytes(str) encodes variable str into bytes
    
    #all string commands are SCPI commands as per "Communication Specs for Programming" manual
    
    #Find manual at http://ni-microwavecomponents.com/quicksyn-lite#documentation
    #Find manual in My Drive > manuals and datasheets > "Quicksyn - FSL0010 synthesizer - programming manual"
    
    def __init__(self,device_address='COM31'):
        self.device = serial.Serial(device_address, baudrate=115200, timeout=1.5, stopbits=1, parity='N') 
    
    #general commands (internal use only)
    def write(self,msg_string): #general set function
        self.device.write(bytes(msg_string))
        return True
    def read(self): #shorter read syntax for get function
        return self.device.readline().decode() #removes byte encoding syntax
    def ask(self,msg_string): #general get function
        self.write(msg_string) #takes an already encoded string
        return self.read()
    
    #specific commands
    def get_frequency(self):
        #print(self.ask(b'FREQ?\r'))
        f = self.ask(b'FREQ?\r') #hard coded encoded command string
        return f
    def set_frequency(self,freq):  # default units in GHz
        cmd_string = 'FREQ ' + str(freq) + 'GHz\r'
        self.write(str.encode(cmd_string))    # this converts a string to bytes
        return "Frequency set to "+str(freq)+" GHz."

    def get_temp(self):
        return (self.ask(b'DIAG:MEAS? 21\r')).strip() + ' °C' #command as per manual spec  
        
    def get_ref_source(self): #device needs a ref source for frequency calibration
         #returns "EXT" for external ref source (REF IN pin)
         #returns "INT" for internal ref source (built in clock)
        return 'Ref source: '+self.ask(b'ROSC:SOUR?\r')
    def set_ref_source(self, source):
        #as above: ref source can only be EXT (external) or INT internal
        if (not (source == "EXT" or source == "INT")):
            return "Invalid entry. Ref source must be set to EXT or IN"
        else:
            cmd_string = str.encode('ROSC:SOUR  ' + (source))
            self.write(cmd_string) #send command to set ref source
            return "Ref source set to "+source
    
    '''def set_ref_out(self, set):
        #set ref out (REF OUT pin) to ON or OFF
        if (not (set == "ON" or set == "OFF")):
            return "Invalid entry. Ref out may only be set to ON or OFF"
        else:
            cmd_string = str.encode('OUTP:ROSC:STAT ' + (source))
            self.write(cmd_string) #send command to turn ref out on or off
            return "Ref out set to "+set'''
    def get_ref_out(self):
         #returns ON or OFF
        return 'Ref out: '+self.ask(b'OUTP:ROSC:STAT?\r')
        
    def set_output(self, set):
        #turn RF output ON or OFF (TURN DEVICE ON OR OFF)
        if (not (set == "ON" or set == "OFF")):
            return "Invalid entry. Ref out may only be set to ON or OFF"
        else:
            if set == "ON":
                self.write(b'0F01')
            elif set == "OFF":
                self.write(b'0F00')
            return "RF set to "+set
    def get_output(self):
        #get RF status
        #returns 1 (ON) or 0 (OFF)
        return 'RF '+(self.ask(b'0x02'))
    
    def getID(self):
        #gets built in device ID; make and model
        #will return 'Phase Matrix,FSL-0010,0000007f,1520201055,b01d
        return self.ask(b'*IDN?\r')
    
    def list_point_set(self,n,freq,dwell, RF) :
        #TABLE MODE
        #n is the point number (or index) in the list
        #freq should be a float in GHz, as elsewhere
        #dwell is the dwell time for this point only (in milliseconds)
        #pulse turns on pulse modulation; write "ON" or "OFF"
        #RF should be "ON" or "OFF"
        #save for saving to flash; 'F' to save, "" otherwise
        if (n < 1 or n > 32767):
            return "n < 1 or n > 32767 (Invalid Entry!)"
        if (dwell < 0.005 or dwell > 4294000):
            return "Dwell time must be between 0.005 ms and 4,294,000 ms!"
        if (RF != "ON" and RF != "OFF"):
            return "Invalid entry! RF setting must be 'ON' or 'OFF'"
        else:
            cmd_string = '13'
            cmd_string += '0'*(4-len(str(hex(n))[2:])) + str(hex(n))[2:]
            cmd_string += '0'*(12-len(str(hex(int(1000000000000*freq)))[2:]))+str(hex(int(1000000000000*freq)))[2:]
            cmd_string += '0000'
            cmd_string += '0'*(8-len(str(hex(1000*dwell))[2:])) + str(hex(1000*dwell))[2:]
            cmd_string += "0"
            if RF == "ON":
                cmd_string += '1'
            elif RF == "OFF":
                cmd_string += '0'
            print(cmd_string)
            cmd_string = str.encode(cmd_string)
            self.write(cmd_string)
            time.sleep(0.4) #required delay
            return "Point "+str(n)+" updated"
    #def savelist(self):
    #list already automatically saved to temp and permanent memory in list point setup command
        #save the list to flash
        #self.write(b'LIST:SAV')
        #return "List saved"
    def runListPoint(self, n):
        #run list point n
        cmd_string = '14'
        cmd_string += '0'*(4-len(str(hex(n)))[2:]) + str(hex(n))[2:]
        cmd_string = str.encode(cmd_string)
        self.write(cmd_string)
        return "Run list point "+str(n)
    def runList(self,dwell,n,trig):
        #dwell in ms
        #run the list n times
        #trig is 0 (software trigger), 1 (hardware trigger) or 2 (list point hardware trigger)
        cmd_string = '15'
        cmd_string += '0'*(8-len(str(hex(dwell*1000))[2:])) + str(hex(dwell*1000))[2:]
        cmd_string += '0'*(4-len(str(hex(n))[2:])) + str(hex(n))[2:]
        cmd_string += '0'+str(hex(4*trig)[2:])
        cmd_string = str.encode(cmd_string)
        self.write(cmd_string)
        return "List run "+str(n)+" times"
    def stopList(self):
        self.write(b'20')
        return "List stopped"
    def eraseList(self):
        #Erase the list- MUST BE DONE BEFORE SETTING A NEW LIST
        self.write(b'22')
        return "List erased"
        
    def normalSweep(self,startf, endf, stepf, dwell, runs, trig) :
        #startf, endf, stepf are starting, ending, and step frequencies in GHz
        #dwell is the univeral dwell time (applies to all points)
        #runs is how many repetitions of the sweep you want to do
        #trig is the trigger type; software (0), sweep (1), or sweep point (2)
        if (int((endf-startf)%stepf) != 0):
            return "Invalid frequencies! Stepf must divide (endf-startf)."
        if (runs < 1 or runs > 32767):
            return "Invalid run number! Runs must be between 1 and 32767, inclusive."
        if (trig != 0 and trig != 1 and trig != 2):
            return "Invalid entry! Trig must be 0, 1, or 2"
        else:
            startf_h = (12-len(str(hex(int(startf*1000000000000))[2:])))*'0'+ str(hex(int(startf*1000000000000))[2:])
            endf_h = (12-len(str(hex(int(endf*1000000000000))[2:])))*'0'+ str(hex(int(endf*1000000000000))[2:])
            stepf_h = (12-len(str(hex(int(stepf*1000000000000))[2:])))*'0' + str(hex(int(stepf*1000000000000))[2:])
            dwell_h = (8-len(str(hex(1000*dwell)[2:])))*'0'+str(hex(1000*dwell)[2:])
            runs_h = (4-len(str(hex(runs)[2:])))*'0' + str(hex(runs)[2:])

            cmd_string = str('1C')+ startf_h + endf_h + stepf_h+ '0000'+ dwell_h+ runs_h +'0'+str(hex(4*trig)[2:])

            cmd_string = str.encode(cmd_string)
            print(cmd_string)
            self.write(cmd_string)
            return str(startf) + "GHz to "+str(endf) + "GHz normal sweep ran."
    def fastSweep(self,startf, endf, points, dwell, runs, trig):
        #startf, endf, are starting, ending frequencies
        #points is the number of sweep points
        #dwell is the univeral dwell time, in ms (applies to all points)
        #runs is how many repetitions of the sweep you want to do
        #trig is the trigger type; software (0), sweep (1), or sweep point (2)
        if (runs < 1 or runs > 32767):
            return "Invalid run number! Runs must be between 1 and 32767, inclusive."
        if (trig != 0 and trig != 1 and trig != 2):
            return "Invalid entry! Trig must be 0, 1, or 2"
        else:
            startf_h = (12-len(str(hex(int(startf*1000000000000))[2:])))*'0' + str(hex(int(startf*1000000000000))[2:])
            endf_h = (12-len(str(hex(int(endf*1000000000000))[2:])))*'0' + str(hex(int(endf*1000000000000))[2:])
            points_h = (4-len(str(hex(points)[2:])))*'0' + str(hex(points)[2:])
            dwell_h = (8-len(str(hex(1000*dwell)[2:])))*'0'+str(hex(1000*dwell)[2:])
            runs_h = (4-len(str(hex(runs)[2:])))*'0' + str(hex(runs)[2:])
            
            cmd_string = str.encode('17'+startf_h+endf_h+points_h+'0000'+dwell_h+runs_h+'0'+str(hex(4*trig)[2:]))
            print(cmd_string)
            self.write(cmd_string)
            return str(startf) + "GHz to "+str(endf) + "GHz fast sweep ran."    

    def reset(self):
        #resets all values to default
        #default frequency: 10 GHz
        #default ref source: INT
        self.write(b'*RST\r')
        time.sleep(0.6) #MUST sleep this long before any new commands are sent
        return '***Reset***'
    
    







