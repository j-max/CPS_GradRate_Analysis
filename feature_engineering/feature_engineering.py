import pandas as pd
import numpy as np
import pickle
import re

import psycopg2 as pg
import pandas.io.sql as pd_sql

connection_args = {
    'host': 'localhost',  
    'dbname': 'cps',    
    'port': 5432
}

conn = pg.connect(**connection_args)

target_columns_1617 = '''School_Id,
                      Administrator,
                      Grades_Offered_All,
                      Student_Count_Total,
                      Student_Count_Low_Income,
                      Student_Count_Special_Ed,
                      Student_Count_English_Learners,
                      Student_Count_Black,
                      Student_Count_Hispanic,
                      Student_Count_White,
                      Student_Count_Asian,
                      Student_Count_Native_American,
                      Student_Count_Other_Ethnicity,
                      Student_Count_Asian_Pacific_Islander,
                      Student_Count_Multi,
                      Student_Count_Hawaiian_Pacific_Islander,
                      Student_Count_Ethnicity_Not_Available,
                      ADA_Accessible,
                      Dress_Code,
                      Classroom_Languages,
                      Transportation_El,
                      Graduation_Rate_School,
                      School_Year,
                      Zip
                '''

target_columns_1718 = '''School_Id,
                      Administrator,
                      Grades_Offered_All,
                      Student_Count_Total,
                      Student_Count_Low_Income,
                      Student_Count_Special_Ed,
                      Student_Count_English_Learners,
                      Student_Count_Black,
                      Student_Count_Hispanic,
                      Student_Count_White,
                      Student_Count_Asian,
                      Student_Count_Native_American,
                      Student_Count_Other_Ethnicity,
                      Student_Count_Asian_Pacific_Islander,
                      Student_Count_Multi,
                      Student_Count_Hawaiian_Pacific_Islander,
                      Student_Count_Ethnicity_Not_Available,
                      Dress_Code,
                      Classroom_Languages,
                      Transportation_El,
                      Graduation_Rate_School,
                      School_Year,
                      Network
                '''

def create_hs_df(year, target_columns):
	'''query the database and create a dataframe with target features for a given year.
			Year must be in format 1718 in order to query the db correctly
			target_columns must  be a list of columns that match the db's field names	
	'''
	query = '''SELECT %s FROM allschools_%s WHERE is_high_school = 'Y' ''' %(target_columns, year)
	df = pd_sql.read_sql(query, conn)
	return df


def merge_multiple_year_hs_dfs(list_of_dfs):
	'''create a dataframe with multipl years concatenated together'''
	return pd.concat(list_of_dfs)



def create_ada_accessible_dummies(school_year, df):
	'''create ada accessibility dummies.  For this particular example, 201617 school year ada data is used to 
	populate 1718 data since it is assumed to be the same, and 1718 lacks it.'''
	
	ada = df[df['school_year'] == school_year][['ada_accessible', 'school_id']]
	df = pd.merge(df, ada, on = 'school_id' )
	df.drop(columns = 'ada_accessible_x', inplace = True)
	df = pd.concat((df, pd.get_dummies(df['ada_accessible_y'])), axis=1)
	#having [0,0] for fully and generally accessible implies no or unknown accessibility
	df.drop(columns = ['No/unknown accessibility','ada_accessible_y'], inplace=True)
	return df



def calculate_demographic_percentages(df):
	'''the original data has students counts, so the following code converts counts
		to percentages and drops the original count columns from the dataframe'''

	demog_headings = ['student_count_asian', 'student_count_asian_pacific_islander', 'student_count_black', 
                  'student_count_english_learners', 'student_count_ethnicity_not_available', 
                  'student_count_hawaiian_pacific_islander', 'student_count_hispanic', 
                  'student_count_low_income', 'student_count_multi', 'student_count_native_american',
                  'student_count_other_ethnicity', 'student_count_special_ed', 'student_count_white']
	for dem in demog_headings:
		dem_per_heading = dem + '_perc'
		df[dem_per_heading] = df[dem]/df['student_count_total']
		df.drop(columns = dem, inplace=True)

	return df

