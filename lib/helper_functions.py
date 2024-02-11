import pandas as pd
import numpy as np
import glob
import os

# read csv, clean and optimize the dataframe and combine the dataframes into one
def read_clean_combine_csv(directory, df, exclude=None):
    excludepath = os.path.join(directory,exclude)
    print(excludepath)
    print()
    for csv_file in glob.glob(os.path.join(directory,'*')):
        if(excludepath != csv_file):
            df1 = pd.read_csv(csv_file)
            df1 = df1[df1['Protocol'] != 'Protocol']
            df1 = optimize_and_clean_df(df1)
            df = pd.concat([df,df1], ignore_index=True)
    df.rename(columns=lambda x: x.replace('/', ' ').replace(' ', '_').lower(), inplace=True)
    return df
    

def optimize_and_clean_df(df):
    # convert columns to correct data types
    df[df.columns.difference(['Dst Port','Protocol','Timestamp','Label'])] = df[df.columns.difference(['Dst Port','Protocol','Timestamp','Label'])].apply(pd.to_numeric, errors='coerce')
    df['Timestamp'] = pd.to_datetime(df.Timestamp, format="%d/%m/%Y %H:%M:%S")
    
    # reduce memory allocation of dataframe with function 
    df, NAlist = reduce_mem_usage(df)
    
    # categorize categorical columns for additional optimization
    df[['Dst Port','Protocol','Label']] = df[['Dst Port','Protocol','Label']].astype('category')
    
    # return dataframe
    return df
    
# taken from https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65
def reduce_mem_usage(props):
    start_mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = []  # Keeps track of columns that have missing values filled in.
    
    for col in props.columns:
        if props[col].dtype != object and props[col].dtype != 'datetime64[ns]':  # Exclude strings and datetime
            
            # Handle non-finite values
            props[col].replace([np.inf, -np.inf], np.nan, inplace=True)

            # make variables for Int, max, and min
            IsInt = False
            mx = props[col].max()
            mn = props[col].min()
            
            # Integer does not support NA, therefore, NA needs to be filled
            if not np.isfinite(props[col]).all():
                NAlist.append(col)
                props[col].fillna(mn-1, inplace=True)
                   
            # test if column can be converted to an integer
            asint = props[col].fillna(0).astype(np.int64)
            result = (props[col] - asint)
            result = result.sum()
            if result > -0.01 and result < 0.01:
                IsInt = True

            # Make Integer/unsigned Integer datatypes
            if IsInt:
                props[col] = pd.to_numeric(props[col], downcast='integer')
            
            # Make float datatypes 32 bit
            else:
                props[col] = props[col].astype(np.float32)
                
    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage is: ", mem_usg, " MB")
    print("This is ", 100 * mem_usg / start_mem_usg, "% of the initial size")
    return props, NAlist
