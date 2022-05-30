# -*- coding: utf-8 -*-
"""
Function for Gaia detection limits

:param a: float or array, semi-major axis in units of au
:param sigma: float, chosen signal to noise ratio
:param d: float, distance to the system in pc
:param mag: int, magnitude of white dwarf in range 13-20

:returns: mp, float or array, mass detectable planet at a given semi-major axis in units of Jupiter mass


"""

def mass_detect_fn(a,sigma,d,mag):
    import pandas as pd
    
    #import in error data
    sigma_w=pd.read_table('Gaia_error.txt',sep=" ",header=0)
    
    #set mass of white dwarf
    jupiter=1.898e27 #mass in kg
    sun=1.989e30 #mass in kg
    mwd=0.6 #average mass, solar masses
    mwd_j=0.6*sun/jupiter
    
    #find noise corresponding to the inputted magnitude
    mag_ind=sigma_w.loc[sigma_w.iloc[:,0]==mag].index[0] #find position of chosen magnitude
    
    #calculate required signal, convert from mas to as
    alpha=sigma*5.1786*sigma_w.iloc[mag_ind,2]*1e-6 #choose second column for DR5 
    
    #invert required signal to find planet mass
    mp=alpha*d*mwd_j/a
    return mp  #planet is returned in Jupiter masses