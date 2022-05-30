# -*- coding: utf-8 -*-
"""
Function for error fernandes planet occurence rate for a given mass and semimajor axis
Uses the mean values from Fernandes et al. 2019 
Assume the progenitor star was 1Msol
Assumes the errors are Gaussian and uses the average value of each error

:param a: float or np.array, semi major axis [au]
:param M: float or np.array, mass [MJup]
:param array: str, mass or a, decide which value is constant and which will be iterated over,
                    default is a

:returns error: array error(P) -error in d^2Nms/dloga dlogM
"""
def fern_plan_error(a,M,array='a'):
    
    import numpy as np
    
    #check correct datatypes
    if array=='a' and type(a)!=np.ndarray:
        raise TypeError('a must be a numpy array')
    elif array=='mass' and type(M)!=np.ndarray:
        raise TypeError('M must be a numpy array')
    else:
        pass #yay our arrays have been correctly specified
    
    #define constants 
    p_break=1581 # [days]
    k=3/2*0.65 # transform by 3/2 as gone from P to a
    year=365.25 # [days]
    c0=2/3*0.84 #factor of 2/3 as dlogP=3/2 dloga
    m1=-0.45
    m_earth=5.976e24 #[kg]
    m_jup=1.898e27 #[kg]
    mconst=10*m_earth/m_jup # [convert to Jupiter masses for consistency in mass values]
    a_break=((p_break/year)**2)**(1/3) 
    
    #define errors - multiplicative factors required to scale errors as above
    dc0=2/3*0.165 
    dm1=0.05
    dk=3/2*0.175
    da_break=0.607
    
    #constant errors
    e1_sq=(dc0/c0)**2
    e2_sq=(k*da_break/a_break)**2
   
    if array=='a': #array is a, m is const
        a_len=len(a)
        #create array for output
        f=np.zeros([a_len])
        error=np.zeros([a_len])
        for x in range(a_len): #could maybe make this faster using arrays but will only run this once to build inputs so its ok
            if a[x] < a_break:
                f[x] = c0*(a[x]/a_break)**k*(M/mconst)**m1 
                
            else:
                f[x] = c0*(a[x]/a_break)**(-k)*(M/mconst)**m1
            error[x]=f[x]*np.sqrt(e1_sq+e2_sq+np.log(a[x]/a_break)**2*dk**2+np.log(M/mconst)**2*dm1**2)
   
    elif array =='mass': #array of masses const a
             
        if a < a_break:
            f = c0*(a/a_break)**k*(M/mconst)**m1 
        else:
            f = c0*(a/a_break)**(-k)*(M/mconst)**m1
            
        error=f*np.sqrt(e1_sq+e2_sq+np.log(a/a_break)**2*dk**2+np.log(M/mconst)**2*dm1**2)
    else:
         raise ValueError('invalid choice of array type - must be a or mass')
    
    return error
    
    





