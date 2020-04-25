from functools import wraps

from flask import Flask, request, jsonify

from models import DataSet, ColumnException

app = Flask(__name__)


@app.before_first_request
def init_dataset():
    app.dataset = DataSet.from_csv('datasource.csv')


def __prepare_args(args):
    columns = args.get('columns')
    if columns is not None:
        columns = columns.split(',')
    return columns


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
    return app.dataset.min(column_names=__prepare_args(request.args))


@app.route('/max', methods=['GET'])
@catch_exception
def get_max():
    return app.dataset.max(column_names=__prepare_args(request.args))


@app.route('/sorted', methods=['GET'])
@catch_exception
def get_sort():
    return app.dataset.sort(column_names=__prepare_args(request.args), reverse=True)


if __name__ == "__main__":
    app.run(host='localhost', port='8000', debug=True)
