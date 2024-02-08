import pyvisa
import numpy as np
import time
import smtplib
from datetime import datetime

gmail_username = 'kinekids2324'
sent_from = 'kinekids2324@gmail.com'
sent_to = ['r.maifredi@campus.unimib.it', 'a.costanzo1975@campus.unimib.it', 'e.torreggiani@campus.unimib.it']
sent_subject = "Hey Friends!"
sent_body = ("Hey, what's up? friend!\n\n"
             "I hope you have been well!\n"
             "\n"
             "Cheers,\n"
             "Riccardo\n")

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)
gmail_app_password = 'ylry timq pxfu xxmw'

class FridgeHandler:

    _instance = None
    _inst = None
    def __new__(self, board = 'ASRL1::INSTR', num_points = 1601):
        if self._instance is None:
            print('Creating the object')
            self._instance = super(FridgeHandler, self).__new__(self)
            self._inst = pyvisa.ResourceManager().open_resource(board)
            print('Cryo handler object created correctly!\n')
        return self._instance
  
    def execute(self, cmd):
        self._inst.write('$'+ str(cmd))
  
    def read(self, cmd):
        answer = self._inst.query_ascii_values(str(cmd), converter='s')
        answer = str.rstrip('\r')
        answer = str.rstrip('\n')
        return answer
        
        
    def comm_protocol(self,value='Q0'):
        
        #Defines the communication protocol
            #Q0: "Normal"
            #Q2: "Sends <LF> after each <CR>"
            
        self.execute(str(value))
    
    def wait(self, secs):
        
        #Sets a delay interval before each character is sent 
        #from IDR via the computer interface
        
        self.execute('W'+str(secs))        

    def read2(self, cmd): #It may happen that the read command returns strange things with ?s and Es. In that case you can't trust the result
        out = '?'
        while ('?' in out[0]) or ('E' in out[0]) or ('A' in out[0]):
            out = self._inst.query_ascii_values(str(cmd), converter='s')
            #print(out)       
        out = str.rstrip(out[0])
        return out

    def set_control(self, stringa='remote'):
        #Define control type - Default to remote mode
        if (stringa=='local'):
            self.execute('C0') #local & locked
        elif (stringa=='remote_locked'):
            self.execute('C1') #remote & locked
        elif (stringa=='local_unlocked'):
            self.execute('C2') #local & unlocked
        elif (stringa=='remote'):
            self.execute('C3') #remote & unlocked
        else:
            print('Choose between local and remote')
        return

    def set_mixch_mode(self, stringa):
        print('Choose between off, fhp, tc')
        if (stringa=='off'):
            self._inst.write('A0')
        elif (stringa=='fhp'):
            self._inst.write('A1')  
        elif (stringa=='tc'):
            self._inst.write('A2')
        else:
            print('Choose between off, fhp, tc')
        return

    def set_still_sorb(self, stringa):

        #Set on/off state of Still & Sorb Heaters
        
        print('O0: Still OFF, Sorb OFF')
        print('O1: Still ON,  Sorb OFF')
        print('O2: Still OFF, Sorb ON in temperature control')
        print('O3: Still ON,  Sorb ON in temperature control')
        print('O4: Still OFF, Sorb ON in power control')
        print('O5: Still ON,  Sorb ON in power control')
        
        if (stringa=='O0'):
            self.visa_handle.write('O0')
        if (stringa=='O1'):
            self.visa_handle.write('O1')
        if (stringa=='O2'):
            self.visa_handle.write('O2')
        if (stringa=='O3'):
            self.visa_handle.write('O3')
        if (stringa=='O4'):
            self.visa_handle.write('O4')
        if (stringa=='O5'):
            self.visa_handle.write('O5')
        else:
            print('O0: Still OFF, Sorb OFF')
            print('O1: Still ON,  Sorb OFF')
            print('O2: Still OFF, Sorb ON in temperature control')
            print('O3: Still ON,  Sorb ON in temperature control')
            print('O4: Still OFF, Sorb ON in power control')
            print('O5: Still ON,  Sorb ON in power control')
        return
    
    def set_still_power(self,valore):
        #Set Still power in units of 0.1 mW
        self._inst.write('S'+str(valore))
        print('Still power settled to: '+str(valore*0.1)+' mW')
        
    def set_sorb_power(self,valore):
        #Set Sorb power in units of 1 mW
        self._inst.write('S'+str(valore))
        print('Sorb power settled to: '+str(valore)+' mW')

    def check_press(self):
        res = self.get_sens(14) < 2800 and self.get_sens(15) < 2880
        if(not res):
            print("PRESSIONE ALTA!")
            self.send_alert_mail()
            time.sleep(60*10)
        return res

    def send_alert(self):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_username, gmail_app_password)
            server.sendmail(sent_from, sent_to, email_text)
            server.close()
            print('Email alert sent!')
        except Exception as exception:
            print("Error: %s!\n\n" % exception)

    def get_sensor(self, cmd = 3):
        '''Measure temperature or pressure of a sensor of the system. Default: MC temperature.'''                           
        k = self.read('R' + str(cmd))
        k = k.replace("R", "")
        k = k.replace("+", "")
        k = float(k)
        return k       

    def state(self):
        out = self._inst.query_ascii_values('X', converter='s')
        out = str.rstrip(out[0])
        print(out)
        
        
    def set_mix_power_range(self,cmd):
        
        #Set Exponent for Mix Power Range
        
        if cmd=='E1':
            self._inst.write('E1')
        if cmd=='E2':
            self._inst.write('E2')
        if cmd=='E3':
            self._inst.write('E3')
        if cmd=='E4':
            self._inst.write('E4')
        if cmd=='E5':
            self._inst.write('E5')       
    
    def set_mixc_temp(self, T):
        '''Set temperature of the mixing chamber to arbitrary value in 0.1 mK. 
        Be careful! The value of temp has to be specified with 5 figures!
        Range is the command name for the power range (E1, E2 ...)'''
        
        cmd = 'E'
        if T <= 50:
            cmd += '1'
        elif T <= 90:
            cmd += '2'
        elif T <= 140:
            cmd += '3'
        elif T <= 400:
            cmd += '4'
        else:
            cmd += '5'

        self.set_mix_power_range(cmd)
        self._inst.write('A2')
        self._inst.write('T' + str(10*int(T)))
        
    def set_mix_prop_band(self, value):
        
        #Set Mixing Chamber Proportional Band in units of 0.1%
        
        self._inst.write('p'+str(value))
        print('Mixing Chamber Integral Band settled to: '+str(value*0.1)+' %')
        
    def set_mix_int_band(self, value):
        
        #Set Mixing Chamber Integral Band in units of 0.1 minute
        
        self._inst.write('i'+str(value))
        print('Mixing Chamber Integral Band settled to: '+str(value*0.1)+' minute')
        
    def set_sorb_control_temp(self, value):
        
        #Set Sorb Control Temperature in units of 0.1K
        
        self._inst.write('K'+str(value))
        print('Control Temperature settled to: '+str(value*0.1)+' Kelvin')