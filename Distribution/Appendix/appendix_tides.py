# -*- coding: utf-8 -*-
"""
Figure 3
Plots mass against final positions for 1Msol progenitor
Colour coded by f=af(true)/af(adiabatic), f=1 means tides are not important
"""

#import required modules and data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#set constants
jupiter=1.898e27 #mass in kg
sun=1.989e30 #mass in kg
wd=0.5702 #mass of wd in solar masses - from Alex simulations
mwd_f=wd*sun/jupiter #mwd in jupiter masses for gaia detection curve and boundary

#import data
from import_data_choice import import_data_choose
#import fine and grid data separately
data2=import_data_choose(False,True,False,'coarse','../') #remove engulfed planets, in Jupiter masses
data3=import_data_choose(False,True,False,'fine','../') #remove engulfed planets, in Jupiter masses

p=1/wd #Mi/Mf
tide_boundary=data2['a_i']*p
ma=data2['M']*jupiter/sun #convert from Jupiter masses to solar masses 
data2['tb']=tide_boundary
data2['f']=(1+1.3*(ma)**(2/7))/(1+1.3*((ma)*p)**(2/7)) #criterion for scattering - use masses as these are still in units of solar mass
data2['ratio']=data2['a_f']/(data2['tb'])

#repeat for both data sets
tide_boundary=data3['a_i']*p
ma=data3['M']*jupiter/sun #convert from Jupiter masses to solar masses 
data3['tb']=tide_boundary
data3['f']=(1+1.3*(ma)**(2/7))/(1+1.3*((ma)*p)**(2/7)) #criterion for scattering - use masses as these are still in units of solar mass
data3['ratio']=data3['a_f']/(data3['tb'])
##################################   add Gaia detection curves #################################
###################################copied from Gaia_graph1.py #####################################


mag=15  #choose WD magnitudes which give most of the S/N>3 detections (see histograms)
d=[20,40] #distance to system in pc - will make two curves for different distances

#choose period range
Pmax=10 #in units of years
amax=Pmax**(2/3)*0.6**(1/3)  #Kepler's law, a in units of au

n=20 #number of au to sample
a=np.linspace(0.01,amax,n) #start at 1au as  stuff inside that won't survive
m_detect=np.zeros([2,n])

#create detection curves
from Gaia_detection_limits_app import mass_detect_fn
#get a 3D array for the three plots
for k in range(len(d)): #distance
    m_detect[k,:]=mass_detect_fn(a,3,d[k],mag,'../../') #want curves of S/N=3


################################# Effects of tides - colour coded by af/aadiabatic ###################
with sns.plotting_context('paper',font_scale=1.5):
    plt.figure(figsize=[10,10])
    plt.scatter(data2['a_f'],data2['M'],marker='+',c=data2['ratio'],vmin=0.2,vmax=1,label='0.03 au initial position spacing')
    
    plt.scatter(data3['a_f'],data3['M'],marker='x',c=data3['ratio'],vmin=0.2,vmax=1,label='0.001au initial position spacing')
    
    #add Gaia detection lines
    plt.vlines(3.91,np.min(data2['M']),np.max(data2['M']),linestyle='--',colors='black')
    plt.plot(a,m_detect[0,:],color='black',linestyle='--',label='S/N=1, G$_{mag}$=15 at 20pc')
    plt.plot(a,m_detect[1,:],color='black',linestyle='-.',label='S/N=1, G$_{mag}$=15 at 40pc')
    #add labels for planet masses
    plt.text(0.1,1/317+0.0005,'Earth',fontsize='medium',color='black')
    plt.text(0.1,17/317,'Neptune',fontsize='medium',color='black')
    plt.text(0.1,1,'Jupiter',fontsize='medium',color='black')
    plt.xlabel('$a_f$/au')
    plt.ylabel('M/M$_J$')
    plt.yscale('log')
    plt.colorbar(label='$f=a_f(true)/a_f(adiabatic)$')
    #plt.xlim([0,3.91])
    plt.xlim([0,5.5])
    plt.ylim([np.min(data2['M']),np.max(data2['M'])])
    plt.legend(bbox_to_anchor=(0.57,0.22),fontsize='small')
    #plt.title('Effects of tides on positions of surviving planets \n 1M$_\odot$ progenitor')
    plt.savefig('../../../Plots/effect_of_tides.pdf',bbox_inches='tight')
    
