# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 16:55:38 2021

@author: Hannah

Creates scatter plot of planet mass vs initial positions
but only those with final positions inside the Gaia period detection region
Points are colour coded by final poistions
"""
#import required modules and data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#import data
from import_data_fn import import_data_1

data=import_data_1(False,True,False,'../') #import surviving planets only, Jupiter mass

#filter data
data2=data[data['a_f']<3.91] #take points with final positions inside Gaia range

############ add Gaia detection curve ###############################

from Gaia_detection_limits_app import mass_detect_fn
mag=15  #choose WD magnitudes which give most of the S/N>3 detections (see histograms)
d=[20,40] #distance to system in pc - will make two curves for different distances

#choose period range
Pmax=10 #in units of years
amax=Pmax**(2/3)*0.6**(1/3)  #Kepler's law, a in units of au

n=20 #number of au to sample
a=np.linspace(0.01,amax,n) #start at 1au as  stuff inside that won't survive
m_detect=np.zeros([len(d),n])

#get a 3D array for the three plots
for k in range(len(d)): #distance
    m_detect[k,:]=mass_detect_fn(a,3,d[k],mag,'../../') #want curves of S/N=3
#################################################################


with sns.plotting_context('paper',font_scale=1.5):
    plt.figure(figsize=[10,10])
    plt.scatter(data2['a_i'],data2['M'],marker='o',c=data2['a_f'])
    plt.plot(a,m_detect[0,:],linestyle='-.',label='G$_{mag}$=15 at 20pc',color='black')
    plt.plot(a,m_detect[1,:],linestyle='--',label='G$_{mag}$=15 at 40pc',color='black')
    plt.xlabel('$a_i$/au')
    plt.ylabel('M/M$_J$')
    plt.text(0.1,1/317,'Earth',fontsize='medium',color='black')
    plt.text(0.1,17/317,'Neptune',fontsize='medium',color='black')
    plt.text(0.1,1,'Jupiter',fontsize='medium',color='black')
    plt.colorbar(label='$a_f$')
    plt.yscale('log')
    plt.xlim([0,4])
    plt.ylim([10**(-2.6),10**1.1])
    plt.legend()
    #plt.title('Initial positions of simulated planets that \n have final periods less than 10 years')
    plt.savefig('../../../Plots/intial_positions_in_range.pdf',bbox_inches='tight')

