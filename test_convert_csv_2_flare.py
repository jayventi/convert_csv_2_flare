
"""
Unit test fixture for convert_csv_2_flare.py

python 2.7
Created on Oct 26, 2016
@author: jayventi
test_convert_csv_2_flare.py
"""

import unittest
from convert_csv_2_flare import *

"""
test setup  depends  on manual creation of the following
directories and files
1 - testdirs
|___ File_A.txt    1024 b
|___ 2 - testdirs/subDirBoo
|     |___ File_B.log    50,000,000 b
|     |___ File_C.csv    50,000,000 b
|___ 3 - testdirs/subDirFoo
      |___ File_D.tar    52,428,800 b
      |___ 4 - testdirs/subDirFoo/subDirBar
          |___ File_E.py    1024 b
these files are provided for testing in testdirs.zip
"""


#  Basic creation and detection
class TestConvertCsv2Flare(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def ospath_expdict_pos_2_win(self, expected_dict):
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_01_ospath_win2pos(self):
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_02_RepresentsInt(self):
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_03_csv_2_tree_path_dicts(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_04_write_2_jsonfile(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_05_root_str(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_06_find_root_dir(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_07_add_root(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_08_calc_children(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_09_calc_root_totlas(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_10_working_node_total(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_11_build_dir_tree_a(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_10_build_dir_tree_b(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

    def test_11_main_a(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)


    def test_11_main_2(self):
        #setup
        #test
        actual = False
        expected = True
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)