"""
01/11/21
Function for importing Alex's 1Msol data

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
    #had to convert to excel files and import as my csv where losing precision which was throwing problems with the comparison
    #import simulation A
    datas=pd.read_excel(sys.path[1]+"simulation_data/results_grid.xlsx")
    datas.columns=['M','a_i','a_f','status']
    #import fine data - simulation B
    dataf=pd.read_excel(sys.path[1]+"simulation_data/results_fine.xlsx")
    dataf.columns=['M','a_i','a_f','status']
    #import extra data - simulation C
    datae=pd.read_excel(sys.path[1]+"simulation_data/results_extra.xlsx")
    datae.columns=['M','a_i','a_f','status']
    #replace the mass values in these columns with rounded ones as having problems due to rounding error
    
    datae['M'].where(~(datae['M']==0.0005859298218282),0.00058593,inplace=True) 
    datae['M'].where(~(datae['M']==0.000773363144514),0.000773363,inplace=True) 
    datas['M'].where(~(datas['M']==0.0005859298218282),0.00058593,inplace=True) 
    datas['M'].where(~(datas['M']==0.000773363144514),0.000773363,inplace=True)
    
    #import  extension to simulation B
    dataex=pd.read_csv(sys.path[1]+"simulation_data/results_groupB_extended.csv")
    dataex.columns=['M','a_i','a_f','status'] 
    
    #concatenate data frames
    data=pd.concat([datas,dataf,datae,dataex],ignore_index=True) #ignore index to avoid duplicated values
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