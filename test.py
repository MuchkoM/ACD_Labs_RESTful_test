import unittest

import numpy as np

from main import Converter, Sorter


class TestConverter(unittest.TestCase):
    string = "1\t2\t3\n4\t5\t6\n7\t8\t9"
    data = np.array([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])

    def test_str_to_data(self):
        converted_data = Converter().to_table(self.string)
        return self.assertTrue(np.equal(converted_data, self.data))

    def test_data_to_str(self):
        converted_str = Converter().to_string(self.data)
        return self.assertEqual(converted_str, self.string)


class TestSorter(unittest.TestCase):

    def test_data_sort1(self):
        data = [['11', '22', '31'], ['44', '15', '63'], ['57', '88', '19'], ['88', '99', '99']]
        sorted_data = [['11', '15', '19'], ['44', '22', '31'], ['57', '88', '63'], ['88', '99', '99']]

        test_data = Sorter().sort(data)
        return self.assertEqual(sorted_data, test_data)

    def test_data_sort2(self):
        data = [['a', 'b', 'c'], ['11', '22', '31'], ['44', '15', '63'], ['-', '88', '19'], ['88', '99', '99']]
        sorted_data = [['11', '15', '19'], ['44', '22', '31'], ['88', '88', '63'], ['-', '99', '99'], ['a', 'b', 'c']]

        test_data = Sorter().sort(data)
        return self.assertEqual(sorted_data, test_data)


class TestTableStringSorter(unittest.TestCase):

    def test_table_str_sort(self):
        string = "1\t2a\t3\n4\t53\t6\n7\t8\t9"
        sorted_string = "1\t8\t3\n4\t53\t6\n7\t2a\t9"

        converter = Converter()
        data = converter.to_table(string)
        sorter = Sorter()
        sorted_data = sorter.sort(data)

        sorted_string_test = converter.to_string(sorted_data)

        return self.assertEqual(sorted_string, sorted_string_test)


class TestSorterNumPy(unittest.TestCase):

    def test_data_sort1(self):
        data = [['11', '22', '31'], ['44', '15', '63'], ['57', '88', '19'], ['88', '99', '99']]
        sorted_data = [['11', '15', '19'], ['44', '22', '31'], ['57', '88', '63'], ['88', '99', '99']]
        np_data = np.array(data)
        np_result_data = np.array(sorted_data)
        np_data.sort(axis=0)
        cmp = np.array_equal(np_data, np_result_data)

        return self.assertTrue(cmp)

    def test_data_sort2(self):
        data = [['a', 'b', 'c'], ['11', '22', '31'], ['44', '15', '63'], ['-', '88', '19'], ['88', '99', '99']]

        np_data = np.array(data)

        def key_func_default(x):
            """Default sorter: str > number"""
            try:
                val = float(x)
                return -1, val
            except ValueError:
                return 1, x

        np_data = np.apply_along_axis(func1d=sorted, axis=0, arr=np_data, key=key_func_default)

        sorted_data = [['11', '15', '19'], ['44', '22', '31'], ['88', '88', '63'], ['-', '99', '99'], ['a', 'b', 'c']]
        np_result_data = np.array(sorted_data)
        cmp = np.array_equal(np_data, np_result_data)

        return self.assertTrue(cmp)


if __name__ == '__main__':
    unittest.main()
