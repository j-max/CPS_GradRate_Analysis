import pandas as pd
pd.set_option('display.max_columns', None)

import numpy as np
import os, sys


full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)


years = ['2018-2019', '2017-2018', '2016-2017', '2015-2016']


file_path_201819_sp = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv'

file_path_201718_sp = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1718.csv'

file_path_201617_sp = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv'


paths = [file_path_201819_sp, file_path_201718_sp, file_path_201617_sp]


def create_sp_path_dictionary(years, paths):


    sp_path_dictionary = {y:'year_missing' for y in years}
    for y, p in zip(years, paths):
        sp_path_dictionary[y] = p

    return sp_path_dictionary

def import_multiple_sy_profiles(sp_paths):

    sy_dictionary = {}
    for year in sp_paths:
        if sp_paths[year] == 'year_missing':
            print(year + ' missing')
        else:
            sy_dictionary[year] = pd.read_csv(sp_paths[year])

    return sy_dictionary

def isolate_important_columns(sy_df):

    # These columns are consistent across 2016-2019 School Years
    sy_df = sy_df[[ "School_ID", "Graduation_Rate_School", "Student_Count_Total",
                    "Student_Count_Low_Income", "Student_Count_Special_Ed","Student_Count_English_Learners",
"Student_Count_Black","Student_Count_Hispanic","Student_Count_White",
"Student_Count_Asian","Student_Count_Native_American","Student_Count_Other_Ethnicity",
"Student_Count_Asian_Pacific_Islander","Student_Count_Multi","Student_Count_Hawaiian_Pacific_Islander",
                    "Student_Count_Ethnicity_Not_Available", 'Is_High_School', 'Dress_Code',
                    "Classroom_Languages","Transportation_El"]]

    return sy_df


def convert_is_high_school_to_bool(sy_df):
    '''
    Some of the School Year profiles' Is_High_School columns are encoded as booleans, some as Y/N.  This function encodes them all as booleans.
    '''

    if sy_df['Is_High_School'].dtype == 'O':
        # Convert y/n to True/False
        sy_df['Is_High_School'] = sy_df['Is_High_School'].map({'Y':True, 'N':False})

    return sy_df

def convert_dress_code_to_bool(sy_df):

    if sy_df['Dress_Code'].dtype == 'O':
        # Convert y/n to True/False
        sy_df['Dress_Code'] = sy_df['Dress_Code'].map({'Y':True, 'N':False})


    return sy_df

def isolate_high_schools(sy_df):

    sy_df = sy_df[sy_df['Is_High_School'] == True]

    return sy_df

sp_paths = create_sp_path_dictionary(years, paths)
df_dict = import_multiple_sy_profiles(sp_paths)

