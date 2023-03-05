import datetime
import calendar
from datetime import timedelta
from django.db import models


from django.utils.translation import gettext_lazy as _


month_rus = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}


class ReportPeriod(models.Model):
    class Periods(models.TextChoices):
        WEEK = 'WK', _('неделя')
        MONTH = 'MT', _('месяц')
        QUARTER = 'QT', _('квартал')
        YEAR = 'YR', _('год')
        DAY = 'DY', _('день')
        USER_DEFINED = 'UD', _('произвольный')

        def __repr__(self):
            return self.label

        def __str__(self):
            return self.label

    period = models.CharField(max_length=2, choices=Periods.choices, default=Periods.MONTH)
    date_begin = models.DateField(default=datetime.date(2000, 1, 1))
    date_end = models.DateField(default=datetime.date(2000, 1, 31))
    name = models.CharField(max_length=100)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def calculatableList(cls):
        return [cls.Periods.WEEK, cls.Periods.MONTH, cls.Periods.QUARTER, cls.Periods.YEAR]

    def setPeriod(self, date_begin: datetime, name):
        if isinstance(name, str):
            if name == 'WK':
                self.period = self.Periods.WEEK
                self.date_begin = date_begin - timedelta(days=date_begin.weekday())
                self.date_end = date_begin + timedelta(days=6)
                self.name = str(self.date_begin.isocalendar()[1]) + ' ' + self.Periods.WEEK.label + ' ' + str(
                    self.date_begin.year)

            if name == 'MT':
                self.period = self.Periods.MONTH
                self.date_begin = date_begin.replace(day=1)
                self.date_end = datetime.date(date_begin.year, date_begin.month,
                                              calendar.monthrange(date_begin.year, date_begin.month)[-1])
                self.name = month_rus[self.date_begin.month] + ' ' + str(self.date_begin.year)

            elif name == 'QT':
                self.period = self.Periods.QUARTER
                quarter = (date_begin.month - 1) // 3 + 1
                self.date_begin = datetime.date(date_begin.year, 3 * quarter - 2, 1)
                self.date_end = datetime.date(date_begin.year, 3 * quarter, 30 if quarter in [2, 3] else 31)
                self.name = str(quarter) + ' ' + self.period.QUARTER.label + ' ' + str(self.date_begin.year)

            elif name == 'YR':
                self.period = self.Periods.YEAR
                self.date_begin = datetime.date(date_begin.year, 1, 1)
                self.date_end = datetime.date(date_begin.year, 12, 31)
                self.name = str(self.date_begin.year)

            elif name == 'DY':
                self.period = self.Periods.DAY
                self.date_begin = date_begin
                self.date_end = date_begin
                self.name = self.date_begin.strftime('%d.%m.%Y')

        elif isinstance(name, datetime.date):
            self.period = self.Periods.USER_DEFINED
            self.date_begin = date_begin
            self.date_end = name
            self.name = self.date_begin.strftime('%d.%m.%Y') + ' - ' + self.date_end.strftime('%d.%m.%Y')

    def copy(self):
        return ReportPeriod(period=self.period, date_begin=self.date_begin, date_end=self.date_end, name=self.name)

    def plus(self, n: int):

        if self.period == 'MT':
            year_n = self.date_begin.year + 1 if self.date_begin.month + n > 12 else self.date_begin.year
            self.date_begin = datetime.date(year_n,
                                            (self.date_begin.month + n) % 12 if self.date_begin.month + n != 12 else 12,
                                            1)
            self.date_end = datetime.date(self.date_begin.year, self.date_begin.month,
                                          calendar.monthrange(self.date_begin.year, self.date_begin.month)[-1])
            self.name = month_rus[self.date_begin.month] + ' ' + str(self.date_begin.year)
        elif self.period == 'QT':
            year_n = self.date_begin.year + 1 if self.date_begin.month + 3 * n > 12 else self.date_begin.year
            qr = ((self.date_begin.month - 1 + 3 * n) // 3 + 1)
            quarter = qr % 4 if qr % 4 != 0 else 4
            self.date_begin = datetime.date(year_n, 3 * quarter - 2, 1)
            self.date_end = datetime.date(year_n, 3 * quarter, 30 if quarter in [2, 3] else 31)
            self.name = str(quarter) + ' ' + self.period.QUARTER.label + ' ' + str(self.date_begin.year)
        elif self.period == 'YR':
            self.date_begin = datetime.date(self.date_begin.year + n, 1, 1)
            self.date_end = datetime.date(self.date_begin.year, 12, 31)
            self.name = str(self.date_begin.year)
        elif self.period == 'DY':
            self.date_begin = self.date_begin + timedelta(days=n)
            self.date_end = self.date_begin
            self.name = self.date_begin.strftime('%d.%m.%Y')
        elif self.period == 'WK':
            self.date_begin = self.date_begin + timedelta(days=n * 7)
            self.date_end = self.date_begin + timedelta(days=6)
            self.name = str(self.date_begin.isocalendar()[1]) + ' ' + self.Periods.WEEK.label + ' ' + str(
                self.date_begin.year)
        elif self.period == 'UD':
            delta = (self.date_end - self.date_begin).days
            self.date_begin = self.date_begin + timedelta(days=delta * n)
            self.date_end = self.date_end + timedelta(days=delta * n)
            self.name = self.date_begin.strftime('%d.%m.%Y')
