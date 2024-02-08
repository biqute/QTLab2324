import matplotlib.animation as animation
import HP8753E as hp
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

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
                av = np.mean(temp)
                average.append(av)
                count += 1
                secs.append(count)
                secs.pop(0)
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

'''
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    temp_c = np.random.normal()
    # Add x and y to lists
    xs.append(i)
    ys.append(temp_c)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys))#, interval=10)
plt.show()
'''