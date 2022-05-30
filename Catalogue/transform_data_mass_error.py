# -*- coding: utf-8 -*-
"""
Script for filtering WD data from eDR3
Initial columns: 
    distance (pc)
    Gmag
    Pwd 
    mass [Msol]
Takes initial catalogue and removes:
    objects with Pwd < 0.75    
    objects with Gmag > 20.7

    objects with nan values

Then either removes
      M+eM > 0.663
      M-eM > 0.663
      M+3eM > 0.663
Adds columns for  noise in units of micro as
"""
from astropy.io import fits
import pandas as pd

extension = 'minus_1_cut' #name of cut applied
wd_file2 = fits.open('Data/smaller_data_mass_error.fits')
dataf=wd_file2[1]

#change endianness and replace in dictionary to make new data frame
from endian_converter import endian_converter
data=endian_converter(dataf,5)

#create variable to store size at each step to see how much you remove
data_size=[len(data)]
#exclude undesired values
data=data[data['Pwd']>0.75]
data_size.append(len(data))
data=data[data['Gmag']<20.7] 
data_size.append(len(data))
data=data[data['mass']<0.609] 
data_size.append(len(data))
#data=data[data['distance']>5]
#data_size.append(len(data))
data=data.dropna(subset=['distance']) #drop data which are missing values needed for the detection calculations
data_size.append(len(data))
data=data.dropna(subset=['Gmag'])
data_size.append(len(data))

print(data_size)
#create column for noise [micro as] for each WD
from noise_calculator import noise_converter
data['noise'], data['enoise']=noise_converter(data['Gmag']) #noise in units of micro as

#save as a fits file again
from astropy.table import Table
t = Table([data['distance'], data['Gmag'], data['Pwd'], data['mass'],data['noise'],data['enoise']], names=('distance', 'Gmag', 'Pwd','mass','noise','enoise'))
t.write('Data/filtered_data_{}.fits'.format(extension), format='fits')









