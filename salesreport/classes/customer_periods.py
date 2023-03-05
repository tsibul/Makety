import datetime

from django.db import models
from maket.models.customer_models import Customer_all
from salesreport.report_period import ReportPeriod
from salesreport.models import Sales_docs


class CustomerPeriods(models.Model):
    class Meta:
        verbose_name = 'periods where was transactions with Client'

    customer = models.ForeignKey(Customer_all, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE)

    def __repr__(self):
        return self.customer.name + ' ' + self.period.name

    def __str__(self):
        return self.customer.name + ' ' + self.period.name

    def blank_transactions_delete(self):
        transactions = Sales_docs.objects.filter(customer=self.customer, sales_doc_date__lte=self.period.date_end,
                                                 sales_doc_date__gte=self.period.date_begin).count()
        if transactions == 0:
            transactions.delete()


def check_transactions(customer: Customer_all, period: ReportPeriod):
    output = False
    transactions = Sales_docs.objects.filter(customer=customer, sales_doc_date__lte=period.date_end,
                                             sales_doc_date__gte=period.date_begin).count()
    if transactions != 0:
        output = True


def fill_customer_periods(date_begin: datetime):
    periods_to_delete = CustomerPeriods.objects.filter(period__gte=date_begin)
    if periods_to_delete.count() == 0:
        periods_to_delete.delete()
    periods = ReportPeriod.objects.all()
    customers = Customer_all.objects.filter(date_last__gte=date_begin)
    for period in periods:
        for customer in customers:
            if check_transactions(customer, period):
                CustomerPeriods(customer=customer, period=period).save()


