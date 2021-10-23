import pandas as pd
pd.set_option('display.max_columns', None)

import numpy as np
import os, sys
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
eda = full_path.split(home_folder)[0] + home_folder + '/' + 'notebooks/eda/'

sys.path.append(root)



def import_and_merge_data(path_to_sp_csv, path_to_pr_csv):

        sp_df = pd.read_csv(path_to_sp_csv)
        pr_df = pd.read_csv(path_to_pr_csv)

        merged_df = sp_df.merge(pr_df, on='School_ID', suffixes= ('_sp', '_pr') )

        return merged_df

def drop_no_students(merged_df):


    '''
    Drop schools from a merged dataframe that do not have student counts.
    '''

    print("0 Student Count")
    print(str(merged_df[merged_df['Student_Count_Total'] == 0].shape[0]) + ' schools')
    print(merged_df[merged_df['Student_Count_Total'] == 0]["Short_Name_sp"])

    merged_df = merged_df[merged_df['Student_Count_Total'] > 0]


    if merged_df[merged_df['Student_Count_Total'] == 0].shape[0]==0:
        print('All 0 Student Count Schools Dropped')

    return merged_df

def drop_no_grad_rate(merged_df):

    ''' 
    Drop schools from a merged dataframe that do not have graduation rates.
    ''' 

    print("0 Graduation Rate")
    print(str(merged_df[merged_df['Graduation_Rate_School'] == 0].shape[0]) + " schools")
    print(merged_df[merged_df['Graduation_Rate_School'] == 0]["Short_Name_sp"])

    merged_df = merged_df[merged_df['Graduation_Rate_School'] > 0]


    if merged_df[merged_df['Graduation_Rate_School'] == 0].shape[0]==0:
        print('All 0 Graduation Rate Schools Dropped')

    return merged_df

