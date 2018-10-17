import unittest

from main import Converter, Sorter, ArrayTable, TableStringSortingTask


class TestConverter(unittest.TestCase):
    string = "1\t2\t3\n4\t5\t6\n7\t8\t9"
    data = ArrayTable([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])

    def test_str_to_data(self):
        converted_data = Converter(ArrayTable).to_table(self.string)
        return self.assertEqual(converted_data.to_array(), self.data.to_array())

    def test_data_to_str(self):
        converted_str = Converter(ArrayTable).to_string(self.data)
        return self.assertEqual(converted_str, self.string)


class TestSorter(unittest.TestCase):

    def test_data_sort1(self):
        data = ArrayTable([['11', '22', '31'], ['44', '15', '63'], ['57', '88', '19'], ['88', '99', '99']])
        sorted_data = ArrayTable([['11', '15', '19'], ['44', '22', '31'], ['57', '88', '63'], ['88', '99', '99']])

        test_data = Sorter().sort(data)
        return self.assertEqual(test_data.to_array(), sorted_data.to_array())

    def test_data_sort2(self):
        data = ArrayTable(
            [['a', 'b', 'c'], ['11', '22', '31'], ['44', '15', '63'], ['-', '88', '19'], ['88', '99', '99']])
        sorted_data = ArrayTable(
            [['11', '15', '19'], ['44', '22', '31'], ['88', '88', '63'], ['-', '99', '99'], ['a', 'b', 'c']])

        test_data = Sorter().sort(data)
        return self.assertEqual(test_data.to_array(), sorted_data.to_array())


class TestTableStringSorter(unittest.TestCase):

    def test_table_str_sort_string(self):
        string = "a\t2a\t3\nab\t53\t9\nab-\t8\t6"
        sorted_string = "a\t8\t3\nab\t53\t6\nab-\t2a\t9"

        task = TableStringSortingTask(string)
        task.perform()
        sorted_string_test = task.result()

        return self.assertEqual(sorted_string, sorted_string_test)

    def test_table_str_sort_string_2(self):
        string = "ab\t2a\t3\na\t53\t9\nab-\t8\t6"
        sorted_string = "a\t8\t3\nab\t53\t6\nab-\t2a\t9"

        task = TableStringSortingTask(string)
        task.perform()
        sorted_string_test = task.result()

        return self.assertEqual(sorted_string, sorted_string_test)


if __name__ == '__main__':
    unittest.main()
