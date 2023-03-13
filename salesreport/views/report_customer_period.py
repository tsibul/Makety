import datetime
from datetime import date
from functools import partial
from salesreport.reports import *
from django.shortcuts import render, HttpResponseRedirect, reverse
from salesreport.views.service import *
from salesreport.report_period import ReportPeriod



def report_customer_period(request):
    print(datetime.datetime.now().time())
    navi = 'ABC-анализ'
    report_type = request.POST['report_type']
    report_type_eco = report_type + '_eco'
    report_type_no_eco = report_type + '_no_eco'
    date_start = datetime.datetime.strptime(request.POST['date_begin'], '%Y-%m-%d').date()
    date_finish = datetime.datetime.strptime(request.POST['date_end'], '%Y-%m-%d').date()
    period_type = request.POST['period_type']
    periods = ReportPeriod.objects.filter(period=period_type, date_end__gte=date_start,
                                          date_begin__lte=date_finish).order_by('date_begin')
    Class = check_class(period_type)
    customers_periods = Class.objects.filter(period__in=periods)
    names = set(customers_periods.values_list('name', flat=True))
    grand_total_eco = sum(customers_periods.values_list(report_type_eco, flat=True))
    grand_total_no_eco = sum(customers_periods.values_list(report_type_no_eco, flat=True))
    report_eco = []
    report_no_eco = []
    print(datetime.datetime.now().time())
#    report_eco = filter(lambda x: x is not None, map(partial(eco_total, Class, periods, report_type_eco), names))
#    report_no_eco = filter(lambda x: x is not None, map(partial(eco_total, Class, periods, report_type_no_eco), names))

    for name in names:
        customers_periods = Class.objects.filter(period__in=periods, name=name)
        total_amount_eco = sum(list(customers_periods.values_list(report_type_eco, flat=True)))
        total_amount_no_eco = sum(list(customers_periods.values_list(report_type_no_eco, flat=True)))
        if total_amount_no_eco:
            report_no_eco.append(
                [name, list(customers_periods.values_list(report_type_no_eco, 'customer', 'period')),
                 total_amount_no_eco])
        if total_amount_eco:
            report_eco.append(
                [name, list(customers_periods.values_list(report_type_eco, 'customer', 'period')), total_amount_eco])
    print(datetime.datetime.now().time())
    report_eco.sort(reverse=True, key=lambda x: x[2])
    report_no_eco.sort(reverse=True, key=lambda x: x[2])
    period_types = ReportPeriod.calculatableList()
    print(datetime.datetime.now().time())
    context = {'navi': navi, 'report_eco': report_eco, 'report_no_eco': report_no_eco, 'periods': periods,
               'period_types': period_types, 'report_type': report_type, 'date_begin': date_start,
               'date_end': date_finish, 'per_type': period_type}
    print(datetime.datetime.now().time())
    return render(request, 'salesreport/reports/customer_period.html', context)


def eco_total(Class, periods, report_type_eco, name):
    customers_periods = Class.objects.filter(period__in=periods, name=name)
    total_amount_eco = sum(list(customers_periods.values_list(report_type_eco, flat=True)))
    if total_amount_eco:
        return [name, list(customers_periods.values_list(report_type_eco, 'customer', 'period')), total_amount_eco]

