"""# Calcolo il filtro ottimo"""

data = None # E' la matrice con i dati su cui si vuole definire il segnale atteso (o medio).
            # Ogni riga è un segnale.
noise = None # E' la matrice con i dati su cui si vuole definire lo spettro di rumore.
# Le matrici devono avere lo stesso numero di colonne.

preStop = 70  #E' il numero di punti della finestra di acquisizione senza il segnale.

bsl = np.mean(data[:,0:preStop],axis=1)
bsl_noise = np.mean(noise,axis=1)

#Faccio in modo tale che i dati e il rumore partano da 0

data = data - np.array([bsl]).T
noise = noise - np.array([bsl_noise]).T

# Calcolo la PSD del rumore, il primo ingrediente del filtro ottimo
t_samp = None   #in secondi

freq, PSD_noise, _ =PSD(noise,t_samp)

npt = PSD_noise.shape[0]
plt.loglog(-1*freq[npt//2:][::-1],PSD_noise[npt//2:][::-1],c='k')
plt.xlabel("Freq [Hz]")
plt.ylabel("PSD [a.u.]")
plt.show()

# Calcolo il segnale atteso (medio), l'ultimo ingrediente per il filtro ottimo

medium = Medium(NPS = PSD_noise)
medium.create_medium(data,np.zeros(data.shape[0]))
medium_pulse = medium.get_medium()

plt.plot(medium_pulse,c='k')
plt.xlabel("# sample")
plt.show()

# Creo il filtro H e lo applico ai dati su cui ho calcolato il medio
H = create_filter(medium_pulse,PSD_noise)

data_filtered_f =  np.fft.fft(data, axis=1)*H # dati filtrati dominio freq

data_filtered_t =  np.fft.ifft(data_filtered_f).real   #dati filtrati dominio temp
data_filtered_t =  np.concatenate((data_filtered_t[:,int(data_filtered_t.shape[1]/2):data_filtered_t.shape[1]], data_filtered_t[:,0:int(data_filtered_t.shape[1]/2)]),axis=1)

#Guardo come cambiano i dati prima e dopo il filtro ottimo
nev = 0
#===================
plt.plot(data[nev],c='k',label="original")
plt.plot(data_filtered_t[nev],label="filtered",c='b')
plt.legend()
plt.show()

"""# Applico il filtro ottimo per valutare l'ampiezza dei dati"""

# Questo passaggio è da fare DOPO che si è calcolato H

data = None  #E' la matrice dei dati su cui voglio applicare il filtro

preStop = 70  #E' il numero di punti della finestra di acquisizione senza il segnale.

bsl = np.mean(data[:,0:preStop],axis=1)
bsl_noise = np.mean(noise,axis=1)

#Faccio in modo tale che i dati e il rumore partano da 0, forse inutile(?)
data = data - np.array([bsl]).T

OFT, OFF, OFdelay, OFtest = applyOF(data,H)

# OFT è l'ampiezza del segnale, calcolata con il filtro ottimo nel dominio del tempo
# OFF è l'ampiezza del segnale, calcolata con il filtro ottimo nel dominio delle frequenze, dovrebbe essere uguale
#     (o molto simile) a OFT
# OFdelay e OFtest ignoratele.

