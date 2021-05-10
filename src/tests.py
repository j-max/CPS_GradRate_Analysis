import unittest
import pandas as pd

class DataFrameTest(unittest.TestCase):

    def test_isupper(self):
        self.assertTrue('FrO'.isupper())
        self.assertFalse('Foo'.isupper())


    def test_isdataframe(self):

        # df = import_dataframe_from_school_profile(sy='2018-2019')
        self.assertEqual(type(df), type(pd.DataFrame()))


if __name__ == '__main__':
      unittest.main()
