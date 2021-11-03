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
    print(str(merged_df[merged_df['Student_Count_Total'] == 0].shape[0]) +
          ' schools')
    print(merged_df[merged_df['Student_Count_Total'] == 0]["Short_Name_sp"])

    merged_df = merged_df[merged_df['Student_Count_Total'] > 0]

    if merged_df[merged_df['Student_Count_Total'] == 0].shape[0] == 0:
        print('All 0 Student Count Schools Dropped')

    return merged_df


def drop_no_grad_rate(merged_df):

    '''
    Drop schools from a merged dataframe that do not have graduation rates.
    '''

    print("0 Graduation Rate")
    print(str(merged_df[merged_df['Graduation_Rate_School'] == 0].shape[0]) +
          " schools")
    print(merged_df[merged_df['Graduation_Rate_School'] == 0]["Short_Name_sp"])
    print('##########')
    print('NA Graduation Rates')
    print(str(merged_df[merged_df['Graduation_Rate_School'].isna()].shape[0]) + " schools")

    merged_df = merged_df[merged_df['Graduation_Rate_School'] > 0]


    if merged_df[merged_df['Graduation_Rate_School'] == 0].shape[0]==0:
        print('All 0/NA Graduation Rate Schools Dropped')

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

def isolate_numeric_columns(merged_df, add_grad_rates=True):

    sy_numerical_independent_features = ["perc_low_income", 
        "Student_Count_Total",  "Student_Count_Low_Income",
        "Student_Count_Special_Ed", "Student_Count_English_Learners",
        "Student_Count_Black", "Student_Count_Hispanic",
        "Student_Count_White",  "Student_Count_Asian",
        "Student_Count_Native_American", "Student_Count_Other_Ethnicity",
        "Student_Count_Asian_Pacific_Islander", "Student_Count_Multi",
        "Student_Count_Hawaiian_Pacific_Islander",
        "Student_Count_Ethnicity_Not_Available"]

    if add_grad_rates:
        sy_numerical_independent_features.append('Graduation_Rate_School')

    return merged_df[sy_numerical_independent_features]

def isolate_important_columns(merged_df):

    """
    There are a large number of columns in the dataset that
    are not used. This function isolates the most important columns.

    One reason for dropping the columns will be to allow
    for feature selection view recursive feature elimination
    and other methods
    """

    # These columns are consistent across 2016-2019 School Years
    sy_id_columns = ["School_ID", "Short_Name_sp"]

    
    target = ["Graduation_Rate_School"]

    sy_boolean_important = ['Is_High_School', 'Dress_Code', "Is_High_School",
                            "Is_Middle_School", "Is_Elementary_School", "Is_Pre_School",
                            "Dress_Code", "PreK_School_Day", "Kindergarten_School_Day",
                            "Bilingual_Services", "Refugee_Services", "Title_1_Eligible",
                            "PreSchool_Inclusive", "Preschool_Instructional",
                            "Significantly_Modified", "Hard_Of_Hearing", "Visual_Impairments"]

    categorical_important = ["School_Type", 'Network', "Primary_Category_sp",
                             "Grades_Offered", "After_School_Hours",
                             "Earliest_Drop_Off_Time", "Classroom_Languages",
                             ]

    return merged_df[sy_important_columns + pr_important_columns]

def isolate_main_networks(merged_df):

    main_networks = ['Network 14', 'Network 15', 'Network 16', 'Network 17']
    main_network_df = merged_df[merged_df['Network'].isin(main_networks)]

    return main_network_df

def prep_high_school_dataframe(path_to_sp, path_to_pr, isolate_main_nw=False):

    '''
    This function uses the functions above to prep a dataframe for modeling
    high school graduation rates.
    '''


    df = import_and_merge_data(path_to_sp, path_to_pr)
    df = convert_is_high_school_to_bool(df)
    df = isolate_high_schools(df)
    df = drop_no_students(df)
    df = drop_no_grad_rate(df)
    # df = isolate_important_columns(df)
    df = make_percent_low_income(df)

    # Select only Networks 14, 15, 16, 17
    if isolate_main_nw==True:
        return isolate_main_networks(df)

    return df


