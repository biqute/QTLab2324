import matplotlib.animation as animation
import HP8753E as hp
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def dist(x, k=4):
    if x!=51:
        return k/(x-51)*np.sin((k*(x-51))) * (1 + np.random.random()/10 - + np.random.random()/10)
    else:
        return 0

def check_T_stable(duration):

        check = False

        t0 = datetime.now().timestamp()
        current = datetime.now().timestamp()
        
        fig, ax = plt.subplots(1, 2, figsize=(10,5))
        
        '''
            T = temperature to check 
            error = interval in which temperature value can float
            interval = seconds to sample temperature T
            Compute dT/dt --> compute "moving" average
        '''

        while((current-t0)<duration):
            window = 10 # Temperature samples for computing moving average
            average, temp, secs = [], [], []
            for i in range(window):
                temp.append(dist(i))
                secs.append(i)
                average.append(np.mean(temp))
            count = window
            count_equal = 0
            while (check==False):
                value = dist(count)
                temp.append(value)
                temp.pop(0)
                count += 1
                secs.append(count)
                secs.pop(0)
                av = np.mean(temp)
                average.append(av)
                print(np.size(secs),np.size(temp))
                ax[0].scatter(secs, temp, color='black', s=1, marker='o', label='raw data')
                ax[1].plot(count, av, color='red', marker='x', label='moving average')
                ax[1].scatter(count, 0, marker='+', color='black')
                ax[0].set_xlim([count-window,count])
                ax[1].set_xlim([count-window,count])
                ax[0].set_ylim([-1,1])
                ax[0].set_xlabel('cycle unit')
                ax[0].set_ylabel('raw data')
                ax[1].set_xlabel('cycle unit')
                ax[1].set_ylabel('moving average')
                plt.pause(0.01)
                if (abs(average[count-window]-average[count-1-window]) < 0.001):
                    count_equal += 1
                    print(average[count-window], average[count-1-window])
                if (count_equal > 4):
                    check = True
            plt.show()
            current = datetime.now().timestamp()
        return True

check_T_stable(duration=60)