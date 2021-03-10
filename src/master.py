import pandas as pd
import pickle

import numpy as np
import math
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.linear_model import  Ridge, Lasso
from sklearn.preprocessing import StandardScaler
import seaborn as sns

import psycopg2 as pg
import pandas.io.sql as pd_sql


connection_args = {
    'host': 'localhost',  
    'dbname': 'cps',    
    'port': 5432
}

conn = pg.connect(**connection_args)
cur = conn.cursor()
query = ('''SELECT * FROM hs_modeldata WHERE log_grad_rate IS NOT NULL''');
df = pd_sql.read_sql(query, conn)
print(df.describe())


#load pickle with features prepared for modelling.
with open('data/pickles/29feat_formodeling.pickle', 'rb') as to_read:
    df = pickle.load(to_read)

#remove target variable from features and define y as target variable.
X = df.drop('log_grad_rate', axis = 1)
y = df.log_grad_rate

print("hello")
 
#the first alpha cands is present for record of how the range was narrowed down
# alpha_cands = np.arange(.001,10.001,.1)
alpha_cands = np.arange(.001, .01, .001)

best_alpha_rsquared = 0
best_alpha = 0

for alpha_candidate in alpha_cands:
		kf_lasso_train_scores = []
    kf_lasso_test_scores = []
    lasso = Lasso(alpha=alpha_candidate)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    kf_splits = kf.split(X, y)

    for train_ind, test_ind in kf_splits:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X.iloc[train_ind])
        y_train = y.iloc[train_ind]

        lasso.fit(X_train_scaled, y_train)
        X_test_scaled = scaler.transform(X.iloc[test_ind])
        y_test = y.iloc[test_ind]

        kf_lasso_train_scores.append(lasso.score(X_train_scaled, y_train))
        kf_lasso_test_scores.append(lasso.score(X_test_scaled, y_test))

    if (sum(kf_lasso_test_scores) / len(kf_lasso_test_scores)) > best_alpha_rsquared:
        best_alpha = alpha_candidate
        best_alpha_rsquared = (sum(kf_lasso_test_scores) / len(kf_lasso_test_scores))
