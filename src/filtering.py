import pandas as pd

def drop_no_students(merged_df):

    '''
    Drop schools from a merged dataframe that do not have student counts.
    '''

    print("0 Student Count")
    print(str(merged_df[merged_df['Student_Count_Total'] == 0].shape[0]) +
          ' schools')
    print(merged_df[merged_df['Student_Count_Total'] == 0]["Short_Name_sp"])

    merged_df = merged_df[merged_df['Student_Count_Total'] > 0]

    if merged_df[merged_df['Student_Count_Total'] == 0].shape[0] == 0:
        print('All 0 Student Count Schools Dropped')

    return merged_df


def drop_no_grad_rate(merged_df):

    '''
    Drop schools from a merged dataframe that do not have graduation rates.
    '''

    # Print number of schools in original with no graduation rates
    print("0 Graduation Rate")
    print(str(merged_df[merged_df['Graduation_Rate_School'] == 0].shape[0]) +
          " schools")

    # Print school names with no grad rates
    print(merged_df[merged_df['Graduation_Rate_School'] == 0]["Short_Name_sp"])

    # Print schools that have n/a for a grad rate
    print('##########')
    print('NA Graduation Rates')
    print(str(merged_df[merged_df['Graduation_Rate_School'].isna()].shape[0])
          + " schools")

    # Keep only schools with graduation rates
    merged_df = merged_df[merged_df['Graduation_Rate_School'] > 0]

    # Print statement if all schools w/o grad rates have been dropped
    if not merged_df[merged_df['Graduation_Rate_School'] == 0].shape[0]:
        print('All 0/NA Graduation Rate Schools Dropped')
    else:
        print('There are still schools without grade rates in the df')

    return merged_df


# Filtering

def isolate_high_schools(merged_df):

    merged_df = merged_df[merged_df['Is_High_School'] == True]

    return merged_df


def isolate_numeric_columns(merged_df, add_grad_rates=True):

    sy_numerical_independent_features = ["perc_low_income",
                                         "Student_Count_Total",
                                         "Student_Count_Low_Income",
                                         "Student_Count_Special_Ed",
                                         "Student_Count_English_Learners",
                                         "Student_Count_Black",
                                         "Student_Count_Hispanic",
                                         "Student_Count_White",
                                         "Student_Count_Asian",
                                         "Student_Count_Native_American",
                                         "Student_Count_Other_Ethnicity",
                                         "Student_Count_Asian_Pacific_Islander",
                                         "Student_Count_Multi",
                                         "Student_Count_Hawaiian_Pacific_Islander",
                                         "Student_Count_Ethnicity_Not_Available"]

    if add_grad_rates:
        sy_numerical_independent_features.append('Graduation_Rate_School')

    return merged_df[sy_numerical_independent_features]

def isolate_numeric_rates(merged_df, dem_rate_columns=STUDENT_POP_PERC_LIST,
                          add_grad_rates=False):

    '''
    Filter the dataframe to only include demographic rate columns
    and, if add_grad_rates==True, the graduation rate of the school
    '''

    if add_grad_rates:
        demrates_plus_gradrate = dem_rate_columns + ['Graduation_Rate_School']
        return merged_df[demrates_plus_gradrate]
    else:
        return merged_df[dem_rate_columns]


def isolate_important_columns(merged_df, confident_columns=False, exclude_target=True):

    """
    There are a large number of columns in the dataset that
    are not used. This function isolates the most important columns.

    One reason for dropping the columns will be to allow
    for feature selection via recursive feature elimination
    and other methods
    """

    # These columns are consistent across 2016-2019 School Years
    sy_id_columns = ["School_ID", "Short_Name_sp"]

    target = ["Graduation_Rate_School"]

    sy_boolean_important = ['Is_High_School', 'Dress_Code',
                            "Is_Middle_School", "Is_Elementary_School",
                            "Is_Pre_School",
                            "PreK_School_Day", "Kindergarten_School_Day",
                            "Bilingual_Services", "Refugee_Services",
                            "Title_1_Eligible",
                            "PreSchool_Inclusive", "Preschool_Instructional",
                            "Significantly_Modified", "Hard_Of_Hearing",
                            "Visual_Impairments"]

    categorical_important = ["School_Type", 'Network', "Primary_Category_sp",
                             "Grades_Offered", "After_School_Hours",
                             "Earliest_Drop_Off_Time", "Classroom_Languages",
                             ]

    engineered_columns = [
        'perc_Student_Count_Low_Income', 'perc_Student_Count_Special_Ed',
        'perc_Student_Count_English_Learners', 'perc_Student_Count_Black',
        'perc_Student_Count_Hispanic', 'perc_Student_Count_White',
        'perc_Student_Count_Asian', 'perc_Student_Count_Native_American',
        'perc_Student_Count_Other_Ethnicity', 'perc_Student_Count_Asian_Pacific_Islander',
        'perc_Student_Count_Multi', 'perc_Student_Count_Hawaiian_Pacific_Islander',
        'perc_Student_Count_Ethnicity_Not_Available', 'Student_Count_Total_1718',
        'student_count_total_change_1_year']


    confident_columns =  ["Dress_Code", "Network"]
                   
    if not confident_columns:
        return merged_df[target +
                         sy_id_columns +
                         sy_boolean_important +
                         categorical_important +
                         engineered_columns]

    if not exclude_target:
        return merged_df[target +
                         engineered_columns +
                         confident_columns]

    return merged_df[engineered_columns +
                     confident_columns]


def isolate_main_networks(merged_df):

    main_networks = ['Network 14', 'Network 15', 'Network 16', 'Network 17']
    main_network_df = merged_df[merged_df['Network'].isin(main_networks)]

    return main_network_df


def filter_cwoption_special_ed(merged_df):

    '''
    Since they are outliers in graduation rate, remove citywide option schools
    and special education schools
    '''

    merged_df = merged_df[~merged_df['School_Type']
                          .isin(['Citywide-Option', 'Special Education'])]

    # There is at least one option network school not categorized as
    # Citywide-option
    merged_df = merged_df[merged_df['Network'] != 'Options']

    return merged_df

