import unittest

# class TestCompareTableData(unittest.TestCase):

#     def assertDictsEqualIgnoreOrder(self, expected, actual):
#         self.assertEqual(set(expected.keys()), set(actual.keys()))
#         for key in expected:
#             with self.subTest(key=key):
#                 self.assertCountEqual(expected[key], actual[key])

#     def test_compare_table_data(self):
#         input_data = {'TestAccount3': ['TestUser2', 'Testuser1', 'TestUser3'], 
#                       'TestAccount1': ['TestUser1'], 
#                       'TestAccount5': ['Testuser1']}
#         table_data = {'TestAccount3': ['Testuser1', 'TestUser2', 'TestUser3'], 
#                       'TestAccount5': ['Testuser1'], 
#                       'TestAccount1': ['TestUser1']}
#         self.assertDictsEqualIgnoreOrder(input_data, table_data)

import unittest

class TestCompareTableData(unittest.TestCase):

    def test_compare_table_data(self):
        input_data = {'TestAccount3': ['TestUser2', 'Testuser1', 'TestUser3'], 
                      'TestAccount1': ['TestUser1'], 
                      'TestAccount5': ['Testuser1']}
        table_data = {'TestAccount3': ['Testuser1', 'TestUser2', 'TestUser3'], 
                      'TestAccount5': ['Testuser1'], 
                      'TestAccount1': ['TestUser1']}
        with self.subTest('Compare each element'):
            for key in input_data:
                with self.subTest(key=key):
                    print(key, input_data[key])  
                    self.assertEqual(sorted(input_data[key]), sorted(table_data[key]), f"{key} doesn't match")
        self.assertEqual(sorted(input_data.keys()), sorted(table_data.keys()), "Keys don't match")
