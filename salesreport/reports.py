from abc import ABC, abstractmethod
import datetime
import calendar
from datetime import timedelta
from maket.models import Good_crm_type, Good_matrix_type, Customer_all
from salesreport.models import Sales_doc_imports
import pandas as pd

from orders.models import models


class Period:

    def __init__(self, date_begin: datetime, name):
        if isinstance(name, str):
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
            elif name == 'day':
                self.name = name
                self.date_begin = date_begin
                self.date_end = date_begin
            else:
                self.name = None
        elif isinstance(name, datetime):
            self.name = 'user defined'
            self.date_begin = date_begin
            self.date_end = name

    def __repr__(self):
        if self.name == 'user defined':
            return self.date_begin.strftime('%d.%m.%Y') + '-' + self.date_end.strftime('%d.%m.%Y')
        elif not self.name:
            return None
        else:
            return self.name + ' from ' + self.date_begin.strftime('%d.%m.%Y')

    def __str__(self):
        if self.name == 'user defined':
            return self.date_begin.strftime('%d.%m.%Y') + '-' + self.date_end.strftime('%d.%m.%Y')
        elif not self.name:
            return None
        else:
            return self.name + ' from ' + self.date_begin.strftime('%d.%m.%Y')


    def copy(self):
        return Period(self.date_begin, self.name)

    def plus(self, n: int):
        if self.name == 'month':
            year_n = self.date_begin.year + 1 if self.date_begin.month + n > 12 else self.date_begin.year
            self.date_begin = datetime.date(year_n,
                                            (self.date_begin.month + n) % 12 if self.date_begin.month + n != 12 else 12,
                                            1)
            self.date_end = datetime.date(self.date_begin.year, self.date_begin.month,
                                          calendar.monthrange(self.date_begin.year, self.date_begin.month)[-1])
        elif self.name == 'quarter':
            year_n = self.date_begin.year + 1 if self.date_begin.month + 3 * n > 12 else self.date_begin.year
            quarter = (self.date_begin.month - 1 + 3 * n) // 3 + 1
            self.date_begin = datetime.date(year_n, 3 * quarter - 2, 1)
            self.date_end = datetime.date(year_n, 3 * quarter + 1, 1) + timedelta(days=-1)
        elif self.name == 'year':
            self.date_begin = datetime.date(self.date_begin.year + n, 1, 1)
            self.date_end = datetime.date(self.date_begin.year + n, 12, 31)
        elif self.name == 'day':
            self.date_begin = self.date_begin + timedelta(days=n)
            self.date_end = self.date_begin
        elif self.name == 'user defined':
            delta = (self.date_end - self.date_begin).days
            self.date_begin = self.date_begin + timedelta(days=delta * n)
            self.date_end = self.date_end + timedelta(days=delta * n)


class AverageBill:

    def __init__(self, period: Period):
        self.period = period


class ClientMigration:

    def __init__(self, period: Period):
        self.period = period


class GoodGroupSales:

    def __init__(self, period: Period):
        self.period = period


class RepeatedSales:

    def __init__(self, period: Period):
        self.period = period


class SalesDinamicsCrm:

    def __init__(self, period: Period):
        #        self.date_begin = period.date_begin
        #        self.date_end = period.date_end
        self.period = period.copy()
        goods = Good_crm_type.objects.all()
        sales_list = {}
        total = 0
        for good in goods:
            sales_list[good] = [0, 0, 0, 0]
            sales = Sales_doc_imports.objects.filter(detail_set__crm=good, sales_doc_date__gte=self.period.date_begin,
                                                     sales_doc_date__lte=self.period.date_end,
                                                     customer_all__internal=False)
            for sale in sales:
                sales_list[good][0] += sale.quantity
                sales_list[good][1] += sale.sale_with_vat
                sales_list[good][2] += sale.sale_without_vat - sale.buy_without_vat
        for good in goods:
            total += sales_list[good][1]
        for good in goods:
            sales_list[good][3] = sales_list[good][1] / total * 100
        self.sales_result = sales_list
        self.total = total

    def __repr__(self):
        return self.period

    def __str__(self):
        return self.period

class CustomerSales(ABC):
    @abstractmethod
    def __init__(self, period: Period, customer: Customer_all):
        self.period = period.copy()
        self.customer = customer



class CustomerSalesPeriod:

    def __init__(self, period: Period, customer: Customer_all):
        self.period = period.copy()
        self.customer = customer
        self.sales = sum(Sales_doc_imports.objects.filter(sales_doc_date__gte=self.period.date_begin, sales_doc_date__lte=self.period.date_end,
                                                     customer_all=customer).values_list('sale_with_vat', flat=True))
    def __repr__(self):
        return self.customer.name + ' ' + str(self.sales)


class CustomerSalesPeriodsNumber(CustomerSalesPeriod):

    def __init__(self, period: Period, customer: Customer_all, number_of_periods: int):
        super().__init__(period, customer)
        i = 0
        sales_total = 0
        period_tmp = period.copy()
        self.sales = []
        while i < number_of_periods:
            period_tmp.plus(1)
            tmp = CustomerSalesPeriod(period_tmp, self.customer).sales
            self.sales.append(tmp)
            sales_total += tmp
            i += 1
        self.sales_total = sales_total

    def __repr__(self):
        return self.customer.name + ' ' + str(self.sales_total)

class CustomerSalesCollection:

    def __init__(self, period: Period, number_of_periods: int = None):
        customers = Customer_all.objects.all().order_by('name')
        collection = []
        for customer in customers:
            customer_report = CustomerSalesPeriodsNumber(period, customer, number_of_periods)
            if customer_report.sales_total:
                collection.append(customer_report)
        self.collection = collection




class CustomerSalesRange(CustomerSalesPeriod):

    def __init__(self, period: Period, customer: Customer_all, number_of_periods: int):
        super().__init__(period, customer)
        self.period = period
        self.customer = customer
        self.sales = []
        i = 0
        while i < number_of_periods:
            period_tmp = self.period.plus(i)
            self.sales.append(CustomerSalesPeriod(period_tmp, self.customer).sales)
            i += 1


class CustomerSalesCollectionPeriod:

    def __init__(self, period: Period):
        self.period = period.copy()
        customers = Customer_all.objects.all().order_by('name')
        collection = []
        for customer in customers:
            collection.append(CustomerSalesPeriod(self.period, customer))
        self.customer_sales = collection

    def __repr__(self):
        return self.period
