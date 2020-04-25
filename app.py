from flask import Flask, request

from models import DataSet

app = Flask(__name__)


@app.before_first_request
def init_dataset():
    app.dataset = DataSet.from_csv('datasource.csv')


def __prepare_args(args):
    columns = args.get('columns')
    if columns is not None:
        columns = columns.split(',')
    return columns


@app.route('/min', methods=['GET'])
def get_min():
    return app.dataset.min(column_names=__prepare_args(request.args))


@app.route('/max', methods=['GET'])
def get_max():
    return app.dataset.max(column_names=__prepare_args(request.args))


if __name__ == "__main__":
    app.run(host='localhost', port='8000', debug=True)
