#fai funzione che manda mail se temperatura va oltre tot
import pyvisa
import numpy as np
import time
import smtplib, ssl

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
    def __new__(self, board = 'ASRL1::INSTR', num_points = 1601 ):
        if self._instance is None:
            print('Creating the object')
            self._instance = super(FridgeHandler, self).__new__(self)
            self._inst = pyvisa.ResourceManager().open_resource(board)
            print('Cryo handler object created correctly!\n')
        return self._instance
  
    def execute(self, cmd):
        self._inst.write('$'+ str(cmd))

    def read(self, cmd):                #It may happen that the read command returns strange things with ?s and Es. In that case you can't trust the result
        out = '?'
        while ('?' in out[0]) or ('E' in out[0]) or ('A' in out[0]):
            out = self._inst.query_ascii_values(str(cmd), converter='s')
            #print(out)       
        out = str.rstrip(out[0])
        return out

    def set_control(self, stringa='C3'):
        print('Choose between local and remote')
        if (stringa=='local'):
            self._inst.write('C0')
        elif (stringa=='remote'):
            self._inst.write('C3')
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

    def set_still(self, stringa):
        
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

            print('Email sent!')
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
    
    def set_T(self, T):
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

        self.execute(cmd)
        self.execute('A2')
        self.execute('T' + str(10*int(T)))

#Possiamo provare ad implementare un tempo dopo il quale, se la temperatura non è stabile, usciamo dal ciclo?    
    def check_stability(self, T, error, sleeptime = 5, pause = 10):     # T --> desired temperature
                                                                                        # error --> uncertainty allowed on the temperature
                                                                                        # interval --> minimum time of stability required. Defaults to 1 minute and half                                                             # sleeptime --> time interval between each check. Defaults to 5 seconds
        counter = 0
        countermax = 10
        out = False
        while (counter < countermax): 
            if self.get_sensor(21) < 5:
                self.send_alert()
                counter = countermax + 1                                                             
            if self.get_sensor(2) > 22000:
                self.send_alert()
                counter = countermax + 1
            if (T-error < self.get_sensor() and self.get_sensor() < T + error): # check if values are ok. change get_sensor parameters (actually remove them -> they'll default to mixing chamber) !!!!!!!!
                counter = 0
                print('I found a temperature value out of range. I am going to sleep for ' + str(pause) + ' seconds')
                time.sleep(pause) #sleeps for 10 seconds default minutes if T not stable         
            else:
                counter += 1
                time.sleep(sleeptime) #5 sec of sleep between each T check
        if counter == countermax:
            print("Temperature is stable and fridgeboy is ready!")
            out = True
        return out


    def scan_sensor(self, sensore, dur, step, cmd):
        # La funzione voglio che :
            # 1. Prenda il sensore x
            # 2. Definito una durata dur, prenda dati ogni step secondi 
                # 2.1 Se riscontra un valore strano deve mandare un alert con un messaggio
            # 3. Deve ritornare i dati come nome_sensore, dato, tempo

        sens = self.get_sensor(sensore)
        N = int(dur/step)
        Temps = np.zeros(N)
        for i in range(N):
            out = self._inst.query_ascii_values(cmd, converter='s')
            out = str.rstrip(out[0])
            time.sleep(step)
            out = (out.split('+'))[1]           # split the string where '+' is and gives back only the second part (1)
            Temps[i] = float(out)
            print('Data at step ' + i + ' is ' + out)

