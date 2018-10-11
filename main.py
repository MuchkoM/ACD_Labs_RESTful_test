from flask import Flask
from flask_restful import reqparse, Api, Resource


class Converter:
    def __init__(self, col_det='\n', row_det='\t'):
        self.col_det = col_det
        self.row_det = row_det

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


class Validate:
    @staticmethod
    def is_valid(data):
        col_count = len(data[0])
        for col in data:
            if col_count != len(col):
                break
        else:
            return True
        return False


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
parser.add_argument('string')
parser.add_argument('row_det')
parser.add_argument('col_det')
parser.add_argument('action')


class TableString(Resource):
    def post(self):
        args = parser.parse_args()
        table_string = args['string']
        action = args['action']
        col_det = args['col_det']
        row_det = args['row_det']

        if action == 'sort':

            if table_string == "":
                result = {
                    'error': True,
                    'message': 'String is empty',
                    'string': table_string,
                    'row_det': row_det,
                    'col_det': col_det,
                }
                return result, 200
            convert = Converter(col_det=col_det, row_det=row_det)
            data = convert.get_data(table_string)

            if not Validate.is_valid(data):
                result = {
                    'error': True,
                    'message': 'Rows lengths is not equal for columns',
                    'string': table_string,
                    'row_det': row_det,
                    'col_det': col_det,
                }
                return result, 200

            sort = Sorter()

            sorted_data = sort.sort(data)

            sorted_string = convert.get_str(sorted_data)

            result = {
                'string': sorted_string,
                'row_det': row_det,
                'col_det': col_det,
            }

            return result, 200


api.add_resource(TableString, '/tableString')

if __name__ == '__main__':
    app.run(debug=True)
