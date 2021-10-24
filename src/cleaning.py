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

    'Simple merge of two school csv files'

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



def convert_is_high_school_to_bool(merged_df):

    '''
    Some of the School Year profiles' Is_High_School columns are encoded as booleans,
    df some as Y/N.  This function encodes them all as booleans.
    '''

    if merged_df['Is_High_School'].dtype == 'O':
        # Convert y/n to True/False
        merged_df['Is_High_School'] = merged_df['Is_High_School'].map({'Y':True, 'N':False})

    return merged_df

def make_percent_low_income(merged_df):

    '''
    Create new column which is percent of the total population which is low income.

    Parameters:
    self.merged_df: dataframe of school id's with low income population count.

    Returns:
    A dataframe with a per_low_income column added to it.
    '''

    merged_df['perc_low_income'] = 0

    merged_df['perc_low_income'] = merged_df['Student_Count_Low_Income']/merged_df['Student_Count_Total']

    merged_df.fillna({'perc_low_income': 0}, inplace=True)

    return merged_df


def isolate_high_schools(merged_df):

    merged_df = merged_df[merged_df['Is_High_School'] == True]

    return merged_df


def isolate_important_columns(merged_df):

    # These columns are consistent across 2016-2019 School Years
    sy_important_columns = [ "School_ID","Short_Name","Graduation_Rate_School",
                    "Student_Count_Total", "Student_Count_Low_Income",
                    "Student_Count_Special_Ed","Student_Count_English_Learners",
                    "Student_Count_Black","Student_Count_Hispanic",
                    "Student_Count_White", "Student_Count_Asian",
                    "Student_Count_Native_American","Student_Count_Other_Ethnicity",
                    "Student_Count_Asian_Pacific_Islander","Student_Count_Multi",
                    "Student_Count_Hawaiian_Pacific_Islander",
                    "Student_Count_Ethnicity_Not_Available", 'Is_High_School', 'Dress_Code',
                    "Classroom_Languages","Transportation_El"]


    pr_important_columns = ["School_ID", "School_Type"]

    return merged_df[sy_df_important_columns + pr_important_columns]

