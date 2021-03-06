from typing import Union
from datetime import datetime
from csv import DictReader
from operator import gt, lt
import bisect

from dateutil.parser import parse, ParserError


def _insort_reverse(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x > a[mid]:
            hi = mid
        else:
            lo = mid+1
    a.insert(lo, x)


class ColumnException(Exception):
    pass


class Row:
    def __init__(self, row_id: Union[int, str], data: {str: Union[int, float, str, datetime]}):
        self.row_id = row_id
        self.data = self.__parse_data(data)

    def get_column_names(self):
        return self.data.keys()

    def __str__(self):
        return str((self.row_id, self.data))

    @classmethod
    def __parse_data(cls, data):
        return {key: cls.__parse_value(value) for key, value in data.items()}

    @staticmethod
    def __parse_value(value):
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        try:
            return parse(value)
        except ParserError:
            return value


class DataSet:
    def __init__(self, rows: [Row], column_names: [str]):
        self.rows = rows
        self.column_names = column_names

    @staticmethod
    def from_csv(csv_path: str):
        with open(csv_path) as data_file:
            reader = DictReader(data_file)
            rows = []
            row_count = 0
            for row in reader:
                rows.append(Row(row_id=row_count, data=row))
                row_count += 1
        column_names = rows[0].get_column_names()
        return DataSet(rows, column_names)

    def min(self, column_names: [str] = None):
        return self.__min_max(lt, column_names)

    def max(self, column_names: [str] = None):
        return self.__min_max(gt, column_names)

    def sort(self, column_names: [str] = None, reverse: bool = False):
        if column_names is None:
            column_names = self.column_names
        else:
            self.__validate_column_names(column_names)
        if reverse:
            insort = _insort_reverse
        else:
            insort = bisect.insort
        columns = {column_name: [] for column_name in column_names}
        for row in self.rows:
            for column_name in column_names:
                insort(columns[column_name], row.data.get(column_name))
        return columns

    def __min_max(self, infix_operator: Union[gt, lt], column_names: [str] = None):
        if column_names is None:
            column_names = self.column_names
        else:
            self.__validate_column_names(column_names)
        result = {}
        for row in self.rows:
            for column_name in column_names:
                if result.get(column_name) is None or infix_operator(row.data.get(column_name), result[column_name]):
                    result[column_name] = row.data.get(column_name)
        return result

    def __validate_column_names(self, column_names: [str] = None):
        if column_names is not None and not set(self.column_names).issuperset(set(column_names)):
            raise ColumnException(f'Column names {set(column_names) - set(self.column_names)} not found')
        return column_names

    def __str__(self):
        return str([str(row) for row in self.rows])
