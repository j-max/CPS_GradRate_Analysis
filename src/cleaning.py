import os
import sys
import pandas as pd

from src.feature_engineering import convert_is_high_school_to_bool
from src.feature_engineering import delta_student_count
from src.feature_engineering import is_charter
from src.feature_engineering import is_isp
from src.feature_engineering import make_percent_demographics
from src.feature_engineering import northwest_quadrant

from src.feature_lists import STUDENT_POP_FEATURE_LIST
from src.feature_lists import STUDENT_POP_PERC_LIST

from src.filtering import isolate_high_schools
from src.filtering import drop_no_students
from src.filtering import drop_no_grad_rate
from src.filtering import filter_cwoption_special_ed


FULL_PATH = os.getcwd()
HOME_FOLDER = 'CPS_GradRate_Analysis'
ROOT = FULL_PATH.split(HOME_FOLDER)[0] + HOME_FOLDER + '/'
EDA = FULL_PATH.split(HOME_FOLDER)[0] + HOME_FOLDER + '/' + 'notebooks/eda/'

sys.path.append(ROOT)


def prep_high_school_dataframe(path_to_sp, path_to_pr,
                               path_to_prior_year_sp,
                               path_to_prior_year_pr,
                               isolate_main_nw=False,
                               new_year_added='1718',
                               remove_outliers=True):

    '''
    This function uses the functions above to prep a dataframe for modeling
    high school graduation rates.
    
    It incorporates functions from the filtering and feature_engineering 
    modules. 
    
    The result of these functions is a dataframe of CPS High Schools
    that exclude those with objectives that don't directly align with 
    increasing graduation rates.  
    
    They also create new features from quantitative demographic counts.
        
    Parameters:
        path_to_sp: path to the most recent School Profile csv.
        path_to_pr: path to the most recent Progress Report csv.
        path_to_prior_year_sp: path to the 2nd most recent School Profile csv.
        path_to_prior_year_pr: path to the 2nd most recent Progress Report csv.
        isolate_main_nw: a boolean to remove all schools outside 
             of the main networks (14-17)
        new_year_added: a string used to append suffixes 
            to duplicate columns after merging prior to current year csv's.
        remove_outliers: a boolean set to True to remove Options, special ed schools, 
            and schools whose records are missing graduation rates.
     
    Return:
        df: A dataframe intended to be used with regression modeling 
        with Graduation_Rate_School as the target. The dataframe has
        outliers removed, features engineered from current and prior 
        years, and contains only high schools. 

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
    df['nw_quadrant'] = df.apply(northwest_quadrant, axis=1)
    df['is_charter'] = df['Network'].apply(is_charter)
    df['is_isp'] = df['Network'].apply(is_isp)

    # Select only Networks 14, 15, 16, 17
    if isolate_main_nw==True:
        return isolate_main_networks(df)

    if remove_outliers:
        return filter_cwoption_special_ed(df)
    
    return df


def import_and_merge_data(path_to_sp_csv, path_to_pr_csv):

    'Simple merge of two school csv files'

    sp_df = pd.read_csv(path_to_sp_csv)
    pr_df = pd.read_csv(path_to_pr_csv)

    merged_df = sp_df.merge(pr_df, on='School_ID', suffixes=('_sp', '_pr'))

    return merged_df
