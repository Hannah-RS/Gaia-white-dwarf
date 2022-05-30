# -*- coding: utf-8 -*-
"""
Function for importing eDR3 wd catalogue in fits form and saving desired columns 
Includes white dwarf names, masses, distance, DR2 source id, Gmag, Pwd

"""


from astropy.io import fits


wd_file = fits.open('Data/gaiaedr3_wd_main.fits.gz',memmap=True)
columns=wd_file[1].columns
data=wd_file[1].data

#get arrays of the things you want
#descriptions are from Gentile Fusillo 2021
name=data['WDJ_name'] #WD J + J2000 RA (hh mm ss.ss)  + Dec. (dd mm ss.s), equinox and epoch 2000
source_id=data['source_id']
distance=data['R_MED_GEO'] #Median of the geometric distance posterior (pc) (Bailer-Jones et al. 2021)  
gmag=data['phot_g_mean_mag'] #Corrected PHOT_G_MEAN_MAG (Gaia Collaboration 2021a)a 
mass=data['mass_mixed'] #Stellar mass (M⊙) resulting from the adopted mass–radius relation and best-fitting parameters (see Section 4) 
pwd=data['Pwd'] #The probability of being a white dwarf 
mass_error=data['emass_mixed'] #error on stellar mass

#change byte order
distance2=distance.byteswap().newbyteorder() 
gmag2=gmag.byteswap().newbyteorder() 
pwd2=pwd.byteswap().newbyteorder() 
mass2=mass.byteswap().newbyteorder() 
name2=name.byteswap().newbyteorder() 
source2=source_id.byteswap().newbyteorder()
mass_error2=mass_error.byteswap().newbyteorder()

from astropy.table import Table
t = Table([name2, distance2, gmag2, pwd2, mass2,source2,mass_error2], names=('name','distance', 'Gmag', 'Pwd','mass','source_id','mass_error'))
t.write('Data/smaller_data_with_name.fits', format='fits')



