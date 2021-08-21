#!/usr/bin/env python
# coding: utf-8

# # Imports
import os, sys

# Set absolute path to the root folder of the directory
full_path = os.getcwd()
home_folder = 'CPS_GradRate_Analysis'
root = full_path.split(home_folder)[0] + home_folder + '/'
sys.path.append(root)


import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import matplotlib.pyplot as plt

import sklearn.pipeline
from sklearn.linear_model import LinearRegression

from statsmodels.graphics.gofplots import qqplot


from src.preprocessing.preprocessing_schoolid import merge_pr_and_sp
from src.preprocessing.preprocessing_schoolid import create_df_for_modeling
import matplotlib.pyplot as plt

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# # Data Import and Train Test Split

# add complete path to the root folder of the project
# so that imports work wherever the file is imported from
path_to_sp_csv = root +'/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Profile_Information_SY1819.csv'

path_to_pr_csv = root + '/data/chicago_data_portal_csv_files/Chicago_Public_Schools_-_School_Progress_Reports_SY1819.csv'

'''
The data for this project comes from the Chicago Data Portal.
Two csv's - the school progress report and the school profile -
have been merged by the merge_pr_and_sp function included
in the src folder.


'''

hs_201819 = merge_pr_and_sp(path_to_sp_csv, path_to_pr_csv)


from sklearn.model_selection import train_test_split, cross_validate

X = hs_201819.drop('Graduation_Rate_School', axis=1)
y = hs_201819.loc[:,'Graduation_Rate_School']

X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 42)


# In[19]:


train_df = X_train.merge(y_train, left_index=True, right_index=True)


# In[20]:


train_df = create_df_for_modeling(train_df)


# In[21]:


X_train = train_df.drop('Graduation_Rate_School', axis=1)
y_train = train_df['Graduation_Rate_School']


# Find the first simple model in the fsm.ipynb notebook in the same folder as this notebook. It is a simple linear regression which predicts graduation rates of schools in the 2018-19 school year with Student Count Total.   The FSM's R^2 was .186 average across 3 fold crossvalidation.  Student Count Total had a coefficient of .0145, which can be understood as: for every 100 students, the graduation rate goes increases by 1.45 points.

# ### Cross Validation Function

# In[55]:


def cps_cross_validate(exogenous_feature_name_list, estimator=LinearRegression()):
    cv = cross_validate(estimator, X_train[exogenous_feature_name_list], y_train, 
                        cv=5, return_train_score=True)
    print('##########train mean R^2#############')
    print(np.mean(cv['train_score']))
    print('##########teast mean R^2#############')
    print(np.mean(cv['test_score']))
    print('#####################################')
    print(cv['train_score'])
    print(cv['test_score'])
    print('##########Coefficients after fit on entire train #############')
    
    # When a pipeline is used, the name_steps have to be extracted from the pipeline object.  
    # The else statement below takes care of that.
    
    if type(estimator) != sklearn.pipeline.Pipeline:
        
        model = estimator
        model.fit(X_train[exogenous_feature_name_list], y_train)
        for coef, col in zip (model.coef_, exogenous_feature_name_list):
            print(coef, col)

        y_hat_train = model.predict(X_train[exogenous_feature_name_list])
        resids = y_train - y_hat_train

        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(7,7))
        ax1.scatter(y_hat_train, resids)
        
        qqplot(resids, ax=ax2, line='q')
        
    
    else: 
        model = estimator
        model.fit(X_train[exogenous_feature_name_list], y_train)
        for coef, col in zip (model.named_steps['linearregression'].coef_, exogenous_feature_name_list):
            print(coef, col)

        y_hat_train = model.predict(X_train[exogenous_feature_name_list])
        resids = y_train - y_hat_train

        fig, (ax1,ax2) = plt.subplots(2,1, figsize=(7,7))
        ax1.scatter(y_hat_train, resids)        
        
        ax1.scatter(y_hat_train, resids)
        
        qqplot(resids, ax=ax2, line='q')


# In[38]:


cps_cross_validate(['Student_Count_Total'])


# # Model Iterations

# ## Add Percent Low Income

# Next, I will add a percent low income students to the model.  This will help quantify how 

# In[39]:


X_train['perc_low_income']


# In[40]:


cps_cross_validate(['Student_Count_Total', 'perc_low_income'])


# > adding percent low income results in a significant increase in both train and validation R^2.

# ## Add Dress Code

# In[41]:


cps_cross_validate(['Student_Count_Total', 'perc_low_income', 'Dress_Code'])


# > Adding dress code improves the train score, but validation scores actually go down a bit.

# ## Add Creative School Certification
# 
# EDA suggested that a Creative School Certification correlates with higher graduation rates. 

# In[42]:


X_train.columns[X_train.columns.str.startswith('creative')]


# In[43]:


exog = ['Student_Count_Total', 'perc_low_income', 'Dress_Code']


# In[44]:


exog.extend(
    list(X_train.columns[X_train.columns.str.startswith('creative')]))


# In[45]:


exog


# In[46]:


cps_cross_validate(exog)


# ## Add teacher attendance
# 

# In[47]:


X_train['teacher_attendance']


# In[48]:


X_train['Teacher_Attendance_Year_2_Pct'].isna().sum()


# In[49]:


exog = ['Student_Count_Total', 'perc_low_income', 'Dress_Code', 'teacher_attendance']


# In[50]:


exog.extend(
    list(X_train.columns[X_train.columns.str.startswith('creative')]))


# The teacher_attendance variable requires imputation, since there are 44 nan values.  To prevent data leakage in the cross validation, I will make use of a pipeline.  A simple imputer will apply the imputation correctly across the folds.

# In[51]:


from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer


# In[52]:


ta_pipe = make_pipeline(SimpleImputer(), LinearRegression())


# In[53]:


ta_pipe.fit(X_train[['teacher_attendance']], y_train).named_steps['linearregression'].coef_


# In[56]:


cps_cross_validate(exog, ta_pipe)


# Both the training and valdiation scores continue to increase by approximately 7 pts from the previous model.
# 
# There continues to be high variance, however. The train and validation splits have an approximately 20 pt difference.
