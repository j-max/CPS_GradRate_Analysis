import pandas as pd

from src.feature_lists import STUDENT_POP_FEATURE_LIST
from src.feature_lists import STUDENT_POP_PERC_LIST


def convert_is_high_school_to_bool(merged_df):

    '''
    Some of the School Year profiles' Is_High_School columns are
    encoded as booleans, df some as Y/N.  This function encodes them
    all as booleans.

    '''

    if merged_df['Is_High_School'].dtype == 'O':
        # Convert y/n to True/False
        merged_df['Is_High_School_Bool'] = merged_df['Is_High_School'].map(
            {'Y': True, 'N': False})

    return merged_df


def make_percent_demographics(merged_df,
                              student_list=STUDENT_POP_FEATURE_LIST):

    '''
    Make demographic number proportions of overall student population.
    The features that are to be converted are found in
    STUDENT_POP_FEATURE_LIST found in the feature_list.py file.
    Examples are Student_Count_Low_Income, Student_Count_Special_Ed,
    and counts for racial demographics..
    '''

    for feature_name in STUDENT_POP_FEATURE_LIST:

        if feature_name == 'Student_Count_Total':
            continue

        perc_feature_name = 'perc_' + feature_name
        merged_df[perc_feature_name] = 0

        merged_df[perc_feature_name] = merged_df[feature_name] /\
            merged_df['Student_Count_Total']

        merged_df.fillna({perc_feature_name: 0}, inplace=True)

    return merged_df


def delta_student_count(merged_df,
                        path_to_prior_year_sp,
                        path_to_prior_year_pr,
                        new_year_added):
    '''Calculate the change in student count from previous year to present'''

    sp_df = pd.read_csv(path_to_prior_year_sp)
    pr_df = pd.read_csv(path_to_prior_year_pr)

    df_prior = sp_df.merge(pr_df, on='School_ID', suffixes=('_sp', '_pr'))

    df_prior_sct = df_prior[['School_ID', 'Student_Count_Total']]

    df_plus_delta_sc = pd.merge(merged_df, df_prior_sct,
                                how='left', on='School_ID',
                                suffixes=('', '_'+new_year_added))

    # Make sure no schools were lost in the merge
    assert (merged_df.shape[0] == df_plus_delta_sc.shape[0],
            'Merge lost schools')

    df_plus_delta_sc['student_count_total_change_1_year'] = (
        df_plus_delta_sc['Student_Count_Total'] -
        df_plus_delta_sc['Student_Count_Total_'+new_year_added])

    return df_plus_delta_sc


def northwest_quadrant(row,
                       longitude_column_name='School_Longitude_pr',
                       latitude_column_name='School_Latitude_pr'):

    '''The northwest quadrant of Chicago is negatively correlated to
    graduation rate.  This function creates a boolean that indicates
    if a school is in the northwest quadrant or not.

    Parameters: a row of a merged dataframe (meant to be used with an
    apply statement

    Returns: a boolean indicating if a school is in the northwest
    quadrant

    '''

    latitude_boundary = 41.825
    longitude_boundary = -87.68

    # () separating the & prevent Type Error
    if ((row[longitude_column_name] < longitude_boundary) &
            (row[latitude_column_name] > latitude_boundary)):

        return True

    return False

    
def is_charter(network_value):

    '''Create a boolean column indicating if a record is a charter school.

    Used in an apply statement in the prep_high_school_dataframe function.
    Apply the function to the 'Network' column.

    '''

    if network_value == 'Charter':
        return True

    return False

def is_isp(network_value):

    '''Create a boolean column indicating if a school is an ISP school.'''

    if network_value == 'ISP':
        return True

    return False
