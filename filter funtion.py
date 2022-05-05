# sorry Jyputer in my labtop dosn't work, I just use python file to do that.
from asyncio.windows_events import NULL
from logging import NullHandler
from pickle import NONE
import re
import csv
import pandas as pd
from pkg_resources import resource_listdir

csvfile = open("database_moto_updated.csv") # or which the file is right?
csv_data = pd.read_csv(csvfile,low_memory=False)
csv_df = pd.DataFrame(csv_data)

Re = r"Sport"
Series.csv_df.contains(Re,case=False,flags=0,na=None,regex=True)

Type_set = c("Sport","Very sport","light") # sorry I did not find the cleaned data, so I don't know exactly how this set should be, please help me fix that
Power_set = c("5000","6000","8000")
Brands_set =  c("Yamaha","Benelli","Honda")

Type = "Sport" # this string here is what our customers enter into the filter box.
Re_T = print("r"+"\""+Type+"\"") # Re now equals to r"Sprot"
Bool_T = csv_df.type.str.contains(Re) # this type after df. is the name of column

Power = "5000" # I donnot konw the exactly power, please help me change later
Re_P = print("r"+"\""+Power+"\"")
Bool_P = csv_df.power.str.contains(Re)

Brands = "Yamaha"
Re_B = print("r"+"\""+Brands+"\"")
Bool_B = csv_df.brands.str.contains(Re)

result_index = csv_df.loc[(csv_df[Bool_T])&(csv_df[Bool_P])&(csv_df[Bool_B])]
result = csv_df.loc[:,result_index]

# There are two loop following, please help me choose a better one.
# loop 1
if Type != None:
    if  Power != None:
        if Brands !=None:
            result_index = csv_df.loc[(csv_df[Bool_T])&(csv_df[Bool_P])&(csv_df[Bool_B])]
            result = csv_df.loc[:,result_index]
        else:
            result_index = csv_df.loc[(csv_df[Bool_T])&(csv_df[Bool_P])]
            result = csv_df.loc[:,result_index]
    elif Brands != None:
        result_index = csv_df.loc[(csv_df[Bool_T])&(csv_df[Bool_B])]
        result = csv_df.loc[:,result_index]
    else:
        result_index = csv_df.loc[csv_df[Bool_T]]
        result = csv_df.loc[:,result_index]
elif Power != None:
    if Brands != None:
        result_index = csv_df.loc[(csv_df[Bool_P])&(csv_df[Bool_B])]
        result = csv_df.loc[:,result_index]
    else:
        result_index = csv_df.loc[(csv_df[Bool_P])]
        result = csv_df.loc[:,result_index]
elif Brands != None:
    result_index = csv_df.loc[(csv_df[Bool_B])]
    result = csv_df.loc[:,result_index]
else:
    result = csv_df

# loop 2
if Type != None & Power != None & Brands !=None:
    result_index = csv_df.loc[(csv_df[Bool_T])&(csv_df[Bool_P])&(csv_df[Bool_B])]
    result = csv_df.loc[:,result_index]
elif Type != None & Power != None:
    result_index = csv_df.loc[(csv_df[Bool_T])&(csv_df[Bool_P])]
    result = csv_df.loc[:,result_index]
elif Type != None & Brands != None:
    result_index = csv_df.loc[(csv_df[Bool_T])&(csv_df[Bool_B])]
    result = csv_df.loc[:,result_index]
elif Power != None & Brands !=None:
    result_index = csv_df.loc[(csv_df[Bool_P])&(csv_df[Bool_B])]
    result = csv_df.loc[:,result_index]
elif Type != None:
    result_index = csv_df.loc[csv_df[Bool_T]]
    result = csv_df.loc[:,result_index] 
elif Power != None:
    result_index = csv_df.loc[(csv_df[Bool_P])]
    result = csv_df.loc[:,result_index]
elif Brands !=None:
    result_index = csv_df.loc[(csv_df[Bool_B])]
    result = csv_df.loc[:,result_index]
else:
    result = csv_df


def filter(Type,Power,Brands,dataframe):
    loop 1 or loop 2
    return(result)
# dose thos code make any sense? we can discuss tomorrow.




