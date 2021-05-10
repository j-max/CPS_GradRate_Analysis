import pandas as pd
import numpy as np
import os, sys
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)


file_path_201819_sp = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv'

file_path_201718_sp = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1718.csv'

file_path_201617_sp = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv'


years = ['2018-2019', '2017-2018', '2016-2017']
paths = [file_path_201819_sp, file_path_201718_sp, file_path_201617_sp]

def create_sp_path_dictionary(years, paths):

    sp_path_dicitonary = {y:p for y,p in zip(years, paths)}

    return sp_path_dicitonary

def import_multiple_sy_profiles(sp_paths):

    sy_dictionary = {}
    for year in sp_paths:
        sy_dictionary[year] = pd.read_csv(sp_paths[year])

    return sy_dictionary

