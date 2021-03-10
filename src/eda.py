import pandas as pd
import numpy as np
from sys import path
path.append('.')
import os
path.append(os.getcwd())

# 660 schools across each profile
profile_1819 = pd.read_csv('data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv')
# 95 columns
hs_1819 = profile_1819[profile_1819['Is_High_School']==True]


profile_1718 = pd.read_csv('data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1718.csv')
# 92 columns

profile_1617 = pd.read_csv('data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1617.csv')
# 91 columns

