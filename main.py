from itertools import groupby

import numpy as np
from flask import Flask, request
from flask_restful import Api, Resource


def is_valid(table):
    """
    Table valid check
    :return: True is valid, False is not valid
    """
    if table is None:
        return False

    g = groupby(table, key=len)
    return next(g, True) and not next(g, False)


class Converter:
    """Class converter string to 2D array and back"""

    def __init__(self, separator_column=None, separator_row=None):
        """ Set separator for string """
        self.separator_column = separator_column or '\n'
        self.separator_row = separator_row or '\t'

    def to_table(self, string):
        """ Convert string to 2D array with """
        array = []
        for str_col in string.split(self.separator_column):
            str_cells = str_col.split(self.separator_row)
            array.append(str_cells)

        if not is_valid(array):
            raise ValueError()

        return np.array(array)

    def to_string(self, table):
        str_list = []
        for col in table:
            str_list.append(self.separator_row.join(col))
        return self.separator_column.join(str_list)


class Sorter:
    def sort(self, table):
        def key(x):
            """Default sorter: str > number"""
            try:
                val = float(x)
                return -1, val
            except ValueError:
                return 1, x

        return np.apply_along_axis(func1d=sorted, axis=0, arr=table, key=key)


app = Flask(__name__)
api = Api(app)


class TableStringResource(Resource):
    def put(self):
        """ Sorting table in string format from json table"""
        json_data = request.get_json(force=True)

        table_string = json_data.get('table', None)
        separator_row = json_data.get('row_det', None)
        separator_column = json_data.get('separator_column', None)

        if table_string is None or table_string == "":
            json_data['message'] = 'String is empty or undefined'
            return json_data, 400

        converter = Converter(separator_column=separator_column, separator_row=separator_row)

        try:
            table = converter.to_table(table_string)
        except ValueError:
            json_data['message'] = 'Table is not valid'
            return json_data, 422

        sorter = Sorter()

        sorted_table = sorter.sort(table)

        sorted_string_table = converter.to_string(sorted_table)

        json_data['table'] = sorted_string_table
        return json_data, 200


api.add_resource(TableStringResource, '/table_string')
if __name__ == '__main__':
    """
    Start point
    """
    app.run(debug=True)
