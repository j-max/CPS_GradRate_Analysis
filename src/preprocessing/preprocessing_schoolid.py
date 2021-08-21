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

def merge_pr_and_sp(path_to_sp_csv, path_to_pr_csv):

    '''
    The two main sources of data for this project come from
    School Profile csv and the Progress report csv.

    This function merges the two on the School_ID column.

    Parameters:
    path_to_sp_csv: path to the School Profile csv
    path_to_pr_csv: path to the Progress Report csv

    Returns:
    merged_df: A dataframe with all of the columns from both
    the school profile and progress report csvs
    '''
    sp_df = pd.read_csv(path_to_sp_csv)
    pr_df = pd.read_csv(path_to_pr_csv)

    merged_df = sp_df.merge(pr_df, on='School_ID', suffixes= ('_sp', '_pr') )

    return merged_df

def isolate_high_schools(merged_df):

    merged_df = merged_df[merged_df['Is_High_School'] == True]

    return merged_df


def drop_no_gr_schools(merged_df):

    '''
    Drop schools from the dataframe that do not have graduation rates.
    This function is meant to be called after isolating high schools.

    Many of the high schools without graduation rates are charter schools.
    For example, YCCS (Youth Connection Charter Schools).
    '''

    merged_df.dropna(subset=['Graduation_Rate_School'], inplace=True)

    return merged_df
 
def drop_specialed_options(merged_df, drop_options=True):

    '''
    Special Education and Citywide Options schools have different
    missions and do not prioritize graduation rates.  They report
    graduation rates means below 20%.

    parameters:
    merged_df: a dataframe with both school profile and progress report
    data merged together.

    drop_options: a boolean that, if True, drops schools
    with School-Type='Citywide-Options'

    Returns:
    merged_df: dataframe with schools that have graduation rates
    suitable for modeling.
    '''

    if drop_options:

        merged_df = merged_df[~merged_df['School_Type'].isin(
                     ['Citywide-Option', 'Special Education'])]

        return merged_df

    else:

        merged_df = merged_df[~merged_df['School_Type'].isin(
                     ['Special Education'])]

        return merged_df

def make_percent_low_income(merged_df):

    '''
    Create new column which is percent of the total population which is low income.

    Parameters:
    merged_df: dataframe of school id's with low income population count.

    Returns:
    A dataframe with a per_low_income column added to it.
    '''

    merged_df['perc_low_income'] = 0

    merged_df['perc_low_income'] = merged_df['Student_Count_Low_Income']/merged_df['Student_Count_Total']

    merged_df.fillna({'perc_low_income': 0}, inplace=True)

    return merged_df

def creative_school_encoding(merged_df, drop=True, drop_column='EMERGING'):

    '''
    The creative school certification shows a statistically significant
    effect on graduation rates based on visual inspection and an ANOVA test.

    This function One Hot Encodes the 'Creative_School_Certification' column.

    Parameters:
    merged_df: dataframe of school id's with Creative_School_Certification column.

    drop: parameter to designate dropping a column.  To be set to true with
    vanilla linear regression models.

    drop_column:  The column to drop.  Set by default to 'EMERGING' so that the
    regression coefficients will be positive in relation to the lowest certificate
    achievement category.

    Returns:
    Dataframe with a one_hot_encoded version of Creative_School_Certification
    and the original column dropped.

    '''

    if drop:
        ohe_csc = OneHotEncoder(drop=['EMERGING'], sparse=False )

        csc_ohe = pd.DataFrame(
                            ohe_csc.fit_transform(
                                merged_df[['Creative_School_Certification']]), 
                            index=merged_df.index, 
                            columns = ohe_csc.get_feature_names(['creative']))

        merged_df = merged_df.merge(csc_ohe, left_index=True, right_index=True)
        merged_df.drop('Creative_School_Certification', axis=1, inplace=True)

        return merged_df


def prep_teacher_attendance(merged_df):

    '''
    Teacher attendance is recorded for two years in the progress report.
    For example, school year 18-19 will have teacher attendance rates
    for 2018 and 2019.

    This function takes the average across the two years.
    '''

    merged_df['teacher_attendance'] = (merged_df['Teacher_Attendance_Year_1_Pct'] +\
                                       merged_df['Teacher_Attendance_Year_2_Pct'])/2

 
    return merged_df

def create_df_for_modeling(merged_df):

    df = isolate_high_schools(merged_df)
    df = drop_no_gr_schools(df)
    df = drop_specialed_options(df)
    df = make_percent_low_income(df)
    df = creative_school_encoding(df)
    df = prep_teacher_attendance(df)

    return df


def isolate_important_columns(sy_df):

    # These columns are consistent across 2016-2019 School Years
    sy_df = sy_df[[ "School_ID","Short_Name","Graduation_Rate_School",
                    "Student_Count_Total", "Student_Count_Low_Income",
                    "Student_Count_Special_Ed","Student_Count_English_Learners",
                    "Student_Count_Black","Student_Count_Hispanic",
                    "Student_Count_White", "Student_Count_Asian",
                    "Student_Count_Native_American","Student_Count_Other_Ethnicity",
                    "Student_Count_Asian_Pacific_Islander","Student_Count_Multi",
                    "Student_Count_Hawaiian_Pacific_Islander",
                    "Student_Count_Ethnicity_Not_Available", 'Is_High_School', 'Dress_Code',
                    "Classroom_Languages","Transportation_El"]]

    return sy_df

def isolate_important_columns_pr_rep(pr_df):

    pr_df = pr_df[["School_ID", "School_Type"]]

    return pr_df

def convert_is_high_school_to_bool(sy_df):
    '''
    Some of the School Year profiles' Is_High_School columns are encoded as booleans,
    df some as Y/N.  This function encodes them all as booleans.
    '''

    if sy_df['Is_High_School'].dtype == 'O':
        # Convert y/n to True/False
        sy_df['Is_High_School'] = sy_df['Is_High_School'].map({'Y':True, 'N':False})

    return sy_df

def remove_no_student_count_schools(sy_df):

    '''
    If a school does not have any students recorded in the school year profile, remove the school.
    '''

    sy_df = sy_df[sy_df['Student_Count_Total'] > 0]

    return sy_df 

def load_prepped_school_year_profile(path_to_school_year_profile):

    '''
    There are 660 schools represented in the CPS Data Portal data files.

    141 of these are high schools. 

    '''
    df = pd.read_csv(path_to_school_year_profile)

    df = isolate_important_columns(df)
    df = convert_is_high_school_to_bool(df)
    df = isolate_high_schools(df)
    df = drop_no_gr_schools(df)
    df = make_percent_low_income(df)
    df = remove_no_student_count_schools(df)

    return df

def merge_prepped_sy_profile_and_prog_rep(path_to_school_year_profile,
                                           path_to_progress_report):

    df_sy = load_prepped_school_year_profile(path_to_school_year_profile)

    df_pr = pd.read_csv(path_to_progress_report)
    df_pr = isolate_important_columns_pr_rep(df_pr)
    df_merged = df_sy.merge(df_pr, on='School_ID')


    return df_merged


def load_unprocessed_hs_df(path_to_school_year_profile):

    df = pd.read_csv(path_to_school_year_profile)

    df = convert_is_high_school_to_bool(df)
    df = isolate_high_schools(df)

    return df


