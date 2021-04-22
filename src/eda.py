import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from sys import path
import os

full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
path.append(root)

# 660 schools across each profile
# 95 columns
profile_1819 = pd.read_csv('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv')

# Since graduation rates are only applicable to high schools
# I subset on the `Is_High_School` column.
hs_1819 = profile_1819[profile_1819['Is_High_School']==True]

# Repeat for each school profile
profile_1718 = pd.read_csv('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1718.csv')
# Is_High_School is coded as Y/N in 1718, not a boolean as in 1819
hs_1718 = profile_1718[profile_1718['Is_High_School']=='Y']


hs_dict = {'1819':hs_1819, '1718':hs_1718}
##########Graduation Rate##########

# Target column for machine learning regression models will be graduation rate
graduation_rate_1819 = hs_1819['Graduation_Rate_School']
graduation_rate = hs_1718['Graduation_Rate_School']

for year in hs_dict:
    print(f"""
        For all records in the {year} school year, there are {
        hs_dict[year]["Graduation_Rate_School"].isna().sum()}
        na values 
    """)
    print("####################") 


for year in hs_dict:
    print(f"""
        The mean graduation rate for the {year} school year is {
        hs_dict[year]["Graduation_Rate_School"].dropna().mean()}
        na values 
    """)
    print("####################") 



# Distribution is left skewed with a mean of ~72
fig, ax = plt.subplots()
ax.hist(graduation_rate_1819)
ax.set_title('Graduation Rate for 2018-19 School Year')
ax.axvline(graduation_rate_1819.mean(), color='r')

print(f"""
2018-19 Records
Original number of schools: {profile_1819.shape[0]}
Number of high schools: {hs_1819.shape[0]}
""")

########### Years prior to 1819 school year 
