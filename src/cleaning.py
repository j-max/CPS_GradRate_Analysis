import os
import sys
import pandas as pd

from src.feature_engineering import convert_is_high_school_to_bool
from src.feature_engineering import make_percent_demographics
from src.feature_engineering import delta_student_count

from src.feature_lists import STUDENT_POP_FEATURE_LIST
from src.feature_lists import STUDENT_POP_PERC_LIST

from src.filtering import isolate_high_schools
from src.filtering import drop_no_students
from src.filtering import drop_no_grad_rate


FULL_PATH = os.getcwd()
HOME_FOLDER = 'CPS_GradRate_Analysis'
ROOT = FULL_PATH.split(HOME_FOLDER)[0] + HOME_FOLDER + '/'
EDA = FULL_PATH.split(HOME_FOLDER)[0] + HOME_FOLDER + '/' + 'notebooks/eda/'

sys.path.append(ROOT)


def prep_high_school_dataframe(path_to_sp, path_to_pr,
                               path_to_prior_year_sp,
                               path_to_prior_year_pr,
                               isolate_main_nw=False,
                               new_year_added='1718'):

    '''
    This function uses the functions above to prep a dataframe for modeling
    high school graduation rates.
    '''


    df = import_and_merge_data(path_to_sp, path_to_pr)
    df = convert_is_high_school_to_bool(df)
    df = isolate_high_schools(df)
    df = drop_no_students(df)
    df = drop_no_grad_rate(df)
    df = make_percent_demographics(df)
    df = delta_student_count(df, path_to_prior_year_sp,
                             path_to_prior_year_pr,
                             new_year_added=new_year_added)

    # Select only Networks 14, 15, 16, 17
    if isolate_main_nw==True:
        return isolate_main_networks(df)
    
    return df


def import_and_merge_data(path_to_sp_csv, path_to_pr_csv):

    'Simple merge of two school csv files'

    sp_df = pd.read_csv(path_to_sp_csv)
    pr_df = pd.read_csv(path_to_pr_csv)

    merged_df = sp_df.merge(pr_df, on='School_ID', suffixes=('_sp', '_pr'))

    return merged_df
