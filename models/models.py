import pandas as pd
import pickle
from highschool_class import HighSchool_DF
import numpy as np

from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.linear_model import  Ridge, Lasso
from sklearn.preprocessing import StandardScaler
import math

with open('../data/pickles/model_data_from_python_script.p', 'rb') as read_file:
		df = pickle.load(read_file)

def select_optimal_alpha(X, y):
		#alpha_cands = np.arange(.001,10.001,.1)
		alpha_cands = np.arange(.001,.01,.001)

		best_alpha_rsquared = 0
		best_alpha = 0
		for alpha_candidate in alpha_cands:
				kf_lasso_train_scores = []
				kf_lasso_test_scores = []
				lasso = Lasso(alpha = alpha_candidate)
				kf = KFold(n_splits=5, shuffle=True, random_state=42)
				kf_splits = kf.split(X,y)

				for train_ind, test_ind in kf_splits:
						scaler = StandardScaler()
						X_train_scaled = scaler.fit_transform(X.iloc[train_ind])
						y_train = y.iloc[train_ind]

						lasso.fit(X_train_scaled, y_train)
						X_test_scaled = scaler.transform(X.iloc[test_ind])
						y_test        = y.iloc[test_ind]

						kf_lasso_train_scores.append(lasso.score(X_train_scaled, y_train))
						kf_lasso_test_scores.append(lasso.score(X_test_scaled, y_test))


				if (sum(kf_lasso_test_scores)/len(kf_lasso_test_scores)) > best_alpha_rsquared:
						best_alpha = alpha_candidate
						best_alpha_rsquared = (sum(kf_lasso_test_scores)/len(kf_lasso_test_scores))
		print(best_alpha_rsquared)
		print(best_alpha)
		return best_alpha

def lasso_to_identify_best_coefficients(X, y, best_alpha):
		#Don't keep holdout set since the sample is small. KFolds validation is enough.
		kf = KFold(n_splits = 5, shuffle = True, random_state = 42)

		#best alpha taken from iterative method
		lasso = Lasso(alpha = best_alpha)

		train_r2 = []
		val_r2 = []
		for train, val in kf.split(X,y):
				scaler = StandardScaler()
				X_train = scaler.fit_transform(X.iloc[train])
				y_train = y.iloc[train]
				lasso.fit(X_train, y_train)
				train_r2.append(lasso.score(X_train, y_train))
				X_val = scaler.transform(X.iloc[val])
				y_val = y.iloc[val]
				val_r2.append(lasso.score(X_val, y_val))
		for feature, coef in zip(list(X), lasso.coef_):
				print(feature, coef)

		meaningful_features = []
		for feature, coef in zip(list(X), lasso.coef_):
				if coef != -0.0:
						meaningful_features.append(feature)
		print(meaningful_features)
		return meaningful_features


def linear_model_with_meaningful_features(X, y, meaningful_features):

		X = X[meaningful_features]
		kf = KFold(n_splits = 5, shuffle=True, random_state=42)

		r2_train = []
		r2_test =   []
		mse = []
		for train, test in kf.split(X,y):
				lm = LinearRegression()
				X_train, y_train = X.iloc[train], y.iloc[train]
				X_test, y_test     = X.iloc[test], y.iloc[test]

				lm.fit(X_train, y_train)
				r2_train.append(lm.score(X_train, y_train))
				r2_test.append(lm.score(X_test, y_test))

				predict_test = lm.predict(X_test)
				untransformed_x_predict = np.e**predict_test
				untransformed_y = np.e**y_test
				mse.append(mean_squared_error(untransformed_x_predict, untransformed_y))

		average_mse = (sum(mse)/len(mse))
		print(math.sqrt(average_mse))
		print(sum(r2_train)/len(r2_train))
		#Mean r-squared on the test sets in the k-fold
		print(sum(r2_test)/len(r2_test))

df_1617 = HighSchool_DF(df).isolate_school_year_1617()
df_1617_no_outliers = df_1617.remove_2std_outliers()
y_1617 = df_1617_no_outliers.target_variable()
features_1617 = df_1617_no_outliers.features()
best_alpha_1617 = select_optimal_alpha(features_1617, y_1617)
meaningful_features_1617 = lasso_to_identify_best_coefficients(features_1617, y_1617, best_alpha_1617)
linear_model_with_meaningful_features(features_1617, y_1617, meaningful_features_1617)


df_1718 = HighSchool_DF(df).isolate_school_year_1718()
df_1718_no_outliers = df_1718.remove_2std_outliers()
y_1718 = df_1718_no_outliers.target_variable()
features_1718 = df_1718_no_outliers.features()
best_alpha_1718 = select_optimal_alpha(features_1718, y_1718)
meaningful_features_1718 = lasso_to_identify_best_coefficients(features_1718, y_1718, best_alpha_1718)
linear_model_with_meaningful_features(features_1718, y_1718, meaningful_features_1718)

df_1618 = HighSchool_DF(df)
df_1618_no_outliers = df_1618.remove_2std_outliers()
y_1618 = df_1618_no_outliers.target_variable()
features_1618 = df_1618_no_outliers.features()
best_alpha_1618 = select_optimal_alpha(features_1618, y_1618)
meaningful_features_1618 = lasso_to_identify_best_coefficients(features_1618, y_1618, best_alpha_1618)
linear_model_with_meaningful_features(features_1618, y_1618, meaningful_features_1618)
