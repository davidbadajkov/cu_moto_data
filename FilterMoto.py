import pandas as pd
import numpy as np

def filter_data(df,type_moto=None,power_moto=None,brand_moto=None):
    '''
    Function to filter the final dataframe. The user provides the dataframe and a type of motorcycle, and/or power, and/or brand.
    
    Args:
    df : User must provide a pandas dataframe.
    type_moto (str): Optional, default is all types. Otherwise, provide a valid string, example: 'Enduro'
    power_moto (str) : Optional, default is all kind of powers. Otherwise, provide a valid string. Example: 'meer dan 35 kW'
    brand_moto (str) : Optional, default is all brands available. Otherwise, provide a valid string. Example : 'BMW'
    
    Returns: Based on the input, the function returns a filtered pandas dataframe sorted by the best deal.
    
    '''
    if type_moto == None:
        filter_type_moto = df['type'].unique()
    else:
        filter_type_moto = [type_moto]
    
    if power_moto == None:
        filter_power_moto = df['power'].unique()
    else:
        filter_power_moto = [power_moto]
    
    if brand_moto == None:
        filter_brand_moto = df['brand'].unique()
    else:
        filter_brand_moto = [brand_moto]
    
    df = df[df['type'].isin(filter_type_moto)]
    df = df[df['power'].isin(filter_power_moto)]
    df = df[df['brand'].isin(filter_brand_moto)]
    
    df = df[['id','metric','price_eur','km','age','cc','brand','type','power','title','location']]
    df = df.sort_values('metric',ascending = True)
    
    return df