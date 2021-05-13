import pandas as pd
import os, sys
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)

from src.preprocessing.preprocessing import import_multiple_sy_profiles, create_sp_path_dictionary

from src.preprocessing.preprocessing import isolate_important_columns, isolate_high_schools, convert_is_high_school_to_bool

from src.preprocessing.preprocessing import years, paths

sp_path_dict = create_sp_path_dictionary(years, paths)
sp_dfs = import_multiple_sy_profiles(sp_path_dict)


def test_create_sp_path_dictionary():

    assert len(create_sp_path_dictionary(years, paths)) == len(years)


def test_import_multiple_sy_profiles():

    sp_path_dict = create_sp_path_dictionary(years, paths)
    sp_dfs = import_multiple_sy_profiles(sp_path_dict)

    df_201617 = sp_dfs['2016-2017']
    assert 'School_ID' in df_201617.columns

    assert type(import_multiple_sy_profiles(sp_path_dict)[years[0]]) == type(pd.DataFrame())


def test_isolate_important_columns():

    df_1819 = isolate_important_columns(sp_dfs['2018-2019'])
    
    assert len(df_1819.columns) == 20

    for year in sp_dfs:
        print(year)
        df = isolate_important_columns(sp_dfs[year])
        assert len(df.columns) == 20


def test_convert_is_high_school_to_bool():

    for year in sp_dfs:
        df = convert_is_high_school_to_bool(sp_dfs[year])
        assert df['Is_High_School'].dtype == 'bool'

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

