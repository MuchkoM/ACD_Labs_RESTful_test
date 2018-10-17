from collections import Iterable
from copy import deepcopy
from itertools import groupby

import numpy as np
from flask import Flask, request
from flask_restful import Api, Resource


class TableStringSortingTask:
    """
        TableStringSorting performer
    """

    def __init__(self, table_string, separator_column, separator_row):
        """
        Init task param
        :param table_string: String with table
        :param separator_column:  Column separator
        :param separator_row: Row separator
        """
        self.input_sting = table_string
        self.converter = Converter(ArrayTable, separator_column=separator_column, separator_row=separator_row)
        self.sorter = Sorter()
        self.output_string = None
        self.isSuccess = False

    def perform(self):
        """
        Task performer
        """
        table = self.converter.to_table(self.input_sting)
        table_sorted = self.sorter.sort(table)
        self.output_string = self.converter.to_string(table_sorted)
        self.isSuccess = True

    def result(self):
        """
        Result of the task
        :return: String with sorted table
        """
        return self.output_string


class TableStringException(Exception):
    """
    Exception for TableStringSortingTask
    """

    def __init__(self, message=None, code=None, *args, **kwargs):
        """
        Init TableStringException
        :param message: Error description
        :param code: HTTP code of error
        :param args: args for super
        :param kwargs: kwargs for super
        """
        super().__init__(args, kwargs)
        self.message = message or "TableString exception"
        self.code = code or 422


class Converter:
    """
    Class converter `str` to `class.Table` and back
    """

    def __init__(self, cls, separator_column=None, separator_row=None):
        """
        Init class,separator setting for converter
        :param cls: Target class to convert
        :param separator_column:  Column separator
        :param separator_row: Row separator
        """
        if separator_column == '':
            raise TableStringException("Column separator is empty")
        if separator_row == '':
            raise TableStringException("Row separator is empty")

        self.separator_column = separator_column or '\n'
        self.separator_row = separator_row or '\t'
        self.cls = cls

    def to_table(self, table_string):
        """
        Convert string to NumPy 2D-array
        :param table_string: String to parse
        :return: Valid NumPy 2D-array
        :except Rise TableStringException with error message and status code
        """
        if table_string is None:
            raise TableStringException("Table_string is undefined")
        if table_string == "":
            raise TableStringException("Table_string is empty")

        array = []
        for str_col in table_string.split(self.separator_column):
            str_cells = str_col.split(self.separator_row)
            array.append(str_cells)

        table = self.cls(array)

        if not table.is_valid():
            raise TableStringException("Table is not valid")

        return table

    def to_string(self, table):
        """
        Convert string to NumPy 2D-array with
        :param table: 2D-array to convert
        :return: String interpretation of array
        :except Rise TableStringException with error message and status code
        """
        str_list = []
        for col in table.to_array():
            str_list.append(self.separator_row.join(col))
        return self.separator_column.join(str_list)


class Table:
    """
    Abstract array
    """
    table = None

    def copy(self):
        """
        Copy of object
        :return: deepcopy of self
        """
        return deepcopy(self)

    def to_array(self):
        """
        Transform object to array
        :return: Array representation
        """
        pass

    def is_valid(self):
        """
        Table valid check
        :return: True is valid, False is not valid
        """
        if self.table is None:
            return False
        if not isinstance(self.table, Iterable):
            return False

        g = groupby(self.table, key=len)
        return next(g, True) and not next(g, False)

    def sort(self, axis, key):
        """
        Sort self.table
        :param axis: sort axis
        :param key: key function for sort
        """
        pass

    def __str__(self):
        """
        String representation of self.table
        :return: representation
        """
        return str(self.table)


# class NumPyTable(Table):
#     def __init__(self, array):
#         self.table: np.ndarray = np.array(array)
#
#     def to_array(self):
#         return self.table.tolist()
#
#     def sort(self, axis, key):
#         """
#         Sort self.table
#         :param axis: sort axis
#         :param key: key function for sort
#         """
#         self.table = np.apply_along_axis(func1d=sorted, axis=axis, arr=self.table, key=key)


class ArrayTable(Table):
    def __init__(self, array):
        self.table = array

    def to_array(self):
        return deepcopy(self.table)

    def transpose(self):
        """
        Transpose self.table
        :return:
        """
        self.table = [list(x) for x in zip(*self.table)]

    def sort(self, axis, key):
        if axis == 0:
            self.transpose()
        for col in self.table:
            col.sort(key=key)
        if axis == 0:
            self.transpose()


class Sorter:
    def __init__(self, axis=0, key=None):
        """
        Init Sorter
        :param axis: axis of sort : 0 is vertical, 1 is horizontal
        :param key: key function for sorting
        """

        def default_key_sort(x):
            """Default sorter: str > number"""
            try:
                val = float(x)
                return -1, val
            except ValueError:
                return 1, x

        self.key = key or default_key_sort
        self.axis = axis

    def sort(self, table):
        """
        Sorting table with self.key function
        :return: `class.Table` sorted
        """
        sorted_table = table.copy()
        sorted_table.sort(axis=self.axis, key=self.key)
        return sorted_table


app = Flask(__name__)
api = Api(app)


class TableStringResource(Resource):
    def put(self):
        """ Sorting table in string format from json string_table"""
        json_data = request.get_json()

        table_string = json_data.get('table_string', None)
        separator_row = json_data.get('separator_row', None)
        separator_column = json_data.get('separator_column', None)

        try:
            task = TableStringSortingTask(table_string=table_string, separator_column=separator_column,
                                          separator_row=separator_row)
            task.perform()
            if task.isSuccess:
                sorted_table_string = task.result()
            else:
                raise TableStringException

        except TableStringException as e:
            json_data['message'] = e.message
            return json_data, e.code

        json_data['table_string'] = sorted_table_string
        return json_data, 200


api.add_resource(TableStringResource, '/table_string')
if __name__ == '__main__':
    """Start point"""
    app.run(debug=True)
