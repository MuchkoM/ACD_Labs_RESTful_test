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
        data = np.array([['11', '22', '31'], ['44', '15', '63'], ['57', '88', '19'], ['88', '99', '99']])
        sorted_data = np.array([['11', '15', '19'], ['44', '22', '31'], ['57', '88', '63'], ['88', '99', '99']])

        test_data = Sorter().sort(data)
        return self.assertTrue(np.equal(sorted_data, test_data))

    def test_data_sort2(self):
        data = np.array(
            [['a', 'b', 'c'], ['11', '22', '31'], ['44', '15', '63'], ['-', '88', '19'], ['88', '99', '99']])
        sorted_data = np.array(
            [['11', '15', '19'], ['44', '22', '31'], ['88', '88', '63'], ['-', '99', '99'], ['a', 'b', 'c']])

        test_data = Sorter().sort(data)
        return self.assertTrue(np.equal(sorted_data, test_data))


class TestTableStringSorter(unittest.TestCase):

    def test_table_str_sort_string(self):
        string = "a\t2a\t3\nab\t53\t9\nab-\t8\t6"
        sorted_string = "a\t8\t3\nab\t53\t6\nab-\t2a\t9"

        converter = Converter()
        sorter = Sorter()

        data = converter.to_table(string)
        sorted_data = sorter.sort(data)
        sorted_string_test = converter.to_string(sorted_data)

        return self.assertEqual(sorted_string, sorted_string_test)

    def test_table_str_sort_string_2(self):
        string = "1\t2a\t3\n4\t53\t6\n7\t8\t9"
        sorted_string = "a\t8\t3\nab\t53\t6\nab-\t2a\t9"

        converter = Converter()
        sorter = Sorter()

        table = converter.to_table(string)
        sorted_data = sorter.sort(table)
        sorted_string_test = converter.to_string(sorted_data)

        return self.assertEqual(sorted_string_test, sorted_string, )


if __name__ == '__main__':
    unittest.main()
