from flask import Flask
from flask_restful import reqparse, Api, Resource, abort


class Converter:
    col_det = '\n'
    row_det = '\t'

    def get_data(self, string):
        arr2 = []
        for str_col in string.split(self.col_det):
            str_cells = str_col.split(self.row_det)
            arr2.append(str_cells)
        return arr2

    def get_str(self, arr2):
        str_list = []
        for col in arr2:
            str_list.append(self.row_det.join(col))
        return self.col_det.join(str_list)

    def is_valid(self, data):
        col_count = len(data[0])
        for col in data:
            if col_count != len(col):
                break
        else:
            return True
        return False


class Data:
    def __init__(self, data):
        self.data = data


class Sorter:

    @staticmethod
    def key(x):

        try:
            val = float(x)
            return -1, val
        except ValueError:
            return 1, x

    def transpose(self, data):
        return [list(i) for i in zip(*data)]

    def sort(self, data):
        data_transpose = self.transpose(data)
        for col in data_transpose:
            col.sort(key=self.key)
        return self.transpose(data_transpose)


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('data')


class Sort(Resource):
    def get(self):
        args = parser.parse_args()
        string = args['data']
        if string is None:
            abort(400)

        convert = Converter()
        data = convert.get_data(string)

        if not convert.is_valid(data):
            abort(422)

        sort = Sorter()

        sorted_data = sort.sort(data)

        sorted_string = convert.get_str(sorted_data)

        result = {'data': sorted_string}

        return result, 200


api.add_resource(Sort, '/sort')

if __name__ == '__main__':
    app.run(debug=True)
