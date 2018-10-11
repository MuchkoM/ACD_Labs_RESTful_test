import unittest

from main import Converter, Sorter


class TestConverter(unittest.TestCase):
    string = """1\t2\t3
4\t5\t6
7\t8\t9"""
    data = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

    def test_str_to_data(self):
        converted_data = Converter().get_data(self.string)
        return self.assertEqual(converted_data, self.data)

    def test_data_to_str(self):
        converted_str = Converter().get_str(self.data)
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

        convert = Converter()
        data = convert.get_data(string)

        sort = Sorter()

        sorted_data = sort.sort(data)

        sorted_string_test = convert.get_str(sorted_data)

        return self.assertEqual(sorted_string, sorted_string_test)


class TestApiSorter(unittest.TestCase):

    def test_table_str_sort(self):
        import json
        import requests
        url = 'http://127.0.0.1:5000/sort'
        data = {
            "string": "1\t2a\t3\n4\t53\t6\n7\t8\t9",
            "row_det": "\t",
            "col_det": "\n",
        }

        data = json.dumps(data)

        response = requests.get(url, data=data)
        print(response.text)
        return self.assertEqual(None, None)


if __name__ == '__main__':
    unittest.main()