def count_classroom_languages(df, school_year):
	'''The number of languages in each school is a comma separated list.
		This function counts the commas in each list to determine how many languages there are in each school.
	'''
	df_languages = df[['school_id', 'classroom_languages', 'school_year']]
	#the data appears to show the same value for languages across the two years
	#so the data will be transformed on one year to prevent duplication at time of merge
	df_languages = df_languages[df_languages['school_year'] == school_year]
	#NaN will be treated as 0 in the language count. 
	#Since language count will be performed with a comma count,
	#set nan to 15 and reset to 0 after the count is performed.
	df_languages.fillna(',,,,,,,,,,,,,,', inplace=True)	
	df_languages['Classroom_Languages_count'] = (
                                            df_languages['classroom_languages'].str.count(',') 
                                            + 1
                                            )
	df_languages['Classroom_Languages_count'].loc[df_languages['Classroom_Languages_count'] == 15] = 0
	df_languages.drop(columns = ['classroom_languages', 'school_year'], inplace=True)
	return  pd.merge(df, df_languages, on='school_id')

def create_el_dummies(df, school_year):
	'''Each school is associated with a list of el stations nearby
		stored as a comma separated list.  This function creates dummie
		variables associated with each color.
	'''
	el_df = df[['school_id', 'transportation_el', 'school_year']]
	#Again, like languages, looks like El values are consistent across years.
	el_df = el_df[el_df['school_year'] == school_year]
	el_df['transportation_el'].value_counts()
	#replace NaN with no_el so that with dummy variable I can drop No_El
	el_df.fillna(value = 'No_El', inplace=True)
	el_dummies = el_df['transportation_el'].str.get_dummies(sep = ', ')
	el_dummies.drop(columns = 'No_El', inplace=True)
	el_df = pd.merge(el_df,el_dummies, left_index=True, right_index=True)
	el_df.drop(columns = ['transportation_el', 'school_year'], inplace=True)
	df = pd.merge(df, el_df, on='school_id')
	df.drop(columns = ['transportation_el'], inplace=True)

	return df

def create_dresscode_binary(df):
	'''Chicago Data Portal lists whether each school has a dress code with N or Y.
	This function takes the original dataframe and changes Y/N to a single binary column.
	'''
	df["Dress_Code_dummie"] = pd.get_dummies(df['dress_code'], drop_first = True)
	df.drop(columns='dress_code', inplace=True)
	return df

def count_grades(df):
	df_grades = df[['grades_offered_all', 'school_id']]
	df_grades['grades_offered_count'] = (df_grades['grades_offered_all'].str.count(',') + 1)     
	df_grades.drop(columns = ['grades_offered_all'], inplace=True)
	df_grades.drop_duplicates('school_id', inplace=True)
	df_grades.sort_values('grades_offered_count')
	df = pd.merge(df, df_grades, on='school_id')
	df.drop(columns = ['classroom_languages', 'grades_offered_all'], inplace=True)

	return df

def charter(row):
    if row['network'] == 'Charter':
        return 1
    else:
        return 0

def create_charter_dummy(df, school_year):
	df_networks = df[['school_id', 'network', 'school_year']]
	df_networks2017 = df_networks[df_networks['school_year']==school_year]

	df_networks2017['charter'] = df_networks2017.apply(lambda row: charter(row), axis=1)
	df_networks2017.drop(columns=['school_year', 'network'], inplace=True)
	df = pd.merge(df, df_networks2017, on='school_id')
	df.drop(columns='network', inplace=True)

	return df

def gender_binary(row):
    if row['gender_f'] == True:
        return 1
    else:
        return 0

