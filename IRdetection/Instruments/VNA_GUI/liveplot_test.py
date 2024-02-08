import matplotlib.animation as animation
import HP8753E as hp
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def low_pass(data, t):
                
        dt = .001
        t = np.arange(0,1,dt)
        n = len(t)
        fhat = np.fft.fft(data,n)
        PSD = fhat * np.conj(fhat)/n
        indices = PSD>max(PSD)/2
        fhat = indices*fhat
        ffilt = np.fft.ifft(fhat)
        return ffilt


def check_T_stable(duration):

        check = False

        t0 = datetime.now().timestamp()
        current = datetime.now().timestamp()
        
        fig = plt.figure()
        ax = fig.add_subplot()
        
        '''
            T = temperature to check 
            error = interval in which temperature value can float
            interval = seconds to sample temperature T
            Compute dT/dt --> compute "moving" average
        '''

        while((current-t0)<duration):
            window = 50 # Temperature samples for computing moving average
            average, temp, secs = [], [], []
            for i in range(window):
                temp.append(np.random.random())
                secs.append(i)
                average.append(np.mean(temp))
            count = window
            count_equal = 0
            while (check==False):
                value = np.random.random()
                temp.append(value)
                temp.pop(0)
                count += 1
                secs.append(count)
                secs.pop(0)
                temp = low_pass(temp, secs)
                av = np.mean(temp)
                average.append(av)
                print(np.size(secs),np.size(temp))
                ax.scatter(secs, temp, color='black', s=1, marker='o', label='raw data')
                ax.scatter(count, av, color='red', marker='x', s=1, label='moving average')
                ax.set_xlim([count-window,count])
                plt.pause(0.05)
                if (abs(average[count-window]-average[count-1-window]) < 0.000001):
                    count_equal += 1
                    print(average[count-window], average[count-1-window])
                if (count_equal > 4):
                    check = True
            plt.legend()
            plt.show()
            current = datetime.now().timestamp()
        return True

check_T_stable(duration=60)