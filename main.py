from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}




class Sorting(Resource):
    def get(self):
        data = request.form['data']

        return {todo_id: todos[todo_id]}


api.add_resource(Sorting, '/sort')

if __name__ == '__main__':
    app.run(debug=True)
