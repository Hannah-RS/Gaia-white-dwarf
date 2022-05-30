# -*- coding: utf-8 -*-
"""
Main script to calculate the detection probability of planets as a function of 
mass and semi-major axis for each white dwarf.

Workflow:
    1. Load data from chosen filtered eDR3 catalogue
    2. Load detection probability data and alpha map
    3. Initialise a matrix of zeros with the same dimensions as the output array
    4. For each WD in the catalogue 
        a) run detection_probability.py - outputs detection probability as a grid
        b) add values to existing detection matrix (ensures only store two of these matrices at a time)
    5. Once done for all WD multiply by the planet occurrence map
    6. Save resulting grid as a csv for plotting in a different script
    Also does the above for a grid where noise is noise+/-error to estimate the size of the uncertainty due to errors in astrometric noise
    
Data is stored in the Catalogue folder
filtered_data_enoise.fits gives the results in the paper. The other filters are for different investigations (see metadata.txt)
Only filtered_data_enoise.fits has the columns for error on astrometric noise. If calculating using other catalogues
will need to comments out lines referrring to enoise as appropriate. You will also need to reduce the number of columns in endian_converter

"""
#Setup
import numpy as np
import time
import pandas as pd

#Step 1: Import data
from astropy.io import fits

#this line depends on file structure

extension='minus_1_cut' #file extension choosing a particular filter
wd_file = fits.open('../Catalogue/Data/filtered_data_{}.fits'.format(extension)) 
data=wd_file[1] #there are 135,625 WD in this file

#change endianness and replace in dictionary to make new data frame
# data in a fits file is big endian, my computer is little endian
from endian_converter import endian_converter
data=endian_converter(data,6) #6 columns in data frame - this line is important - if the number of columns is wrong it won't import all your data

#convert data['noise'] and data['enoise'] to as
data.loc[:,'noise']=data['noise'].copy()*1e-6
data.loc[:,'enoise']=data['enoise'].copy()*1e-6

#Step 2: Load Ranalli 2018 data and alpha map data
  
#import Ranalli data
# read matrix and convert to numpy array
detfract10yr = pd.read_csv('detfract10yr.txt', sep=' ', header=14)
detfract10yr = detfract10yr.values
#log(SN) edges
xedges10yr = np.array([-0.3  , -0.241, -0.182, -0.123, -0.064, -0.005,  0.054,  0.113, \
    0.172,  0.231,  0.29 ,  0.349,  0.408,  0.467,  0.526,  0.585, \
    0.644,  0.703,  0.762,  0.821,  0.88 ,  0.939,  0.998,  1.057])
#log(P/years) edges
yedges10yr = np.array([-1.1  , -1.025, -0.95 , -0.875, -0.8  , -0.725, -0.65 , -0.575, \
   -0.5  , -0.425, -0.35 , -0.275, -0.2  , -0.125, -0.05 ,  0.025, \
    0.1  ,  0.175,  0.25 ,  0.325,  0.4  ,  0.475,  0.55 ,  0.625, \
    0.7  ,  0.775,  0.85 ,  0.925,  1.   ,  1.075,  1.15 ,  1.225, \
    1.3  ,  1.375])

#transform edges
mwd=0.6
snedges10yr=xedges10yr[1:] #need to remove one value as there is an extra bin
unlogP=10**yedges10yr
aedges10yr=(mwd*(unlogP)**2)**(1/3)

#import signal map for a WD at 1pc - created in detection probability heatmaps notebook
alpha_map=pd.read_csv('alpha_map.csv')


#Step 3: Initialise a matrix of zeros with correct dimensions
output=np.zeros([33,31])
output2=np.zeros([33,31])
output3=np.zeros([33,31])

#Step 4:
    # could do this as a loop
    # would also be interesting to see what happens with arrays - will time the loop first
from probability_calculator import detection_probability
tic=time.perf_counter() #time this
for i in range(len(data)): #start with 10
    #output - maps using noise
    #output2 - maps using noise-enoise
    #output3 - maps using noise+enoise
    out1=detection_probability(alpha_map,detfract10yr,aedges10yr,snedges10yr,data.loc[i,'noise'],data.loc[i,'distance'])
    output=output+out1
    
    out2=detection_probability(alpha_map,detfract10yr,aedges10yr,snedges10yr,data.loc[i,'noise']-data.loc[i,'enoise'],data.loc[i,'distance'])
    output2=output2+out2
    
    out3=detection_probability(alpha_map,detfract10yr,aedges10yr,snedges10yr,data.loc[i,'noise']+data.loc[i,'enoise'],data.loc[i,'distance'])
    output3=output3+out3

toc=time.perf_counter()
print('This calculation took {}s'.format(toc-tic)) #for whole catalogue will take around 1500-2000s

#save the output so don't have to rerun stage 1-4 every time if only want to alter step 5
np.savetxt('Results/Probabilities/pjk_{}.csv'.format(extension),output,delimiter=',')
np.savetxt('Results/Probabilities/ll_pjk_{}.csv'.format(extension),output2,delimiter=',')
np.savetxt('Results/Probabilities/ul_pjk_{}.csv'.format(extension),output3,delimiter=',')






