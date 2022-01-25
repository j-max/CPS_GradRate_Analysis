import pandas as pd

from src.feature_engineering import convert_is_high_school_to_bool
from src.feature_engineering import delta_student_count
from src.feature_engineering import is_charter
from src.feature_engineering import is_isp
from src.feature_engineering import make_percent_demographics
from src.feature_engineering import northwest_quadrant

from src.filtering import isolate_high_schools
from src.filtering import drop_no_students
from src.filtering import drop_no_grad_rate
from src.filtering import filter_cwoption_special_ed


class District:

    def __init__(self,
                 path_to_sp_csv,
                 path_to_pr_csv, 
                 path_to_prior_year_sp,
                 path_to_prior_year_pr):

        self.path_to_sp_csv = path_to_sp_csv
        self.path_to_pr_csv = path_to_pr_csv
        self.path_to_prior_year_sp = path_to_prior_year_sp
        self.path_to_prior_year_pr = path_to_prior_year_pr
        
        self.sp_df = pd.read_csv(self.path_to_sp_csv)
        self.pr_df = pd.read_csv(self.path_to_pr_csv)

        self.unaltered_df = (self.sp_df.merge(self.pr_df,
                                              on='School_ID',
                                              suffixes=('_sp', '_pr')))

        self.df = self.prep_frame()

    def prep_frame(self):

        self.df = (self.sp_df.merge(self.pr_df,
                                    on='School_ID',
                                    suffixes=('_sp', '_pr')))    
        self.df = convert_is_high_school_to_bool(self.df)
        self.df = make_percent_demographics(self.df)
 
        self.df = convert_is_high_school_to_bool(self.df)
        self.df = isolate_high_schools(self.df)
        self.df = drop_no_students(self.df)
        self.df = drop_no_grad_rate(self.df)
        self.df = make_percent_demographics(self.df)
        self.df = delta_student_count(self.df,
                                      self.path_to_prior_year_sp,
                                      self.path_to_prior_year_pr,
                                      new_year_added='1718')
        self.df['nw_quadrant'] = self.df.apply(northwest_quadrant, axis=1)
        self.df['is_charter'] = self.df['Network'].apply(is_charter)
        self.df['is_isp'] = self.df['Network'].apply(is_isp)
        self.df = filter_cwoption_special_ed(self.df)
        
        return self.df
 
