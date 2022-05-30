# -*- coding: utf-8 -*-
"""
Function to calculate the noise for a given WD based on its Gmagnitude
The formula used for the error is from https://www.cosmos.esa.int/web/gaia/science-performance#astrometric%20performance

:params gmag: slice of dataframe containing floats corresponding to white dwarf magnitude

:returns noise: slice of dataframe containing floats corresponding to a 10 year mission, to be appended to existing dataframe

"""
def magnitude_error(gmag):
    """
    Calculates error for given Gmag from https://www.cosmos.esa.int/web/gaia/science-performance#astrometric%20performance

    Parameters
    ----------
    gmag : float, denotes the broad-band, white-light, Gaia magnitude

    Returns
    -------
    sigma_pi: float, parralax standard error [micro as]

    """
    T_factor = 0.527
    
    import numpy as np
    z = 10**(0.4*(gmag-15)) # apply same criterion to everything for z
    z[10**(0.4*(13-15))>10**(0.4*(gmag-15))]=10**(0.4*(13-15)) #replace values for which the second thing is bigger
    
    sigma_pi = T_factor*(40+800*z+30*z**2)**(0.5)
    return sigma_pi

def noise_converter(gmag):
    """
    Calculate single along accuracy per field of view for a given white dwarf 

    Parameters
    ----------
    gmag : float
            broad-band, white-light, Gaia magnitude

    Returns
    -------
    sigma_fov: float
                single along scan accuracy per field of view [micro as]
    esigma_fov: float, 
                error in single along scan accuracy per field of view [micro as]

    """
    import numpy as np
    
    sigma_pi = magnitude_error(gmag) #use our above function
    
    #convert sigma_pi to sigma_fov 
    #150 \pm 46 = sky-averaged number of field crossings in 10 year mission (Ranalli 2018)
    # 2.15 geometric factor
    #1.1 science contingency margin - reduced from 1.2 in eDR3
    e_nfov=50 #error in number of field crossings
    
    sigma_fov = np.sqrt(150)*sigma_pi/(2.15*1.1)
    
    # sigma_fov = C*sqrt(Nfov), esigma_fov= d(sigma_fov)/d(Nfov)*eNfov
    esigma_fov=0.5*sigma_pi/(2.15*1.1*np.sqrt(150))*50
    
    return sigma_fov, esigma_fov
    
