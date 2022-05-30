# -*- coding: utf-8 -*-
"""
Function to convert imported data from big endian to little endian

:params data: data from a fits file (got from new_data=fits.open(), 
                                     data=new_data[1]), containing a table. Data is of big endian type
:param N: number of columns in data frame

:returns: dataframe with all data little endian type
"""

def endian_converter(datafile,N):
    import pandas as pd
    
    #get the actual data
    data=datafile.data
    headers=datafile.header
    
    #create a dictionary to store values
    data_dict={}
    #change endianness and replace in dictionary to make new data frame
    for i in range(N):
        data_swapped=data['{}'.format(headers[8+2*i])].byteswap().newbyteorder() #take every second key after 9 - these correspond to TFORMi 
        data_dict['{}'.format(headers[8+2*i])]=data_swapped
    
    data_frame=pd.DataFrame(data_dict)
    return data_frame
    
