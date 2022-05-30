# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 18:18:17 2021
Modified 26/01/22

Code to create graphs of minimum detectable planet mass for a given signal to noise as a function of a

chosen an error for a typical magnitude 15 and am plotting curves of constant S/N
 N is the along-scan accuracy per field of view =sigma_fov
Gaia website gives sky-averaged parallax errors 
Error calculation done using mass_detect_fn
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import matplotlib as mpl #needed for changing colour cycle
from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color=['black', 'blue', 'seagreen','springgreen', 'lightskyblue' ])

import seaborn as sns

mag=15
m_wd=0.6
d=[20,40,60] #distance to system in pc - will make three plots one for each WD survey

#choose period range
Pmax=10 #in units of years
amax=Pmax**(2/3)*(m_wd)**(1/3)  #Kepler's law, a in units of au

n=20 #number of au to sample
a=np.linspace(1,amax,n) #start at 1au to align with simulation points

#array of signal to noise
l=5
sigma=np.linspace(1,3,l) #1 is p_detect =0.3 reasonable lower bound, 3 p_detect=0.92 for 10 year mission (Ranalli 2018)

from Gaia_detection_limits import mass_detect_fn
#mass_detect_fn(a,sigma,d,mag)

m=len(d)
mplt=np.zeros([m,n,l])

#get a 3D array for the three plots
for k in range(m): #distance
    for i in range(n): #semi-major axis
        for j in range(l): #signal to noise
            mplt[k,i,j]=mass_detect_fn(a[i],sigma[j],d[k],mag)
        
 
################# make figure ##############################
plottype='paper'
   

with sns.plotting_context('{}'.format(plottype),font_scale=1.5):
    plt.figure(figsize=[12,6],dpi=300) 
    for k in range(m-1):
        plt.subplot(1,2,k+1)
        for j in range(l):
            plt.plot(a,mplt[k,:,j],label='{}'.format(sigma[j]))
        
        plt.ylabel('Planet mass/M$_{Jup}$')
        plt.xlabel('Semi-major axis/au')
        plt.ylim([0,6])
        plt.xlim([1,amax])
        plt.legend(title='S/N')
        plt.title('G$_{}$ {} at {}pc '.format('{mag}',mag,d[k]))
        plt.subplots_adjust(bottom=0.1, top=0.95, left=0.1, right=0.95,wspace=0.4,hspace=0.4)
        #plt.savefig('../../plots/graph1_subplots.pdf',bbox_inches='tight')     
