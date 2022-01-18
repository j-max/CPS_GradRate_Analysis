import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
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
        id='continuous-v-graduation-rate',
    ),
    
    html.Br(),
    html.Label("Radio Items"),
    dcc.RadioItems(
        children='''Select a demographic population to see correlation to 
                    graduation rate''',
        id='demographic_radio',
        options=[
            {'label': 'Student Count', 'value': 'Student_Count_Total'},
            {'label': 'Low Income Students',
             'value': 'perc_Student_Count_Low_Income'},
            {'label': 'Special Ed Students',
             'value': 'perc_Student_Count_Special_Ed'}
        ]
    )
])


@app.callback(
    Output('continuous-v-graduation-rate', 'figure'),
    Input('demographic_radio', 'value'))
def update_figure(dem_selected):

    '''Plot demographic count vs graduation rate based on radio selection'''

    fig = px.scatter(sy_1819, x=dem_selected,
                     y='Graduation_Rate_School',
                     hover_name='Short_Name_sp')

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
