
"""
Unit test fixture for convert_csv_2_flare.py

python 2.7
Created on Oct 26, 2016
@author: jayventi
test_convert_csv_2_flare.py
"""

import unittest
from json import load
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
        self.converter = ConvertCsv2Flare()

    def tearDown(self):
        pass

    def test_01_ospath_win2pos(self):
        self.setUp()
        #test
        test_path = "\Windows\System32\DriverStore\FileRepository"
        actual = self.converter.ospath_win2pos(test_path)
        expected = "/Windows/System32/DriverStore/FileRepository"
        self.assertEqual(actual, expected)
        self.assertEqual(actual, expected)

    def test_02_RepresentsInt_true(self):
        self.setUp()
        #test
        actual = self.converter.RepresentsInt(123)
        expected = True
        self.assertEqual(actual, expected)

    def test_02_RepresentsInt_false(self):
        #test
        actual = self.converter.RepresentsInt("12noT3")
        expected = False
        self.assertEqual(actual, expected)

    def test_03_csv_2_tree_path_dicts(self):
        #setup
        #test
        test_file = "FSHistory_test.csv"
        actual = self.converter.csv_2_tree_path_dicts(test_file)
        expected = {'testdirs/subDirBoo': {'ps': '0', 'txt': '0', 'log_Cn': '1', 'log': '50000000', 'zip': '0', 'zz_time': '06:47:17',
                    'ps_Cn': '0', 'js_Cn': '0', 'txt_Cn': '0', 'js': '0', 'zip_Cn': '0', 'other': '0', 'sql_Cn': '0', 'sql': '0',
                    'path': 'testdirs/subDirBoo', 'csv_Cn': '1', 'csv': '50000000', 'zz_level': '1', 'other_Cn': '0', 'zz_today': '2016-10-17'},
                    'testdirs/subDirFoo': {'ps': '0', 'txt': '0', 'log_Cn': '0', 'log': '0', 'zip': '0', 'zz_time': '06:47:17',
                    'ps_Cn': '0', 'js_Cn': '0', 'txt_Cn': '0', 'js': '0', 'zip_Cn': '0', 'other': '52429824', 'sql_Cn': '0', 'sql': '0',
                    'path': 'testdirs/subDirFoo', 'csv_Cn': '0', 'csv': '0', 'zz_level': '1', 'other_Cn': '2', 'zz_today': '2016-10-17'}}
        self.assertEqual(actual, expected)

    def test_04_write_2_jsonfile(self):
        #setup
        #test
        test_dict = {u'1': u'123'}
        self.converter.write_2_jsonfile(test_dict, 'test_write_2_json.test')
        with open('test_write_2_json.test') as data_file:
            data = load(data_file)
        actual = data
        expected = test_dict
        self.assertEqual(actual, expected)

    def test_05_root_str(self):
        #setup
        #test
        actual = self.converter.root_str("root", "root-candidate")
        expected = "root"
        self.assertEqual(actual, expected)

    def test_06_find_root_dir(self):
        #setup
        test_file = "FSHistory_test.csv"
        tree_ditc = self.converter.csv_2_tree_path_dicts(test_file)
        #test
        actual = self.converter.find_root_dir(tree_ditc)
        expected = "testdirs"
        self.assertEqual(actual, expected)

    def test_07_add_root(self):
        test_file = "FSHistory_test.csv"
        tree_ditc = self.converter.csv_2_tree_path_dicts(test_file)
        root_path = self.converter.find_root_dir(tree_ditc)
        #setup
        #test
        self.converter.add_root(tree_ditc, root_path)
        actual = tree_ditc["testdirs"]
        expected = {'root': True}
        self.assertEqual(actual, expected)

    def test_08_calc_children(self):
        #setup
        test_file = "FSHistory_test.csv"
        tree_ditc = self.converter.csv_2_tree_path_dicts(test_file)
        root_path = self.converter.find_root_dir(tree_ditc)
        self.converter.add_root(tree_ditc, root_path)
        #test
        self.converter.calc_children(tree_ditc)
        actual = tree_ditc['testdirs']['children']
        expected = ['subDirBoo', 'subDirFoo']
        self.assertEqual(actual, expected)

    def test_09_calc_root_totlas(self):
        #setup
        test_file = "FSHistory_test.csv"
        tree_ditc = self.converter.csv_2_tree_path_dicts(test_file)
        root_path = self.converter.find_root_dir(tree_ditc)
        self.converter.add_root(tree_ditc, root_path)
        self.converter.calc_children(tree_ditc)
        #test
        self.converter.calc_root_totlas(tree_ditc, root_path)
        actual = tree_ditc['testdirs']
        expected = {'ps': 0, 'csv': 50000000, 'log_Cn': 1, 'log': 50000000, 'zip': 0, 'other_Cn': 2, 'ps_Cn': 0, 'js_Cn': 0, 'js': 0,
                    'zip_Cn': 0, 'other': 52429824, 'zz_level': 2, 'sql_Cn': 0, 'sql': 0, 'csv_Cn': 1, 'txt_Cn': 0, 'txt': 0, 'root': True, 
                    'children': ['subDirBoo', 'subDirFoo']}
        self.assertEqual(actual, expected)

    def test_10_working_node_total_fixed(self):
        # test fixed type in this case 'log'
        #setup
        test_file = "FSHistory_test.csv"
        tree_ditc = self.converter.csv_2_tree_path_dicts(test_file)
        root_path = self.converter.find_root_dir(tree_ditc)
        self.converter.add_root(tree_ditc, root_path)
        self.converter.calc_children(tree_ditc)
        self.converter.calc_root_totlas(tree_ditc, root_path)
        #test
        working_node = {'name': 'testdirs/subDirBoo', 'node': tree_ditc['testdirs/subDirBoo']}
        actual = self.converter.working_node_total(working_node, 'log')
        expected = 100000000
        self.assertEqual(actual, expected)

    def test_10_working_node_total_total(self):
        # test total all types 
        #setup
        test_file = "FSHistory_test.csv"
        tree_ditc = self.converter.csv_2_tree_path_dicts(test_file)
        root_path = self.converter.find_root_dir(tree_ditc)
        self.converter.add_root(tree_ditc, root_path)
        self.converter.calc_children(tree_ditc)
        self.converter.calc_root_totlas(tree_ditc, root_path)
        #test
        working_node = {'name': 'testdirs/subDirBoo', 'node': tree_ditc['testdirs/subDirFoo']}
        actual = self.converter.working_node_total(working_node, 'total')
        print actual
        expected = 52429824
        self.assertEqual(actual, expected)
'''
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
'''

if __name__ == "__main__":
    unittest.main(verbosity=2)