def create_admin_gender_dummy(df):
	df_admin = df[['administrator', 'school_id']]
	df_admin.drop_duplicates('school_id')
	gender = re.compile(r'Mrs|Ms|Mr')
	df_admin['gender_marker'] = df_admin['administrator'].astype(str).str.match(gender)
	df_admin.drop_duplicates('school_id', inplace=True)

	male_marker = re.compile(r'Mr|Juan|Richard|Ali|Kevin|Douglas|Raul|Victor|Abdul|Charles|Antonio|Brian|Francisco|\
        Sheldon|Michael|Stephen|Peter|Gregory|Trent|Myron|Gerald|Elias|Octavio|Matthew|\
        David|Leonard|Ferdinand|Fernando|Mark|Patrick|George|Wayne|Anthony|William|\
        Stephen|Timothy|Paul')
	female_marker = re.compile(r'Mrs|Ms|Dr. Hillyn|Sharnette|Tressie|Leticia|Priscilla|Joyce|Stephanie|Tanya|Veronica|Kathy|\
         Sandra|Torry|Stephanie|Carolyn|Milena|Vanesa|Breanda|Laura|Kelly|Anna|Nancy|\
         Tamika|Janice|Mary|Shanele|Falilat|Dr.Femi|Noel|Tawanna|Tonya|Sandra|Dr. Vanesa|Tamika')
	df_admin['gender_f'] = df_admin['administrator'].astype(str).str.match(female_marker)
	df_admin.drop(columns = ['administrator', 'gender_marker'], inplace=True)

	df = pd.merge(df, df_admin, on='school_id')

	df['gender_f_bn'] = df.apply(lambda row: gender_binary(row), axis=1)
	df.drop(columns = ['administrator', 'gender_f'], inplace = True)

	return df
	
def reflect_and_log_transform_grad_rates(df):
		'''
		The target variable, graduation rates, is left skewed.  
		To fix this, reflect the data and log transform it.
		'''
		df['Grad_Rate_Reflected'] = 100 - df['graduation_rate_school']
		df['log_grad_rate'] = np.log(df['Grad_Rate_Reflected'])
		df.drop(columns =['Grad_Rate_Reflected'], inplace=True)

		return df

def replace_comma(row):
		'''
		When scraping the income data with Selenium from 'https://factfinder.census.gov'
		the incomes included commas in the thousandths place.
		This function removes them
		'''
		return float(row['Zip_Mean_Income'].replace(',', ''))

def merge_income_data_per_zip(df):
		'''
		Associates the mean household income per zip gathered with Selenium https://factfinder.census.gov
		with the school zip codes.

		This function is specifically built from years 2016-17, and 2017-18.
		'''
		zip_2016 = df[df.school_year == 'School Year 2016-2017'][['school_id', 'zip']]
		df = pd.merge(df, zip_2016, on='school_id')
		df.drop('zip_x', axis=1, inplace=True)
		df.rename(columns = {'zip_y':'zip'}, inplace=True)
		df_2016 = df[df['school_year'] == 'School Year 2016-2017']
		df_2016_income = pd.read_csv('../data/compiled_datafiles/meanHHincome_2016.csv', header=None)
		df_2016_income.columns = ['zip', 'Zip_Mean_Income']
		df_2016 = pd.merge(df_2016, df_2016_income, on = 'zip' )

		df_2017 = df[df['school_year'] == 'School Year 2017-2018']
		df_2017_income = pd.read_csv('../data/compiled_datafiles/meanHHincome_2017.csv', header=None)
		df_2017_income.columns = ['zip', 'Zip_Mean_Income']
		df_2017 = pd.merge(df_2017, df_2017_income, on = 'zip' )

		df = df_2016.append(df_2017)

		df['Zip_Mean_Income'] = df.apply(lambda row: replace_comma(row), axis =1) 

		return df

		
list_of_dfs = [create_hs_df('1617', target_columns_1617), create_hs_df('1718', target_columns_1718)]
df = merge_multiple_year_hs_dfs(list_of_dfs)
school_year = 'School Year 2016-2017'
df = create_ada_accessible_dummies(school_year, df)
df = calculate_demographic_percentages(df)
df = count_classroom_languages(df, school_year)
df = create_el_dummies(df, 'School Year 2017-2018')
df = create_dresscode_binary(df)
df = count_grades(df)
df = create_charter_dummy(df, 'School Year 2017-2018')
df = create_admin_gender_dummy(df)
df = reflect_and_log_transform_grad_rates(df)
df = merge_income_data_per_zip(df)

with open('../data/pickles/model_data_from_python_script.p', 'wb') as write_file:
		pickle.dump(df, write_file)
