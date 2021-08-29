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


class SchoolYear():

    '''

    Params:
    path_to_sp_csv: Path to a School Profile csv
    path_to_pr_csv: Path to a Progress Report csv from the same year as above

    '''

    def __init__(self, path_to_sp_csv, path_to_pr_csv):

        '''
        Initialize SchoolYear object with a path to
        a school profile csv and a progress report csv.
        '''

        self.path_to_sp_csv = path_to_sp_csv
        self.path_to_pr_csv = path_to_pr_csv
        self.sp_df = pd.read_csv(self.path_to_sp_csv)
        self.pr_df = pd.read_csv(self.path_to_pr_csv)
        self.merged_df = self.merge_pr_and_sp()
        self.total_high_school_count = self.merged_df['Is_High_School'].sum()
        self.total_school_count = len(sy_1819.merged_df['School_ID'].unique())


    def merge_pr_and_sp(self):

        '''
        The two main sources of data for this project come from
        School Profile csv and the Progress report csv.

        This function merges the two on the School_ID column.

        Returns:
        merged_df: A dataframe with all of the columns from both
        the school profile and progress report csvs
        '''

        self.merged_df = self.sp_df.merge(self.pr_df, on='School_ID', suffixes= ('_sp', '_pr') )

        # make a copy so that originals can be compared to preprocessed df

        return self.merged_df


    def convert_is_high_school_to_bool(self):
        '''
        Some of the School Year profiles' Is_High_School columns are encoded as booleans,
        df some as Y/N.  This function encodes them all as booleans.
        '''

        if self.merged_df['Is_High_School'].dtype == 'O':
            # Convert y/n to True/False
            self.merged_df['Is_High_School'] = self.merged_df['Is_High_School'].map({'Y':True, 'N':False})

        return self.merged_df

    def make_percent_low_income(self):

        '''
        Create new column which is percent of the total population which is low income.

        Parameters:
        self.merged_df: dataframe of school id's with low income population count.

        Returns:
        A dataframe with a per_low_income column added to it.
        '''

        self.merged_df['perc_low_income'] = 0

        self.merged_df['perc_low_income'] = self.merged_df['Student_Count_Low_Income']/self.merged_df['Student_Count_Total']

        self.merged_df.fillna({'perc_low_income': 0}, inplace=True)

        return self.merged_df


    def isolate_high_schools(self):

        self.merged_df = self.merged_df[self.merged_df['Is_High_School'] == True]

        return self.merged_df


    def drop_no_gr_schools(self):

        '''
        Drop schools from the dataframe that do not have graduation rates.
        This function is meant to be called after isolating high schools.

        Many of the high schools without graduation rates are charter schools.
        For example, YCCS (Youth Connection Charter Schools).
        '''

        self.merged_df.dropna(subset=['Graduation_Rate_School'], inplace=True)

        return self.merged_df


    def drop_specialed_options(self, drop_options=True):

        '''
        Special Education and Citywide Options schools have different
        missions and do not prioritize graduation rates.  They report
        graduation rates means below 20%.

        parameters:
        self.merged_df: a dataframe with both school profile and progress report
        data merged together.

        drop_options: a boolean that, if True, drops schools
        with School-Type='Citywide-Options'

        Returns:
        self.merged_df: dataframe with schools that have graduation rates
        suitable for modeling.
        '''
        
        if drop_options:

            self.merged_df = self.merged_df[~self.merged_df['School_Type'].isin(
                        ['Citywide-Option', 'Special Education'])]

            return self.merged_df

        else:

            self.merged_df = self.merged_df[~self.merged_df['School_Type'].isin(
                        ['Special Education'])]

            return self.merged_df

    def creative_school_encoding(self, drop=True, drop_column='EMERGING'):

        '''
        The creative school certification shows a statistically significant
        effect on graduation rates based on visual inspection and an ANOVA test.

        This function One Hot Encodes the 'Creative_School_Certification' column.

        Parameters:
        self.merged_df: dataframe of school id's with Creative_School_Certification column.

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
                                    self.merged_df[['Creative_School_Certification']]), 
                                index=self.merged_df.index, 
                                columns = ohe_csc.get_feature_names(['creative']))

            self.merged_df = self.merged_df.merge(csc_ohe, left_index=True, right_index=True)
            self.merged_df.drop('Creative_School_Certification', axis=1, inplace=True)

            return self.merged_df


    def prep_teacher_attendance(self):

        '''
        Teacher attendance is recorded for two years in the progress report.
        For example, school year 18-19 will have teacher attendance rates
        for 2018 and 2019.

        This function takes the average across the two years.
        '''

        self.merged_df['teacher_attendance'] = (self.merged_df['Teacher_Attendance_Year_1_Pct'] +\
                                        self.merged_df['Teacher_Attendance_Year_2_Pct'])/2


        return self.merged_df

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



    def remove_no_student_count_schools(self):

        '''
        If a school does not have any students recorded in the school year profile, remove the school.
        '''

        self.merged_df = self.merged_df[self.merged_df['Student_Count_Total'] > 0]

        return self.merged_df 

    def create_df_for_modeling(self):

        self.isolate_high_schools()
        self.drop_no_gr_schools()
        self.drop_specialed_options()
        self.make_percent_low_income()
        self.creative_school_encoding()
        self.prep_teacher_attendance()
        self.remove_no_student_count_schools()

        return self.merged_df 



### Tests

sy_1819 = SchoolYear('../../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv', '../../data/chicago_data_portal_csv_files/.ipynb_checkpoints/Chicago_Public_Schools_-_School_Progress_Reports_SY1819-checkpoint.csv')

# df_1819 = sy_1819.create_df_for_modeling()
