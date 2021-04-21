import pandas as pd
import numpy as np
from sys import path
import os

full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
path.append(root)

# 660 schools across each profile
profile_1819 = pd.read_csv('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv')
# 95 columns
hs_1819 = profile_1819[profile_1819['Is_High_School']==True]

# The profile csv for 1718 need headers
profile_1718 = pd.read_csv('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1718.csv')
# 92 columns

# Target column for machine learning regression models will be graduation rate
graduation_rate = profile_1819['Graduation_Rate_School']

print(f"""For all records in the 1819 school year, there are {
                                    graduation_rate.isna().sum()
                                    } na values""")

# Since graduation rates are only applicable to high schools
# I subset on the `Is_High_School` column.

hs_1819 = profile_1819[profile_1819['Is_High_School']==True]

print(f"""
2018-19 Records
Original number of schools: {profile_1819.shape[0]}
Number of high schools: {hs_1819.shape[0]}
""")

########### Years prior to 1819 school year 
