import unittest
import converter
import sorter


class TestConverter(unittest.TestCase):
    string = """1\t2\t3
4\t5\t6
7\t8\t9"""
    data = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

    def test_str_to_data(self):
        converted_data = converter.Converter().get_data(self.string)
        return self.assertEqual(converted_data, self.data)

    def test_data_to_str(self):
        converted_str = converter.Converter().get_str(self.data)
        return self.assertEqual(converted_str, self.string)


class TestSorter(unittest.TestCase):
    data = [['11', '22', '31'], ['44', '15', '63'], ['57', '88', '19']]
    sorted_data = [['11', '15', '19'], ['44', '22', '31'], ['57', '88', '63']]

    def test_data_to_str(self):
        test_data = sorter.Sorter().sort(self.data)
        return self.assertEqual(test_data, self.sorted_data)


if __name__ == '__main__':
    unittest.main()
