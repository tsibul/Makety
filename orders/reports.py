import datetime
import calendar
from datetime import timedelta
import pandas as pd

from .models import models


class Period:

    def __init__(self, date_begin: datetime, name):
        if type(name) == 'str':
            if name == 'month':
                self.name = name
                self.date_begin = date_begin.replace(day=1)
                self.date_end = datetime.date(date_begin.year, date_begin.month,
                                              calendar.monthrange(date_begin.year, date_begin.month)[-1])
            elif name == 'quarter':
                self.name = name
                quarter = (date_begin.month - 1) // 3 + 1
                self.date_begin = datetime.date(date_begin.year, 3 * quarter - 2, 1)
                self.date_end = datetime.date(date_begin.year, 3 * quarter + 1, 1) + timedelta(days=-1)
            elif name == 'year':
                self.name = name
                self.date_begin = datetime.date(date_begin.year, 1, 1)
                self.date_end = datetime.date(date_begin.year, 12, 31)
            else:
                self.name = None
        elif type(name) == 'datetime':
            self.name = 'user defined'
            self.date_begin = date_begin
            self.date_end = name

    def plus(self, n: int):
        if self.name == 'month':
            year_n = self.date_begin.year if self.date_begin.month + n > 12 else self.date_begin.year + 1
            self.date_begin = datetime.date(year_n, (self.date_begin.month + n) % 12, 1)
            self.date_end = datetime.date(self.date_begin.year, self.date_begin.month,
                                              calendar.monthrange(self.date_begin.year, self.date_begin.month)[-1])
        elif self.name == 'quarter':
            year_n = self.date_begin.year if self.date_begin.month + 3 * n > 12 else self.date_begin.year + 1
            quarter = (self.date_begin.month - 1 + 3 * n) // 3 + 1
            self.date_begin = datetime.date(year_n, 3 * quarter - 2, 1)
            self.date_end = datetime.date(year_n, 3 * quarter + 1, 1) + timedelta(days=-1)
        elif self.name == 'year':
            self.date_begin = datetime.date(self.date_begin.year + n, 1, 1)
            self.date_end = datetime.date(self.date_begin.year + n, 12, 31)


class AverageCheck:

    def __init__(self, period: Period):
        self.period = period
