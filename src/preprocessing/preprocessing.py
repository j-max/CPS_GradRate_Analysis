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


def create_sp_path_dictionary(year, paths):


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

def isolate_high_schools(sy_df):

    if sy_df['Is_High_School'].dtype == 'O':
        # Convert y/n to True/False
        sy_df['Is_High_School'] = sy_df['Is_High_School'].map({'Y':True, 'N':False})


    sy_df = sy_df[sy_df['Is_High_School'] == True]

    return sy_df

sp_paths = create_sp_path_dictionary(years, paths)
df_dict = import_multiple_sy_profiles(sp_paths)

