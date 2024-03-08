import HP8753E as hp
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import sys
sys.path.insert(1, 'C://Users//kid//SynologyDrive//Lab2023//KIDs//QTLab2324//IRdetection//Instruments//Gas_Handler22')
import handler
import time


def check_stability(window, disc):
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

check_stability(50, 10)