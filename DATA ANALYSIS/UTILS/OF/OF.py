# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import gridspec
import gc, h5py
from scipy import optimize
from scipy import signal

# %load_ext autoreload
# %autoreload 2

rc('text', usetex=False)
rc('font', family='serif', size=20)
rc('figure', figsize=(12,8))
rc('axes',linewidth=2)

class Medium():
    '''
    Questa è la classe che permette di definire il segnale atteso dato degli eventi di rumore
    e degli eventi di segnale rumorosi.
    '''

    def __init__(self, medium=None, NPS=None):
        self._medium   = medium # Pulse medium
        self._NPS      = NPS    # noise power spectrum (compunted in not normalized units)
        return

    def set_NPS(self, NPS):
        # Set Noise Power Spectrum (externally computed)
        self._NPS = NPS

    def get_NPS(self):
        return self._NPS

    def get_medium(self):
        return self._medium

    def set_medium(self, medium):
        self._medium = medium
        return

    def create_medium(self, data, bsl=None, indexes=None):
        for _ in range(2):
            self.__do_medium(data, bsl=bsl, indexes=indexes)
        return

    def __do_medium(self, data, bsl=None, indexes=None):

        edata = (data.T - bsl).T if indexes is None else (data[indexes].T - bsl[indexes]).T

        S_omega = np.fft.fft(edata, axis=1)
        S_omega[:,0] = np.zeros(edata.shape[0])        #WHY?

        if self._medium is None:
            S_cc = S_omega[0,:].conjugate()
        else:
            S_cc = np.fft.fft(self._medium).conjugate()
            S_cc[0] = 0.


        K   = 1.
        H   = K * (S_cc/self._NPS)
        OFT = np.fft.ifft(S_omega*H).real
        OFT = np.concatenate((OFT[:,int(edata.shape[1]/2):edata.shape[1]], OFT[:,0:int(edata.shape[1]/2)]), axis=1)

        delay_ref = int(edata.shape[1]/2.)
        time      = np.arange(edata.shape[1])
        a,b       = parabolic_fit(OFT)[0:2]

        max_pos_true = -b/(2*a)
        delay        = max_pos_true - delay_ref
        del a,b, max_pos_true

        for i in range(edata.shape[0]):
            edata[i,:] = np.interp(time+delay[i],time, edata[i,:])

        self._medium = np.mean(edata,axis=0)

        return

def create_filter(medium,NPS):
    '''
    medium è il segnale atteso, quello senza rumore
    NPS è il noise spectral density
    '''

    val_cal = medium[-1]
    S       = np.fft.fft(medium)
    S[0]    = 0+0*1j
    OF_med  = np.fft.ifft(S*S.conjugate()/NPS).real
    K       = val_cal/np.amax(OF_med)
    H = K*S.conjugate()/NPS   #H è la funzione di trasferimento del filtro, nel dominio delle frequenze

    return H

def PSD(edata,t_sample,wind = "hanning"):
    '''
    data una matrice di eventi di rumore (edata) e il tempo di campionamento (t_sample), valuta la PSD
    '''
    wind     = wind
    npt      = edata.shape[1]

    f, pxx = signal.welch(edata,fs=1./t_sample, window=wind, nperseg=npt, scaling='density', axis=1)
    mean_true_scale = np.mean(pxx, axis = 0)

    f = np.append( f[:-1], -1*f[1:][::-1])
    mean_true_scale = np.append( mean_true_scale[:-1],  mean_true_scale[1:][::-1] )
    mean_use_scale  = mean_true_scale* (1./t_sample*edata.shape[1]/2.)    #correct?

    return f, mean_use_scale, mean_true_scale

def parabolic_fit(mat,stop=0):

    max_pos = np.argmax(mat[:,stop:-1],axis=1) + stop
    dim     = np.arange(0,mat.shape[0])
    x1 = max_pos-1
    x2 = max_pos
    x3 = max_pos+1
    y1 = mat[dim,x1]
    y2 = mat[dim,x2]
    y3 = mat[dim,x3]
    a  = (x1*(y3-y2) + x2*(y1-y3)+x3*(y2-y1) )  / ( (x1-x2)*(x1-x3)*(x2-x3)   )
    b  = (y2-y1)/(x2-x1)-a*(x1+x2)
    c  = y1 -a*x1**2 -b*x1

    return a,b,c,max_pos

def applyOF(edata,H):

        events_OF_f = np.fft.fft(edata, axis=1)*H
        OFF         = np.array(np.sum(np.abs(events_OF_f), axis=1)/edata.shape[1])
        events_OF   = np.fft.ifft(events_OF_f).real
        events_OF   = np.concatenate((events_OF[:,int(edata.shape[1]/2):edata.shape[1]], events_OF[:,0:int(edata.shape[1]/2)]),axis=1)
        a,b,c       = parabolic_fit(events_OF, 0)[0:3]
        OFmax_pos   = np.argmax(events_OF,axis=1)
        OFdelay     = -b/(2.*a)  -edata.shape[1]/2
        OFT         = -1.*(b**2)/(4.*a) +c
        del a,b,c, events_OF_f

        OFtest = 1. - OFT/OFF

        return OFT, OFF, OFdelay, OFtest