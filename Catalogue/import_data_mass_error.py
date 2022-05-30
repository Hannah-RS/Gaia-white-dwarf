# -*- coding: utf-8 -*-
"""
Function for importing eDR3 wd catalogue in fits form and saving desired columns as a fits file
Imports mass and error and creates two columns for min and max mass
Author: Hannah Sanderson
"""


from astropy.io import fits


wd_file = fits.open('Data/gaiaedr3_wd_main.fits.gz',memmap=True)
columns=wd_file[1].columns
data=wd_file[1].data

#get arrays of the things you want
#descriptions are from Gentile Fusillo 2021
distance=data['R_MED_GEO'] #Median of the geometric distance posterior (pc) (Bailer-Jones et al. 2021)  
gmag=data['phot_g_mean_mag'] #Corrected PHOT_G_MEAN_MAG (Gaia Collaboration 2021a)a 
pwd=data['Pwd'] #The probability of being a white dwarf 
mass=data['mass_mixed'] #Stellar mass (M⊙) resulting from the adopted mass–radius relation and best-fitting parameters (see Section 4) 
mass_error=data['emass_mixed'] #error on stellar mass

#change byte order
distance2=distance.byteswap().newbyteorder() 
gmag2=gmag.byteswap().newbyteorder() 
pwd2=pwd.byteswap().newbyteorder() 
mass2=mass.byteswap().newbyteorder() 
mass_error2=mass_error.byteswap().newbyteorder()
from astropy.table import Table
t = Table([distance2, gmag2, pwd2, mass2,mass_error2], names=('distance', 'Gmag', 'Pwd','mass','mass_error'))
t.write('smaller_data_mass_error.fits', format='fits')


