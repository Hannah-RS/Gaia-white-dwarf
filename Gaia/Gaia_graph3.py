# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 18:18:17 2021
Modified 26/01/22


Code to create a graph of S/N against d with contours for given planet mass and a


 N is the along-scan accuracy per field of view =sigma_fov
Gaia website gives sky-averaged parallax errors 
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl #needed for changing colour cycle
from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=['k','blue','seagreen','skyblue']) #set colour for graph later
import seaborn as sns
#import in error data

sigma_w=pd.read_table('Gaia_error.txt',sep=" ",header=0)
mag=15 #typical WD mag averaged from Fusillo data

#create array of planet masses
earth_mass=5.9724e24 #mass of earth for scale
solar_mass=1.989e30/earth_mass #mass of Sun in units of Earth mass

m_wd=0.6*solar_mass #average white dwarf mass
l=20
d=np.linspace(1,100,l) #distance to system in pc - input variable

#choose semi-major axis range
amax=4
amin=1
n=4 #number of  au points to sample 
a=np.linspace(amin,amax,n) #start at 1au as assume stuff inside that won't survive

#array of planet masses
mplt=[1,17,318]  #Earth, Neptune, Jupiter in units of Earth mass

#define function to return signal to noise as a function of mass
#d in this function will be an index for the distance array
def mass_detect(a,d_ind,mp):
    #input a semi major axis, sensitivity, distance away and return a planet
    mag_ind=sigma_w.loc[sigma_w.iloc[:,0]==mag].index[0]
    noise=sigma_w.iloc[mag_ind,2]*1e-6*5.1786
    
    signal=(mp/m_wd)*a/d[d_ind]
    sn=signal/noise
    return sn

m=len(mplt)
sn=np.zeros([m,n,l])

#get a 3D array for the three plots
for k in range(m): #planet mass
    for i in range(n): #semi-major axis
        for j in range(l): #distance
            sn[k,i,j]=mass_detect(a[i],j,mplt[k])
        
#make plots to display the data
mjup=mplt[2]



################################  Make figure ###########################################
plottype='paper'
   

with sns.plotting_context('{}'.format(plottype),font_scale=2):
    plt.figure(figsize=[10,10])
    k=0
    for i in range(n):
            
         plt.loglog(d,sn[k,i,:],ls='-',label='{:.1f}'.format(a[i]))
    k=1
    for i in range(n):
            
         plt.loglog(d,sn[k,i,:],ls='--')
    
    k=2
    for i in range(n):
            
         plt.loglog(d,sn[k,i,:],ls='-.')   
    plt.ylabel('S/N')
    plt.xlabel('d/pc')
    plt.ylim([0.1,20])
    plt.xlim([1,100])
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')
    plt.hlines(y=1,xmin=0,xmax=100,color='black',ls='-')
    plt.legend(title='Semi-major axis/au')
    plt.title('S/N for a G$_{mag}$ 15, 0.6M$_\odot$ white dwarf')
    plt.text(25,1.8,'Jupiter at 4au',rotation=-39.5)
    plt.text(7.3,0.25,'Neptune at 4au',rotation=-39.5)
    #plt.savefig('../../plots/log_mplt_d_{}.pdf'.format(plottype),bbox_inches='tight')  
    
