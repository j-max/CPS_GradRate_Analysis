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

from src.schools import SchoolProfiles

sy_1819 = SchoolProfiles()

sy_1819.read_profile('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv')

sy_1819.read_prog_report('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Progress_Reports_SY1819.csv')

# 660 schools across each profile
# 95 columns
profile_1819 = pd.read_csv('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv')

#grad_rate_1819=profile_1819['Graduation_Rate_School']
#profile_1819.drop('Graduation_Rate_School', axis=1, inplace=True)
#profile_1819.insert(0, 'Graduation_Rate_School', grad_rate_1819)

# Repeat for each school profile
profile_1718 = pd.read_csv('../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1718.csv')

#grad_rate_1718=profile_1718['Graduation_Rate_School']
#profile_1718.drop('Graduation_Rate_School', axis=1, inplace=True)
#profile_1718.insert(0, 'Graduation_Rate_School', grad_rate_1718)

profile_dicts = {'1819':profile_1819, '1718':profile_1718}

for year in profile_dicts:
    grad_rate=profile_dicts[year]['Graduation_Rate_School']
    profile_dicts[year].drop('Graduation_Rate_School', axis=1, inplace=True)
    profile_dicts[year].insert(0, 'Graduation_Rate_School', grad_rate)


# Since graduation rates are only applicable to high schools
# I subset on the `Is_High_School` column.
hs_1819 = profile_1819[profile_1819['Is_High_School']==True]

# Is_High_School is coded as Y/N in 1718, not a boolean as in 1819
hs_1718 = profile_1718[profile_1718['Is_High_School']=='Y']


hs_dict = {'1819':hs_1819, '1718':hs_1718}
##########Graduation Rate##########

# Target column for machine learning regression models will be graduation rate
graduation_rate_1819 = hs_1819['Graduation_Rate_School']
graduation_rate_1718 = hs_1718['Graduation_Rate_School']


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
def grad_plotter():
    fig, ax = plt.subplots()
    ax.hist(graduation_rate_1819)
    ax.set_title('Graduation Rate for 2018-19 School Year')
    ax.axvline(graduation_rate_1819.mean(), color='r')

    plt.show()



print(f"""
2018-19 Records
Original number of schools: {profile_1819.shape[0]}
Number of high schools: {hs_1819.shape[0]}
""")

##########Correlations##########

hs_1819.corr()['Graduation_Rate_School'].sort_values()

'''
feature_mask = [
Is_Elementary_School                      -4.525411e-02
Is_Pre_School                             -7.275555e-03
School_Latitude                            1.114710e-02
Attendance_Boundaries                      1.866599e-02
Zip                                        3.746629e-02
Is_Middle_School                           4.516552e-02
Dress_Code                                 9.229378e-02
School_Longitude                           9.978306e-02
Student_Count_Asian_Pacific_Islander       1.254034e-01
Student_Count_English_Learners             1.525532e-01
Student_Count_Ethnicity_Not_Available      1.580427e-01
Student_Count_Hawaiian_Pacific_Islander    1.983118e-01
Student_Count_Special_Ed                   2.088732e-01
Student_Count_White                        2.107417e-01
Student_Count_Black                        2.244583e-01
Student_Count_Asian                        2.474511e-01
Student_Count_Native_American              2.620670e-01
Student_Count_Multi                        2.675798e-01
Student_Count_Hispanic                     3.383062e-01
Student_Count_Low_Income                   4.255831e-01
Student_Count_Total                        4.344694e-01
Is_GoCPS_High_School                       8.085954e-01
Is_GoCPS_Participant                       8.085954e-01
College_Enrollment_Rate_School             8.382556e-01
Graduation_Rate_School                     1.000000e+00
Student_Count_Other_Ethnicity                       NaN
Is_GoCPS_PreK                                       NaN
Closed_For_Enrollment_Date                          NaN
]
'''

##########Feature Exploration 1819##########
print(hs_1819['Is_Pre_School'].value_counts())
print('There is only 1 high school which is also a preschool')

print(hs_1819['Is_Pre_School'].value_counts())

print(hs_1819['Is_Elementary_School'].value_counts())
print("15 high schools are also elementary schools")

print(hs_1819['Is_Middle_School'].value_counts())
print("29 high schools are also middle schools")

print(hs_1819['Dress_Code'].value_counts())
print('63 schools have dress codes')


