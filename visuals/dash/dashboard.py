import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.express as px 

# Set absolute path to the root folder of the directory
import os
import sys
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)


sys.path.append('../..')

import pandas as pd
import sklearn
from src.preprocessing_schoolid import SchoolYear
from src.cps_model import print_cv_results
from sklearn.model_selection import train_test_split


##########Preprocess with School Year Class
sy_1819 = SchoolYear(root+'/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv',
                    root+ '/data/chicago_data_portal_csv_files/.ipynb_checkpoints/Chicago_Public_Schools_-_School_Progress_Reports_SY1819-checkpoint.csv')

sy_1819.isolate_high_schools()
sy_1819.drop_no_gr_schools()
sy_1819.drop_no_student_schools()
sy_1819.make_percent_low_income()



colors = {
    'background': '#111111',
    'text': '#C5DB5F'
}
app = dash.Dash(__name__) # Initialize the app 
# ------------------------------------------------------------------
app.layout = html.Div() # Define the app 
# ------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True) # Run the app 

