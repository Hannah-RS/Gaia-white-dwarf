# -*- coding: utf-8 -*-
"""
Script for combining Pjk with d^2Nwd/dloga dlog P to get a distribution of detected planets
Uses the output of total_detection_probability.py
Returns d2Ndet/dloga dlogP
"""

import numpy as np

wd_extension = 'minus_1_cut' #which set of wds are you using

output=np.loadtxt('Results/Probabilities/pjk_{}.csv'.format(wd_extension),delimiter=',') #Pjk
output2=np.loadtxt('Results/Probabilities/ll_pjk_{}.csv'.format(wd_extension),delimiter=',') #lower error on Pjk
output3=np.loadtxt('Results/Probabilities/ul_pjk_{}.csv'.format(wd_extension),delimiter=',') #upper error on Pjk

add_path='../Distribution/'

dist_extension = 'final' #which wd distribution are you using

hist_val_wd=np.loadtxt('{}wd_distribution_{}.csv'.format(add_path,dist_extension),delimiter=',')
error_val_wd=np.loadtxt('{}error_distribution_{}.csv'.format(add_path,dist_extension),delimiter=',')
a_edges_wd=np.loadtxt('{}wd_a_edges.csv'.format(add_path),delimiter=',')
m_edges_wd=np.loadtxt('{}wd_m_edges.csv'.format(add_path),delimiter=',')

detected_planets=np.multiply(hist_val_wd,output) #elementwise multiplication

# combine fractional errors in quadrature then multiply by value of detected planets in each bin to get absolute error
#make a mask to avoid div 0 error
mask_hist_val=np.ma.masked_where(hist_val_wd==0,hist_val_wd)
mask_output=np.ma.masked_where(output==0,output)
lower_error_planets=np.multiply(detected_planets,np.sqrt((output2/mask_output)**2+(error_val_wd/mask_hist_val)**2)) 
upper_error_planets=np.multiply(detected_planets,np.sqrt((output3/mask_output)**2+(error_val_wd/mask_hist_val)**2)) 

#Step 6: Save the data for plotting

np.savetxt('Results/Distributions/detected_planets_{}.csv'.format(wd_extension),detected_planets,delimiter=',')
np.savetxt('Results/Distributions/lower_error_planets_{}.csv'.format(wd_extension),lower_error_planets,delimiter=',')
np.savetxt('Results/Distributions/upper_error_planets_{}.csv'.format(wd_extension),upper_error_planets,delimiter=',')


