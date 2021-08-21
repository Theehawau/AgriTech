import unittest
import pandas as pd
import sys
from GetDimension import GetDimensionFromBounds


class TestReadData(unittest.TestCase):
    """
    A class for unit-testing functiosns in the GetDimension.py file.
    """
    def setUp(self):
        self.validate_response = (True,'IA_FullState','https://s3-us-west-2.amazonaws.com/usgs-lidar-public/IA_FullState/ept.json',([-10425171.94, -10423171.94], [5164494.71, 5166494.71]))
         
    def test_validate_bounds(self):
        gd = GetDimensionFromBounds(([-10425171.940, -10423171.940], [5164494.710, 5166494.710]))
        response = gd.validate_bound('data.csv')
        self.assertEqual(response, self.validate_response, f'Expected{self.validate_response} got{response}')


if __name__ == '__main__':
	unittest.main()