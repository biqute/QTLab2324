import numpy as np
from matplotlib import rc
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
        self._H        = None
        return

    @property
    def NPS(self):
        #Noise Power Spectrum
        return self._NPS
    
    @NPS.setter
    def NPS(self, NPS):
        # Set Noise Power Spectrum (externally computed)
        self._NPS = NPS

    @NPS.getter
    def get_NPS(self):
        return self._NPS

    @property
    def medium(self):
        return self._medium
    
    @medium.setter
    def medium(self,m):
        self._medium = m
    
    @medium.getter
    def medium(self):
        return self._medium

    def create_medium(self, data, bsl=None, indexes=None):
        for _ in range(2):
            result = self.__do_medium(data, bsl=bsl, indexes=indexes)
        return result

    def __do_medium(self, data, bsl=None, indexes=None):
        """
        Process a 1D data array, applying a filtering operation in the frequency domain and aligning the signal based on a parabolic fit.

        Parameters:
        data    : 1D array, the signal to process
        bsl     : 1D array, baseline to subtract from the data (optional)
        indexes : 1D array of indices to select specific data points (optional)

        Returns:
        float : The mean value of the aligned data
        """

        # Subtract baseline
        data = (data - bsl) if indexes is None else (data[indexes] - bsl[indexes])

        # FFT of the data
        S_omega = np.fft.fft(data)

        # Determine S_cc
        if self._medium is None:
            S_cc = S_omega.conjugate()
        else:
            S_cc = np.fft.fft(self._medium).conjugate()
            S_cc[0] = 0.  # Set the zero-frequency component to zero

        # Interpolate self._NPS to match the length of S_cc
        npt = len(S_omega)
        NPS_interpolated = np.interp(np.linspace(0, 1, npt), np.linspace(0, 1, len(self._NPS)), self._NPS)

        # Calculate the filter H
        K = 1.
        H = K * (S_cc / NPS_interpolated)

        # Apply the filter and perform inverse FFT
        OFT = np.fft.ifft(S_omega * H).real

        # Reorder the time-domain signal (circular shift)
        OFT = np.concatenate((OFT[int(npt / 2):], OFT[:int(npt / 2)]))

        # Calculate delay and align the data
        delay_ref = int(npt / 2)
        time = np.arange(npt)

        # Perform parabolic fit on OFT to find the peak position
        a, b = self.parabolic_fit(OFT)[0:2]
        max_pos_true = -b / (2 * a)
        delay = max_pos_true - delay_ref

        # Align the data based on the computed delay
        data_aligned = np.interp(time + delay, time, data)

        # Return the mean value of the aligned data
        return data_aligned
    
    @property
    def H(self):
        return self._H
    
    @H.setter
    def H(self):
        self._H = self.create_filter()

    @H.getter
    def H(self):
        return self._H


    def create_filter(self):
        '''
        medium è il segnale atteso, quello senza rumore
        NPS è il noise spectral density
        '''

        val_cal = self._medium[-1]
        S       = np.fft.fft(self._medium)
        S[0]    = 0+0*1j
        OF_med  = np.fft.ifft(S*S.conjugate()/self._NPS).real
        K       = val_cal/np.amax(OF_med)
        return K*S.conjugate()/self._NPS   #H è la funzione di trasferimento del filtro, nel dominio delle frequenze

    '''
    def PSD(self,data,t_sample,wind = "hann"):
        
        #data una matrice di eventi di rumore (edata) e il tempo di campionamento (t_sample), valuta la PSD

        wind     = wind
        npt      = len(data)

        f, pxx = signal.welch(data,fs=1./t_sample, window=wind, nperseg=npt, scaling='density', axis=1)
        mean_true_scale = np.mean(pxx, axis = 0)

        f = np.append(f[:-1], -1*f[1:][::-1])
        mean_true_scale = np.append( mean_true_scale[:-1],  mean_true_scale[1:][::-1] )
        mean_use_scale  = mean_true_scale* (1./t_sample*len(data)[1]/2.)    #correct?

        return f, mean_use_scale, mean_true_scale
    '''

    def PSD(self, data, t_sample, wind="hann"):

        # Number of points in the data
        npt = len(data)

        # Compute PSD using Welch's method
        f, pxx = signal.welch(data, fs=1./t_sample, window=wind, nperseg=npt, scaling='density')

        # No need for mirroring frequencies or additional scaling
        return f, pxx


    def parabolic_fit(self, data, stop=0):
        """
        Perform a parabolic fit on a 1D data array to find the peak position.
        
        Parameters:
        data : 1D array, data to fit
        stop : int, index from which to start looking for the peak (optional)

        Returns:
        tuple : coefficients (a, b, c) for the parabolic fit y = ax^2 + bx + c
                and the position of the peak
        """
        # Find the maximum position
        max_pos = np.argmax(data[stop:]) + stop

        # Get neighboring points
        x1, x2, x3 = max_pos - 1, max_pos, max_pos + 1
        y1, y2, y3 = data[x1], data[x2], data[x3]

        # Fit a parabola
        a = (x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)) / ((x1 - x2) * (x1 - x3) * (x2 - x3))
        b = (y2 - y1) / (x2 - x1) - a * (x1 + x2)
        c = y1 - a * x1**2 - b * x1

        return a, b, c, max_pos

    def applyOF(self, data, H):
        """
        Apply the filtering operation in the frequency domain and calculate metrics.

        Parameters:
        data : 1D array, the signal to process
        H    : 1D array, the filter to apply

        Returns:
        tuple : OFT (filtered output total), OFF (filtered output total), 
                OFdelay (delay of the peak), OFtest (testing value),
                and OFmax_pos (position of the maximum in the output)
        """
        # FFT of the data
        events_OF_f = np.fft.fft(data) * H

        # Calculate the filtered signal
        OFF = np.sum(np.abs(events_OF_f)) / len(data)
        events_OF = np.fft.ifft(events_OF_f).real

        # Reorder the time-domain signal (circular shift)
        npt = len(data)
        events_OF = np.concatenate((events_OF[npt//2:], events_OF[:npt//2]))

        # Perform parabolic fit on OFT to find the peak position
        a, b, c, _ = self.parabolic_fit(events_OF, 0)

        # Calculate the peak position and delay
        OFmax_pos = np.argmax(events_OF)
        OFdelay = -b / (2 * a) - npt / 2
        OFT = -b**2 / (4 * a) + c

        # Test value
        OFtest = 1 - OFT / OFF

        return OFT, OFF, OFdelay, OFtest, OFmax_pos