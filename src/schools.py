import pandas as pd
import numpy as np


class SchoolProfiles():

    def __init__(self, school_profile=None, school_prog_rep=None):
        self.school_profile = school_profile
        self.school_prog_rep = school_prog_rep


    def read_profile(self, data_portal_profile_csv):

        self.school_profile = pd.read_csv(data_portal_profile_csv)

    def read_prog_report(self, data_portal_prog_rep_csv):

        self.school_prog_rep = pd.read_csv(data_portal_prog_rep_csv)



class School():

    pass
