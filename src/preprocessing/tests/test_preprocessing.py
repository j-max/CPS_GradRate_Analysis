import pandas as pd
import os, sys
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)

from src.preprocessing.preprocessing import import_multiple_sy_profiles, create_sp_path_dictionary, isolate_high_schools

from src.preprocessing.preprocessing import years, paths

def test_create_sp_path_dictionary():

    assert len(create_sp_path_dictionary(years, paths)) == len(years)


def test_import_multiple_sy_profiles():

    sp_path_dict = create_sp_path_dictionary(years, paths)
    sp_dfs = import_multiple_sy_profiles(sp_path_dict)

    df_201617 = sp_dfs['2016-2017']
    assert 'School_ID' in df_201617.columns

    assert type(import_multiple_sy_profiles(sp_path_dict)[years[0]]) == type(pd.DataFrame())



def test_isolate_high_schools_sy_profiles():

    sp_path_dict = create_sp_path_dictionary(years, paths)
    df_dict = import_multiple_sy_profiles(sp_path_dict)

    df_1617 = df_dict['2016-2017']
    df_1718 = df_dict['2017-2018']
    df_1819 = df_dict['2018-2019']

    assert 'Is_High_School' in df_1617.columns
    assert 'Is_High_School' in df_1718.columns
    assert 'Is_High_School' in df_1819.columns

    hs_1819 = isolate_high_schools(df_1819)

    assert hs_1819['Is_High_School'].sum() == len(hs_1819)

