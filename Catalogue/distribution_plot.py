# -*- coding: utf-8 -*-
"""
Script to plot WD distribution as a function of Gmag and pc coloured by 1/(noise*d) 
Creates Figure 7 in paper
"""
from astropy.io import fits
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns


wd_file = fits.open('Data/filtered_data_enoise.fits')
dataf=wd_file[1]

#change endianness and replace in dictionary to make new data frame
from endian_converter import endian_converter
data=endian_converter(dataf,6)

#for a sense of scale find alpha for mj at 2au
alphaj=(1.898e27/(0.6*1.989e30))*2*1e6 # [micro as]

#create new S/N column
data.loc[:,'SN_1Mj']=alphaj/(data['noise'].copy()*data['distance'].copy())
data['SN_error_1Mj'] = data['SN_1Mj']/data['noise']*data['enoise'] #error on SN

#filter to remove anything with S/N <0.5 (lines up with min val in Ranalli)
subset=data[data['SN_1Mj']>0.5]

#for a sense of scale find alpha for 13mj at 3.91au
alpha13j=(13*1.898e27/(0.6*1.989e30))*3.91*1e6 # [micro as]
#create new S/N column
data.loc[:,'SN_13Mj']=alpha13j/(data['noise'].copy()*data['distance'].copy())
data['SN_error_13Mj'] = data['SN_13Mj']/data['noise']*data['enoise'] #error on SN

#filter to remove anything with S/N <0.5 (lines up with min val in Ranalli)
subset2=data[data['SN_13Mj']-data['SN_error_13Mj']>0.5]

#filter to remove anything with S/N >3 
subset3=data[data['SN_13Mj']-data['SN_error_13Mj']>3]

subset4=data[data['SN_1Mj']-data['SN_error_1Mj']>3] #must be above 3 if you include error too
subset4['distance'].max()
subset4['Gmag'].max()

#group high S/N points separately
subset3_high=subset3[subset3['SN_13Mj']>10]
subset3_low=subset3[subset3['SN_13Mj']<10]

subset4_high=subset4[subset4['SN_1Mj']>10]
subset4_low=subset4[subset4['SN_1Mj']<10]

#make plot for S/N>3
with sns.plotting_context('paper',font_scale=2.5):
    plt.figure(figsize=[20,10],tight_layout=True)
    plt.subplot(1,2,1)
    plt.scatter(subset4_low['distance'],subset4_low['Gmag'],c=subset4_low['SN_1Mj'],s=70,cmap='viridis_r')
    plt.colorbar(label='S/N')
    plt.scatter(subset4_high['distance'],subset4_high['Gmag'],color='#440154FF',s=100,marker='+')
    plt.ylabel('G$_{mag}$')
    plt.xlabel('d/pc')
    plt.title('a) 1M$_J$ planet at 2au')
    
    #repeat for largest possible signal
    
    plt.subplot(1,2,2)
    plt.scatter(subset3_low['distance'],subset3_low['Gmag'],c=subset3_low['SN_13Mj'],s=50,vmin=3,cmap='viridis_r')
    plt.colorbar(label='S/N')
    plt.scatter(subset3_high['distance'],subset3_high['Gmag'],color='#440154FF',s=50,marker='+')
    plt.ylabel('G$_{mag}$')
    plt.xlabel('d/pc')
    plt.title('b) 13M$_J$ planet at 3.91 au')
    
    
    #plt.savefig('../../Plots/white_dwarf_distribution.pdf',bbox_inches='tight')
    #plt.savefig('../../Plots/white_dwarf_distribution_g3_group.png')
    
    
