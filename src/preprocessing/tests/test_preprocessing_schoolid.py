import pandas as pd
import os, sys
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)

from src.preprocessing.preprocessing_schoolid import remove_no_student_count_schools, merge_prepped_sy_profile_and_prog_rep

path_to_school_year_profile = '../../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv'
path_to_pr_csv = '../../data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Progress_Reports_SY1819.csv'



def test_remove_no_student_count_schools():

    df = pd.read_csv(path_to_school_year_profile)
    original_length = len(df)

    df = remove_no_student_count_schools(df)
    new_length = len(df)

    if df[df['Student_Count_Total'] == 0].shape[0] >= 1:
        assert new_length < original_length

def test_merge_prepped_sy_profile_and_prog_rep():

    merged_df = merge_prepped_sy_profile_and_prog_rep(path_to_school_year_profile, path_to_pr_csv)

    assert merged_df.shape == (136, 23)
