from flask import Flask, request
from flask_restful import  Api, Resource
from itertools import groupby


class Converter:
    def __init__(self, col_det=None, row_det=None):
        self.col_det = col_det or '\n'
        self.row_det = row_det or '\t'

    def get_table(self, string):
        arr2 = []
        for str_col in string.split(self.col_det):
            str_cells = str_col.split(self.row_det)
            arr2.append(str_cells)
        return arr2

    def get_string(self, arr2):
        str_list = []
        for col in arr2:
            str_list.append(self.row_det.join(col))
        return self.col_det.join(str_list)


class DataMethods:
    @staticmethod
    def is_valid(data):
        if data is None:
            return False

        g = groupby(data, key=len)
        return next(g, True) and not next(g, False)

    @staticmethod
    def transpose(data):
        return [list(i) for i in zip(*data)]


class Sorter:
    def __init__(self, data, key=None):
        if key is None:
            def key_func_default(x):
                try:
                    val = float(x)
                    return -1, val
                except ValueError:
                    return 1, x

            self.key = key_func_default
        else:
            self.key = key

        self.data = data

    def sort(self):
        data_transpose = DataMethods.transpose(self.data)
        for col in data_transpose:
            col.sort(key=self.key)
        return DataMethods.transpose(data_transpose)


app = Flask(__name__)
api = Api(app)


class TableString(Resource):
    def put(self):
        json_data = request.get_json(force=True)

        table_string = json_data.get('table', None)
        row_det = json_data.get('row_det', None)
        col_det = json_data.get('col_det', None)

        if table_string is None or table_string == "":
            json_data['message'] = 'String is empty or undefined'
            json_data['success'] = False
            return json_data, 422

        converter = Converter(col_det=col_det, row_det=row_det)

        table = converter.get_table(table_string)

        if not DataMethods.is_valid(table):
            json_data['message'] = 'Table is not valid'
            json_data['success'] = False
            return json_data, 422

        sorter = Sorter(table)

        sorted_table = sorter.sort()
        sorted_string_table = converter.get_string(sorted_table)

        json_data['table'] = sorted_string_table
        json_data['success'] = True
        return json_data, 200


api.add_resource(TableString, '/table_string')

if __name__ == '__main__':
    app.run(debug=True)
