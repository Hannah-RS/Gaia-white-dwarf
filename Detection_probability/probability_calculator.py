# -*- coding: utf-8 -*-
"""
Function to calculate detection probability as a function of planet mass and semi-major axis
for a given white dwarf
Functionalised form of the example code in Ranalli_data/Detection probability heatmaps notebook

:params noise: float, noise of WD [as]
:params d: float, distance to WD [pc]

:returns prob_hist: np.array, dimensions are 33 (corresponding to binning of Ranalli data in semi-major 
                                 axis space) by 31 (corresponding to mass binning in Alex data)
                                values are the detection probabilities for a planet according to mass and semi-major axis for a given white dwarf
Work in progress:
    1. Dependency on current file structure
    2. hard coded number of bins in m direction as 31
"""

def detection_probability(alpha_map,detfract10yr,aedges10yr,snedges10yr,noise,d):
    #import modules
    import numpy as np
    import pandas as pd
    
    #Step 1: Get signal to noise values for every mass and semi-major axis

    #scale alpha_map by noise and distance
    alpha_map.loc[:,'SN']=alpha_map['alpha'].copy()/(noise*d)
    
    #Step 2: Compare with Ranalli data to find corresponding detection probability values
    
    #for each signal and semi major axis value in alpha_map find the corresponding bin edges
    alpha_map.loc[:,'a_index']=np.digitize(alpha_map['a'],aedges10yr) #find index of bin it belongs to in a space
    alpha_map.loc[:,'sn_index']=np.digitize(np.log10(alpha_map['SN']),snedges10yr) #find index of bin it belongs to in m space
    
    #Relabel outliers
    #Things with S/N greater than max value will be given an index of 23
    #These strong objects are still detectable so just relabel with second lowest index

    alpha_map.loc[(alpha_map.a_index == (len(aedges10yr))),'a_index']=len(aedges10yr)-1
    alpha_map.loc[(alpha_map.sn_index == (len(snedges10yr))),'sn_index']=len(snedges10yr)-1

    #things outside of range will move into smallest bin as value in this bin is 0 anyway
    alpha_map.loc[(alpha_map.a_index == 0),'a_index']=1
    alpha_map.loc[(alpha_map.sn_index == 0),'sn_index']=1

    alpha_map.loc[:,'prob_detect']=detfract10yr[alpha_map['sn_index']-1,alpha_map['a_index']-1] 
    
    #Step 3: convert into a map of detection probability as a function of mass and semi-major axis
    #make into a histogram of values which will be in a sum
    # do combination of int, array in bins option as want a edges to match
    prob_hist, a_edges, m_edges=np.histogram2d(alpha_map['a'],alpha_map['logM'],weights=alpha_map['prob_detect'],bins=[aedges10yr,31])
    
    return prob_hist
    
    