import json
from collections import Iterable
from copy import deepcopy
from itertools import groupby

from flask import Flask, request, Response


class Converter:
    """
    Class converter `str` to `class.Table` and back
    """

    def __init__(self, cls, separator_column=None, separator_row=None):
        """
        Init class, separator setting for converter
        :param cls: Target class to convert
        :param separator_column:  Column separator
        :param separator_row: Row separator
        """
        if separator_column == '':
            raise ApiError("Column separator is empty")
        if separator_row == '':
            raise ApiError("Row separator is empty")

        self.separator_column = separator_column or '\n'
        self.separator_row = separator_row or '\t'
        self.cls = cls

    def to_table(self, table_string):
        """
        Convert string to `class.Table`
        :param table_string: String to parse
        :return: Valid `class.Table`
        :except Raise ApiError
        """
        if table_string is None:
            raise ApiError("Table_string is undefined")
        if table_string == "":
            raise ApiError("Table_string is empty")

        array = []
        for str_col in table_string.split(self.separator_column):
            str_cells = str_col.split(self.separator_row)
            array.append(str_cells)

        table = self.cls(array)

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
    Abstract table
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
        Transform table to array
        :return: Array representation
        """
        raise NotImplementedError()

    def is_valid(self):
        """
        Table valid check
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
        raise NotImplementedError()

    def __str__(self):
        """
        String representation of table
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


class Format:
    """
    Abstract converter
    """
    content_type = None

    def __init__(self, table_cls=ArrayTable):
        self.table_cls = table_cls

    def parse(self, parse_request):
        raise NotImplementedError()

    def render(self, render_table):
        raise NotImplementedError()

    def render_error(self, error):
        raise NotImplementedError()


class JsonFormat(Format):
    content_type = 'application/json'

    def parse(self, parse_request):
        json_dict = parse_request.json

        array = json_dict.get('table')

        if not isinstance(array, list):
            raise ApiError("Parse error")

        if not array:
            raise ApiError("Table is empty")

        table = self.table_cls(array)
        if not table.is_valid():
            raise ApiError("Table is not valid")
        return table

    def render(self, table):
        json_dict = dict()
        json_dict['table'] = table.to_array()
        return Response(json.dumps(json_dict), mimetype=self.content_type)

    def render_error(self, error):
        json_dict = dict()
        json_dict['message'] = error.msg
        out = json.dumps(json_dict)
        return Response(out, mimetype=self.content_type, status=error.code)


class TextFormat(Format):
    content_type = 'text/plain'

    def __init__(self, col_sep=None, row_sep=None, table_cls=ArrayTable):
        super().__init__(table_cls)
        self.converter = Converter(table_cls, separator_column=col_sep, separator_row=row_sep)

    def parse(self, parse_request):
        string = parse_request.data.decode(parse_request.charset)

        if string == "":
            raise ApiError("Table is empty")

        table = self.converter.to_table(string)
        if not table.is_valid():
            raise ApiError("Table is not valid")
        return table

    def render(self, table):
        out = self.converter.to_string(table)
        return Response(out, mimetype=self.content_type)

    def render_error(self, error):
        return Response(error.msg, mimetype=self.content_type, status=error.code)


class ApiError(Exception):
    def __init__(self, msg, code=400, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg
        self.code = code


app = Flask(__name__)


def parse_param(input_request):
    param = dict()
    param['format'] = input_request.args.get('format')
    param['sort'] = request.args.get('sort')

    separator_column = request.args.get('separator_column')
    separator_column_escaped = request.args.get('separator_column_esc') == 'True'

    separator_row = request.args.get('separator_row')
    separator_row_escaped = request.args.get('separator_row_esc') == 'True'

    if separator_column is not None and separator_column_escaped:
        separator_column = bytearray(separator_column, encoding=request.charset).decode('unicode_escape')

    if separator_row is not None and separator_row_escaped:
        separator_row = bytearray(separator_row, encoding=request.charset).decode('unicode_escape')

    param['separator_column'] = separator_column
    param['separator_row'] = separator_row

    return param


@app.route('/table', methods=["PUT"])
def sort():
    param = parse_param(request)

    body_format = param['format']
    sorting = param['sort']

    formatter = None
    try:
        if body_format is None or body_format == 'text':

            separator_column = param['separator_column']
            separator_row = param['separator_row']

            formatter = TextFormat(col_sep=separator_column, row_sep=separator_row)
        elif body_format == 'json':
            formatter = JsonFormat()
        else:
            raise ApiError("Unsupported format of body.")

        if sorting is None or sorting == 'default':
            sorter = Sorter()
        else:
            raise ApiError("Unsupported type of sorting.")

        table = formatter.parse(request)
        sorted_table = sorter.sort(table)
        response = formatter.render(sorted_table)

        return response

    except ApiError as error:
        if formatter is None:
            return Response(error.msg, status=error.code)
        else:
            return formatter.render_error(error)


if __name__ == '__main__':
    """Start point"""
    app.run(debug=True)
