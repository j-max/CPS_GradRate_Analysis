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
FULL_PATH = os.getcwd()
HOME_FOLDER = 'CPS_GradRate_Analysis'
ROOT = FULL_PATH.split(HOME_FOLDER)[0] + HOME_FOLDER + '/'
sys.path.append(ROOT)

sys.path.append('../..')

import pandas as pd
import sklearn
from src.cleaning import prep_high_school_dataframe
from src.cps_model import print_cv_results

# Preprocess with School Year Class
sy_1819 = prep_high_school_dataframe(ROOT+'/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv',
                     ROOT+ '/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Progress_Reports_SY1819.csv',
                     ROOT+ '/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Progress_Reports_SY1718.csv',
                     ROOT+'/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1718.csv')

colors = {
    'background': '#41B6E6',
    'text': '#000000'
}
app = dash.Dash(__name__) # Initialize the app 

# ------------------------------------------------------------------
fig = px.scatter(sy_1819, x='Student_Count_Total', y='Graduation_Rate_School')

app.layout = html.Div(children=[
    html.H1(children="CPS Dashboard",
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
    ),
    html.Div(children='''
        A Dashboard Visualizing Statistics about CPS Schools
''',
             style={
                 'textAlign': 'center'
                 }
                     
    ),
    dcc.Graph(
        id='Total Students vs. Graduation Rate',
        figure=fig
    )
])       

if __name__ == '__main__':
    app.run_server(debug=True)
