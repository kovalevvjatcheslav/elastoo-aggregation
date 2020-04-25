from functools import wraps

from flask import Flask, request, jsonify

from models import DataSet, ColumnException

app = Flask(__name__)


@app.before_first_request
def init_dataset():
    app.dataset = DataSet.from_csv('datasource.csv')


def catch_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ColumnException as error:
            response = jsonify({'error': str(error)})
            response.status_code = 400
            return response
    return wrapper


@app.route('/min', methods=['GET'])
@catch_exception
def get_min():
    column_names = request.args.getlist('columns') if request.args.getlist('columns') else None
    return app.dataset.min(column_names=column_names)


@app.route('/max', methods=['GET'])
@catch_exception
def get_max():
    column_names = request.args.getlist('columns') if request.args.getlist('columns') else None
    return app.dataset.max(column_names=column_names)


@app.route('/sorted', methods=['GET'])
@catch_exception
def get_sort():
    column_names = request.args.getlist('columns') if request.args.getlist('columns') else None
    return app.dataset.sort(column_names=column_names, reverse=True)


if __name__ == "__main__":
    app.run(host='localhost', port='8000', debug=True)
