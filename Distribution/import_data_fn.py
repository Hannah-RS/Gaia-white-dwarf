# -*- coding: utf-8 -*-
"""
20/05/22 Function for importing rerun simulation 1Msol data

:param engulfed: bool, if True include engulfed planets in data
:param jupiter_mass: bool, if True convert planet masses to units of Jupiter mass, if False returns solar mass planets
:param log_mass: bool, if True return logarithm of mass in chosen units
:param path: str, default is blank, path to Alex_new_data_NERC from where the code is being run

:returns: data frame with columns [M, a_i, a_f, status], status=1 means engulfed, status=0 means survived
"""
def import_data_1(engulfed,jupiter_mass,log_mass,path=''):
    #import required modules and data
    import numpy as np
    import pandas as pd
    import sys 
    sys.path.insert(1, '{}'.format(path))
    #constants
    jupiter=1.898e27 #mass in kg
    sun=1.989e30 #mass in kg
    wd=0.5702 #mass of wd in solar masses - from Alex simulations
    
    #import data for 1Msol star
    
    #import simulation A
    datac=pd.read_csv(sys.path[1]+"simulation_data/results_1p0_coarse.csv")
    datac.columns=['M','a_i','a_f','status']
    #import fine data - simulation B
    dataf=pd.read_csv(sys.path[1]+"simulation_data/results_1p0_fine.csv")
    dataf.columns=['M','a_i','a_f','status']
    
    #add another 0.03 past MU
    datae=pd.read_csv(sys.path[1]+"simulation_data/results_1p0_extras.csv")
    datae.columns=['M','a_i','a_f','status']

    
    #concatenate data frames
    data=pd.concat([datac,dataf,datae],ignore_index=True) #ignore index to avoid duplicated values
    data=data.dropna() #removes blank lines read in as NaN
   
    #filtering
    data2=data[data['status']!=-1]#remove simulation errors
    
    if engulfed == True: #keep engulfed planets
        pass
    elif engulfed == False:
        data2=data2[data2['status']==0] #remove engulfed planets from data set
    else:
        raise ValueError('Invalid option: engulfed must equal True or False')
    
    if jupiter_mass == True:
        ma=np.array(data2['M'].copy()) #mass array in stellar masses - take a true copy 
        masses=ma*(sun/jupiter) #convert to units of jupiter mass
    else:
        masses=np.array(data2['M'].copy())

    if log_mass == True:
        logmasses=np.log10(masses) # take logs so axis is nicer
        #now replace data in the array 
        data2['logM']=logmasses #create new column in dataframe
    else: pass
        
    #now replace data in the array 
    data2.loc[:,'M']=masses #replace data in data frame
    
    return data2

