# -*- coding: utf-8 -*-
"""
Script for filtering WD data from eDR3 to output WD with S/N>3 for a 1Mj planet at 2au
Then compares with the Montreal White Dwarf Database to add columns for Ca/H and Ca/He
as a csv and latex table, ranked in order of highest S/N

Takes initial catalogue and removes:
    objects with Pwd < 0.75    
    objects with Gmag > 20.7
    objects with M > 0.663 Msol
    objects with nan values
    
  
Then columns for  noise and error on noise in units of micro as
Then calculates S/N for 1Mj at 2au
Then filters for S/N >3

"""
from astropy.io import fits
import pandas as pd
import numpy as np

wd_file2 = fits.open('Data/smaller_data_with_name.fits')
dataf=wd_file2[1]
extension = 'SN_1mj' #name of filter applied

#change endianness and replace in dictionary to make new data frame
from endian_converter import endian_converter
data=endian_converter(dataf,7) #need to change the number of columns here if have more columns in filtered data

#create variable to store size at each step to see how much you remove
data_size=[len(data)]
#exclude undesired values
data=data[data['Pwd']>0.75]
data_size.append(len(data))
data=data[data['Gmag']<20.7] 
data_size.append(len(data))
data=data[data['mass']<0.663] 
data_size.append(len(data))

data=data.dropna(subset=['distance']) #drop data which are missing values needed for the detection calculations
data_size.append(len(data))
data=data.dropna(subset=['Gmag'])
data_size.append(len(data))

print(data_size)
#create column for noise [micro as] for each WD

from noise_calculator import noise_converter
data['noise'], data['enoise']=noise_converter(data['Gmag']) #noise in units of micro as

#calculate S for a 1Mj planet
alphaj=(1.898e27/(0.6*1.989e30))*2*1e6 # [micro as]

data['SN'] = alphaj/(data['noise']*data['distance'])
data['SN_error'] = data['SN']/data['noise']*data['enoise'] #error on SN



subset = data[data['SN']-data['SN_error']>3] #only keep values with S/N >3 within error
subset.sort_values('SN',ascending=False) #sort data by SN

#import and compare with pollution database
mwdd = pd.read_csv('Data/MWDD-export.csv',delimiter=',',low_memory=False)

#split the string of column 2 to compare DR3 Id
mwdd[['Gaia','EDR3','source_id','blank1','blank2']]=mwdd['name'].str.split(' ',expand=True)

# drop None source id values
mwdd=mwdd.dropna(axis=0,subset=['source_id'])

#make dataframe smaller
mwdd_small = mwdd[['source_id','logcahe','logcah','Dpc']]
#filter so less than max distance to speed up comparison

mwdd_small = mwdd_small[mwdd_small['Dpc']<subset['distance'].max()]

#now compare source id
subset.loc[:,'source_id']=subset.loc[:,'source_id'].astype(str)
mwdd_small.loc[:,'source_id']=mwdd_small.loc[:,'source_id'].astype(str)

#merges the two data frames matching source id
new = subset.merge(mwdd_small,'outer','source_id')
#everything below row = len(subset) is in montreal database but my not list so exclude
final = new.iloc[0:len(subset),:]
#reorder by S/N
final=final.sort_values('SN',ascending=False)
final2 = final[['name','source_id','distance','Gmag','Pwd','mass','mass_error','SN','SN_error','logcahe','logcah']]

#now tidy up to save and export to latex - remove duplicates here and make small columns for paper, nan?
table_dat=final[['name','source_id','distance','Gmag','SN','SN_error','logcahe','logcah']]
#save as a csv
final2.to_csv('Data/SN_1mj.csv',',',index=False)

table_dat.to_latex(header=['White dwarf name','Gaia source ID','R_MED_GEO','G$_{mag}$','S/N for 1$M_J$ at 2au','error on S/N','Ca/He','Ca/H'],index=False,float_format='{:0.1f}'.format,na_rep=' ')








