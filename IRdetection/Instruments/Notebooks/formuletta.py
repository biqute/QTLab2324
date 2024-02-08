csi = (hbar * omega)/(2*KB*T)
num = np.exp(-d0/(KB*T))*np.sinh(csi)*sp.kn(0,csi)
den = (1-2*np.exp(-d0/(KB*T))*np.exp(-csi)*sp.iv(0,-csi))


dq0 = -1/(q0**2)
dalpha = (1/alpha)*(kondo(T)-1/q0+b*np.log(T/T_k))
db = -np.log(T/T_k)
dd0 = alpha * dalpha * (-1/(KB*T)) * (1/den)
dT = (((d0/(KB*T*T))*num - (csi/T)*num*/np.tanh(csi) + (csi/T)*num*sp.kn(1,csi)/sp.kn(0,csi))*den+num*(1-den)*(d0/(KB*T*T) + (csi/T)*(1-sp.iv(1,csi)/sp.iv(0,csi))))/(den**2)



def errorQ():
    e = np.sqrt((dq0*err_q0)**2 + (dalpha*err_alpha)**2 + (db*err_b)**2 + (dd0*err_d0)**2 + (dT*err_T)**2)
    return e



