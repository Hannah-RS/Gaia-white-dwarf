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
    objects with M > 0.663 Msol
    objects with nan values

    
Adds columns for  noise and error on noise in units of micro as

Make sure to alter the file name based on the cuts applied
Also alter the number of columns and values in line 55  t=Table depending on how much 
information you imported from the eDR3 catalogue (names, masses etc)
Also alter number of columns in endian converter if importing more information
"""
from astropy.io import fits
import pandas as pd


wd_file2 = fits.open('Data/smaller_data_with_name.fits') #delete with_name
dataf=wd_file2[1]

extension = 'final' #name of filter applied
#change endianness and replace in dictionary to make new data frame
from endian_converter import endian_converter
data=endian_converter(dataf,7) #need to change the number of columns here if have more columns in filtered data
# was 4 
#create variable to store size at each step to see how much you remove
data_size=[len(data)]
#exclude undesired values
#data=data[data['source_id']==4698424845771339520]
data_size.append(len(data))
data=data[data['Pwd']>0.75]
data_size.append(len(data))
data=data[data['Gmag']<20.7] 
data_size.append(len(data))
data1=data[data['mass']<0.663] #apply mass filter to remove overly massive white dwarfs
data2=data[data['mass'].isna()==True]  #keep mass nan objects as assume they are 0.6M_\odot
data = pd.concat([data1,data2],ignore_index=True) #rejoin the two data frames
data_size.append(len(data))
#data=data[data['distance']<100]
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









