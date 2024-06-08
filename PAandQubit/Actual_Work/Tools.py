import numpy as np


def dBm_to_mVrms(dbm, R = 50):                            # R = 50 Ohm

    return (np.sqrt(R * 10**((dbm - 30)/10)))* 1e3



def mVrms_to_dBm(mv, R = 50):

    return 10 * np.log10((mv * 1e-3)**2 * 1000 / R)


def dBm_to_mVpk(dbm, R = 50):                            # R = 50 Ohm

    return (np.sqrt(2 * R * 10**((dbm - 30)/10)))* 1e3



def mVpk_to_dBm(mv, R = 50):

    return 10 * np.log10((mv * 1e-3)**2 * 500 / R)


def dBm_to_mVpp(dbm, R = 50):                            # R = 50 Ohm

    return 2 * (np.sqrt(2 * R * 10**((dbm - 30)/10)))* 1e3



def mVpp_to_dBm(mv, R = 50):

    return 10 * np.log10((mv * 1e-3)**2 * 125 / R)