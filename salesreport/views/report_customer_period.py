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
    #    report_eco = filter(lambda x: x is not None, map(partial(create_final_list, Class, periods, report_type_eco), names))
    #    report_no_eco = filter(lambda x: x is not None, map(partial(create_final_list, Class, periods, report_type_no_eco), names))

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
    report_eco_c, report_eco = abc_check(report_eco, grand_total_eco)
    report_no_eco_c, report_no_eco = abc_check(report_no_eco, grand_total_no_eco)
    context = {'navi': navi, 'report_eco': report_eco, 'report_no_eco': report_no_eco, 'periods': periods,
               'period_types': period_types, 'report_type': report_type, 'date_begin': date_start,
               'date_end': date_finish, 'per_type': period_type, 'grand_total_eco': grand_total_eco,
               'grand_total_no_eco': grand_total_no_eco}
    print(datetime.datetime.now().time())
    return render(request, 'salesreport/reports/customer_period.html', context)


def create_final_list(Class, periods, report_type_eco, name):
    customers_periods = Class.objects.filter(period__in=periods, name=name)
    total_amount_eco = sum(list(customers_periods.values_list(report_type_eco, flat=True)))
    if total_amount_eco:
        return [name, list(customers_periods.values_list(report_type_eco, 'customer', 'period')), total_amount_eco]


def abc_check(report, grand_total):
    start_letter = 'A'
    tmp_sum = 0
    number_of_periods = [(0, 0, 0) for i in report[0][1]]
    report_total_c = ['Клиенты "C"', number_of_periods, 0]
    report_c = []
    for rep in report:
        rep.append(start_letter)
        tmp_sum += rep[2]
        if grand_total * 0.95 > tmp_sum > grand_total * 0.8:
            start_letter = 'B'
        elif grand_total * 0.95 < tmp_sum:
            start_letter = 'C'
        if rep[3] == 'C':
            report_total_c[1] = list(map(lambda x: (x[0][0] + x[1][0], 0, 0), list(zip(rep[1], report_total_c[1]))))
            report_total_c[2] += rep[2]
            report_c.append(rep)
    report_total_c.append('C')
    report_n = list(filter(lambda x: x[3] != 'C', report))
    report_n.append(report_total_c)
    return report_c, report_n
