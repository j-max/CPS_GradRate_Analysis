import os, sys

from shapely import geometry
# Set absolute path to the root folder of the directory
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)

from src.cleaning import *
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Create 2018-2019 SchoolYear class
path_to_pr_1819 = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Progress_Reports_SY1819.csv'
path_to_sp_1819 = root + 'data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv'

# Custom functions in src/cleaning.py

# sy_1819 will hold data about all of the schools to allow for eda on the entire student population
sy_1819 = import_and_merge_data(path_to_sp_1819, path_to_pr_1819)

# As shown below, the high school df will be cleaned to have a specific subset of records
sy_1819_hs = import_and_merge_data(path_to_sp_1819, path_to_pr_1819)
sy_1819_hs = convert_is_high_school_to_bool(sy_1819_hs)
sy_1819_hs = isolate_high_schools(sy_1819_hs)

# series for each High Schools Longitude
hs_longs = sy_1819_hs["School_Longitude_sp"]

# series for each High School's latitude`
hs_lats = sy_1819_hs["School_Latitude_sp"]

hs_geometry = [Point(long, lat) for long, lat in zip(hs_longs, hs_lats)] 

geo_df = gpd.GeoDataFrame(sy_1819_hs, geometry=hs_geometry)

# This is not necesary to plot, but could come in handy in the future. 
network_colors = {'Charter':'r', 
                  'ISP':'g',
                  'Network 15':'b',
                  'Network 17':'orange',
                  np.nan:'black',
                  'Options':'pink',
                  'Contract':'green',
                   'Network 16': 'yellow',
                   'Network 14':'cyan', 
                   'AUSL':'magenta'}

geo_df['network_colors'] = geo_df['Network'].map(network_colors)

chicago_shape = gpd.read_file(root+'data/shape_files/geo_export_74e2d584-f137-45fb-b412-80348c0deab2.shp') 

geo_df.explore("Network")
