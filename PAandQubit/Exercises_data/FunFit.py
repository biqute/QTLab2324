import pandas as pd
import numpy as np

def moving_avg(x, y, size: int):
    if size % 2 == 0:
        size = size + 1
    # Convert array of integers to pandas series
    numbers_series = pd.Series(y)
    # Get the window of series of observations of specified window size
    windows = numbers_series.rolling(size)
    # Create a series of moving averages of each window
    moving_averages = windows.mean()
    # Convert pandas series back to list
    moving_averages_list = moving_averages.tolist()
    # Remove null entries from the list
    y_avg = moving_averages_list[size - 1:]
    a = int((size-1)/2)
    x_cut = x[a:-a]
    return {'x': x_cut, 'y': y_avg}


def data_cut(x, y, L_cut, R_cut):
    
    idx_L = np.argmin(np.abs(x - L_cut))
    idx_R = np.argmin(np.abs(x - R_cut))

    return {'x': x[idx_L:idx_R], 'y': y[idx_L:idx_R]}

def Lorentzian(x, amplitude, center, width, offset):
    return (amplitude - offset) / (1 + (2 * (x - center) / width) ** 2) + offset

import numpy as np

def Sinc(x, pars):
    amplitude   = pars[0]
    center      = pars[1]
    offset      = pars[2]

    return amplitude * (np.sinc(x - center) ** 2) + offset


