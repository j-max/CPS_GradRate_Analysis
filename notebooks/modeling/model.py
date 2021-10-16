# Set absolute path to the root folder of the directory
import sys
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)


sys.path.append('../..')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.preprocessing_schoolid import SchoolYear
from src.cps_model import print_cv_results
from sklearn.model_selection import train_test_split

# Metrics and validation tools
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_validate, cross_val_predict

# Models
from sklearn.linear_model import LinearRegression

##########Preprocess with School Year Class
sy_1819 = SchoolYear(root+'/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv',
                    root+ '/data/chicago_data_portal_csv_files/.ipynb_checkpoints/Chicago_Public_Schools_-_School_Progress_Reports_SY1819-checkpoint.csv')

sy_1819.isolate_high_schools()
sy_1819.drop_no_gr_schools()
sy_1819.drop_no_student_schools()
sy_1819.make_percent_low_income()


##########Train Test split

X = sy_1819.merged_df.drop("Graduation_Rate_School", axis=1)
y = sy_1819.merged_df["Graduation_Rate_School"]

# The split below leaves 27 schools for the test set
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=.2, random_state=42)

##########FSM

'''
The FSM will simply predict the mean graduation rate from the 2018-19 School Year. 
'''

mean_grad_rate_201819 = X_train.Graduation_Rate_Mean.unique()[0]

y_hat = np.full(len(X_train), mean_grad_rate_201819)

'''This r2 is negative, which makes sense, since the mean
of the entire dataset is less accurate than the mean of training set.'''
print(r2_score(y_train, y_hat))

'''The baseline RMSE is helpful.
Predicting the mean misses by an average of 22 Graduation points'''
print(np.sqrt(mean_squared_error(y_train, y_hat)))

##########Linear Regression Models

# Student Population predicting Graduation Rate

lr = LinearRegression()

print(cross_validate(lr, X_train[["Student_Count_Total"]], y_train,
                     scoring=('r2', 'neg_mean_squared_error')))

