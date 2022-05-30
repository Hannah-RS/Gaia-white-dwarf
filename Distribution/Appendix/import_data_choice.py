"""
09/11/21
Function for importing 1Msol simulation data but with ability to select how much data to take

:param engulfed: bool, if True include engulfed planets in data
:param jupiter_mass: bool, if True convert planet masses to units of Jupiter mass, if False returns solar mass planets
:param log_mass: bool, if True return logarithm of mass in chosen units
:param data: str, coarse or  fine
:param folder: str, path to simulation data from folder

:returns: data frame with columns [M, a_i, a_f, status], status=1 means engulfed, status=0 means survived
"""
def import_data_choose(engulfed,jupiter_mass,log_mass,data_choice,folder):
    #import required modules and data
    import numpy as np
    import pandas as pd

    #constants
    jupiter=1.898e27 #mass in kg
    sun=1.989e30 #mass in kg
    wd=0.5702 #mass of wd in solar masses - from Alex simulations
    
    
    #import data for 1Msol star
    #had to convert to excel files and import as my csv where losing precision which was throwign problems with the comparison
    if data_choice == 'coarse':
        data=pd.read_csv("{}simulation_data/results_1p0_coarse.csv".format(folder))
        
        data.columns=['M','a_i','a_f','status']
    
    elif data_choice == 'fine':
        #import fine data
        data=pd.read_csv("{}simulation_data/results_1p0_fine.csv".format(folder))
        data.columns=['M','a_i','a_f','status']

        
    else: raise ValueError('Not a valid data option')
            
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
        masses=np.log10(masses) # take logs so axis is nicer
    else: pass

    #now replace data in the array 
    data2.loc[:,'M']=masses #replce data in data frame
    
    return data2

