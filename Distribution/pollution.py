# -*- coding: utf-8 -*-
"""
Figure 8 in paper
Creates a scatter plot of simulated final positions of planets colour-coded by
scattering ability

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
from import_data_fn import import_data_1
data=import_data_1(False,True,False) #remove engulfed planets, in Jupiter masses

data2=data.sort_values('a_f',axis=0,ascending=True) #sort in order of final position

p=1/wd #Mi/Mf
tide_boundary=data2['a_i']*p
ma=data2['M']*jupiter/sun #convert from Jupiter masses to solar masses 
data2['tb']=tide_boundary
data2['f']=(1+1.3*(ma)**(2/7))/(1+1.3*((ma)*p)**(2/7)) #criterion for scattering - use masses as these are still in units of solar mass
data2['ratio']=data2['a_f']/(data2['tb'])

#use status column to set for moved in and types of scattering

data2['status'].where(~(data2['a_i']>data2['a_f']),0,inplace=True) #indicates moved inward
data2['status'].where(~((data2['ratio']<data2['f']) & (data2['a_i']<data2['a_f'])),0.5, inplace=True) #no outer belt scattering
data2['status'].where(~((data2['ratio']>data2['f']) & (data2['a_i']<data2['a_f'])),1, inplace=True) #outer belt scattering

#filter data according to status to make three scatter marks for summary plot
d1=data2[data2['status']==0] #moved inward
d2=data2[data2['status']==0.5] #moved out, no scattering
d3=data2[data2['status']==1]  #moved in, scattering  

data_e=import_data_1(True, True, False) #reimport data with engulfed planet, Jupiter masses
d4=data_e[data_e['status']==1] #an array of engulfed planets for illustrative purposes

#get arrays for boundary regions for filling plot

d1.sort_values('a_f',axis=0,ascending=True)     
d2.sort_values('a_f',axis=0,ascending=True)     
d3.sort_values('a_f',axis=0,ascending=True)
d4.sort_values('a_f',axis=0,ascending=True)
     

#get mass array 
#need different lengths for each category as not all planet masses fall in each category
mdrop1=d1.drop_duplicates('M',keep='first')
marray1=mdrop1.sort_values('M',axis=0,ascending=True)
mass1=np.array(marray1['M']) #get just mass values

mdrop2=d2.drop_duplicates('M',keep='first')
marray2=mdrop2.sort_values('M',axis=0,ascending=True)
mass2=np.array(marray2['M']) #get just mass values

mdrop3=d3.drop_duplicates('M',keep='first')
marray3=mdrop3.sort_values('M',axis=0,ascending=True)
mass3=np.array(marray3['M']) #get just mass values

mdrop4=d4.drop_duplicates('M',keep='first')
marray4=mdrop4.sort_values('M',axis=0,ascending=True)
mass4=np.array(marray4['M']) #get just mass values

#set up arrays
b1=np.zeros(len(mass1))
b2=np.zeros(len(mass2))
b3=np.zeros(len(mass3))

# extract the innermost (b) and outermost (o) final position for each mass in each category        
for i in range(len(mass1)): #inward movement
    b1[i]=d1[d1['M']==mass1[i]].nsmallest(1, 'a_f')['a_f']

    
for i in range(len(mass2)): #no scattering
    b2[i]=d2[d2['M']==mass2[i]].nsmallest(1, 'a_f')['a_f']

    
for i in range(len(mass3)): #outward and scattering
    b3[i]=d3[d3['M']==mass3[i]].nsmallest(1, 'a_f')['a_f']


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
from Appendix.Gaia_detection_limits_app import mass_detect_fn
#get a 3D array for the three plots
for k in range(len(d)): #distance
    m_detect[k,:]=mass_detect_fn(a,3,d[k],mag,'../') #want curves of S/N=3


##################################### Summary plot new log scale ##################################################
from matplotlib.legend_handler import HandlerTuple
with sns.plotting_context('paper',font_scale=2):
    plt.figure(figsize=[20,10])
        
    #scatter on the final positions
    f=plt.scatter(d1['a_f'],d1['M'],marker='o',color='indigo')
    g=plt.scatter(d2['a_f'],d2['M'],marker='x',color='seagreen')
    h=plt.scatter(d3['a_f'],d3['M'],marker='+',color='gold')
    dead=plt.scatter(d4['a_f'],d4['M'],marker='*',color='gray')
      
    #add Gaia detection lines
    k=plt.vlines(3.91,np.min(marray3['M']),np.max(marray3['M']),linestyle='-',colors='black',label='10 year length of extended Gaia mission')
    l=plt.plot(a,m_detect[0,:],color='black',linestyle='--',label='S/N=1, G$_{mag}$=15 at 20pc')
    z=plt.plot(a,m_detect[1,:],color='black',linestyle='-.',label='S/N=1, G$_{mag}$=15 at 40pc')
    plt.yscale('log')

    #add scattering labels
    plt.annotate('Inward migration due to tides',xy=(2.7,3),xytext=(1.28,8),arrowprops=dict(arrowstyle='->'),color='white',bbox=dict(facecolor='indigo', alpha=1))
    plt.annotate('Change in resolution of \n simulated initial positions',xy=(4.5,2.2),xytext=(4.3,0.78),arrowprops=dict(arrowstyle='->'),bbox=dict(facecolor='white', alpha=0.7,edgecolor='white'))
    plt.text(5.8,1e-1,'Adiabatic outward migration',bbox=dict(facecolor='gold', alpha=1))
    plt.text(2,1.5e-2,'Outward migration slowed due to tides',color='white',bbox=dict(facecolor='seagreen', alpha=1))
    plt.text(0.5,0.7e-1,'Engulfed planets',color='white',bbox=dict(facecolor='gray', alpha=1))
    
    plt.xlabel('$a_f$/au')
    plt.ylabel('M/M$_J$')
    
    #create first legend for planet positions
    first_legend=plt.legend([(f,g,h),(dead)],['Final planet positions','Engulfed planets'],numpoints=1,handler_map={tuple: HandlerTuple(ndivide=None)},loc='upper right',fontsize='small',frameon=True,edgecolor='black',markerscale=2,framealpha=1)
    # Add the legend manually to the current Axes.
    ax = plt.gca().add_artist(first_legend)
    
    #second legend for gaia stuff
    plt.legend(loc='lower right',fontsize='small',frameon=True,edgecolor='black',markerscale=0.8,framealpha=1)
    plt.xlim([0,8])
    plt.ylim([min(marray3['M']),max(marray3['M'])])

    
    plt.savefig('../../Plots/summary_scatter.pdf',bbox_inches='tight')