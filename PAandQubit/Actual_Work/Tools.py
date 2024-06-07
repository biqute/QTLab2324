import numpy as np


def dBm_to_mV(dbm, R = 50 ):                            # R = 50 Ohm

    return (np.sqrt(2 * R * 10**((dbm - 30)/10)))* 1e3



def mV_to_dBm(mv, R = 50):

    return 10 * np.log10(((mv*1e-3)**2)*500/ R)