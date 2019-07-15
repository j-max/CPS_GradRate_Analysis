import pandas as pd
import numpy as np
import pickle


with open('../data/pickles/model_data_from_python_script.p', 'rb') as read_file:
		df = pickle.load(read_file)


class HighSchool_DF(pd.DataFrame):

		@property
		def _constructor(self):
				return HighSchool_DF

		def isolate_school_year_1617(HighSchool_DF):
				df = HighSchool_DF[HighSchool_DF.school_year=='School Year 2016-2017']
				df = df.dropna(subset=['log_grad_rate'])
				return df

		def isolate_school_year_1718(HighSchool_DF):
				df = HighSchool_DF[ HighSchool_DF.school_year=='School Year 2017-2018']
				df = df.dropna(subset=['log_grad_rate'])

				return df

		def target_variable(HighSchool_DF):
				target = HighSchool_DF.log_grad_rate
				return target

		def features(HighSchool_DF):
				features = HighSchool_DF.drop(columns= ['graduation_rate_school', 'school_id', 'school_year', 'log_grad_rate'])
				return features

		def remove_2std_outliers(HighSchool_DF):
				df = HighSchool_DF_remove_outliers_2std = HighSchool_DF[(np.abs(
												HighSchool_DF.log_grad_rate-HighSchool_DF.log_grad_rate.mean())
                        <= 2*HighSchool_DF.log_grad_rate.std())]
				return df


