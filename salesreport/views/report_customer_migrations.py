import datetime
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.db.models import Q
from salesreport.views.service import *
from salesreport.report_period import ReportPeriod


class MigrationReport:

    def __init__(self, *args):
        if len(args) == 5:
            self.period = args[0]
            self.clients_start = args[1]
            self.clients_come = args[2]
            self.clients_gone = args[3]
            self.clients_sales = args[4]
            self.clients_end = self.clients_start + self.clients_come - self.clients_gone
            if self.clients_start != 0:
                self.clients_come_percent = self.clients_come / self.clients_start * 100
                self.clients_gone_percent = self.clients_gone / self.clients_start * 100
                self.clients_conversion = self.clients_sales / self.clients_start * 100

        else:
            raise TypeError("wrong number of args")


def report_customer_migrations(request):
    navi = 'Миграции клиентов'
    period_types = ReportPeriod.calculatableList()
    date_start = datetime.datetime.strptime(request.POST['date_begin'], '%Y-%m-%d').date()
    date_finish = datetime.datetime.strptime(request.POST['date_end'], '%Y-%m-%d').date()
    period_type = request.POST['period_type']
    periods = ReportPeriod.objects.filter(period=period_type, date_end__gte=date_start,
                                          date_begin__lte=date_finish).order_by('date_begin')
    Class = check_class(period_type)

    migration_list = []
    for period in periods:
        date_begin_3_years_ago = period.date_begin.replace(year=period.date_begin.year - 3)
        date_end_3_years_ago = period.date_end.replace(year=period.date_end.year - 3)
        customer_start_no = Customer_all.objects.filter(date_last__gte=date_begin_3_years_ago,
                                                        date_first__lt=period.date_begin, internal=False,
                                                        customer_group=None).count()
        group_start_no = Customer_groups.objects.filter(date_last__gte=date_begin_3_years_ago,
                                                        date_first__lt=period.date_begin).count()
        clients_quantity_start = customer_start_no + group_start_no
        customer_come_no = Customer_all.objects.filter(date_first__gte=period.date_begin,
                                                       date_first__lte=period.date_end, internal=False,
                                                       customer_group=None).count()
        group_come_no = Customer_groups.objects.filter(date_first__gte=period.date_begin,
                                                       date_first__lte=period.date_end).count()
        clients_quantity_come = customer_come_no + group_come_no
        customer_gone_no = Customer_all.objects.filter(date_last__gte=date_begin_3_years_ago,
                                                       date_last__lte=date_end_3_years_ago, internal=False,
                                                       customer_group=None).count()
        group_gone_no = Customer_groups.objects.filter(date_last__gte=date_begin_3_years_ago,
                                                       date_last__lte=date_end_3_years_ago).count()
        clients_quantity_gone = customer_gone_no + group_gone_no
        clients_sales_quantity = Class.objects.filter(~Q(sales_with_vat=0) & Q(period=period)).count()
        migration_list.append(
            MigrationReport(period, clients_quantity_start, clients_quantity_come, clients_quantity_gone,
                            clients_sales_quantity))

    context = {'navi': navi, 'period_types': period_types, 'per_type': period_type, 'date_begin': date_start,
               'date_end': date_finish, 'migration_list': migration_list}
    return render(request, 'salesreport/reports/customer_migrations.html', context)
