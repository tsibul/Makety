import datetime
from django.shortcuts import render, HttpResponseRedirect, reverse
from salesreport.views.service import *
from salesreport.report_period import ReportPeriod





def report_customer_geography(request):
    navi = 'Типы и география'
    period_types = ReportPeriod.calculatableList()
    report_type = request.POST['report_type']
    report_type_eco = report_type + '_eco'
    report_type_no_eco = report_type + '_no_eco'
    date_start = datetime.datetime.strptime(request.POST['date_begin'], '%Y-%m-%d').date()
    date_finish = datetime.datetime.strptime(request.POST['date_end'], '%Y-%m-%d').date()
    period_type = request.POST['period_type']
    periods = ReportPeriod.objects.filter(period=period_type, date_end__gte=date_start,
                                          date_begin__lte=date_finish).order_by('date_begin')
    Class = check_class(period_type)
    customers_period = Class.objects.filter(period__in=periods)

    context = {'navi': navi,  'report_type': report_type, 'date_begin': date_start,
               'date_end': date_finish, 'per_type': period_type, 'period_types': period_types,}
    return render(request, 'salesreport/reports/customer_geography.html', context)


def create_final_list(Class, periods, report_type_eco, name):
    customers_periods = Class.objects.filter(period__in=periods, name=name)
    total_amount_eco = sum(list(customers_periods.values_list(report_type_eco, flat=True)))
    if total_amount_eco:
        return [name, list(customers_periods.values_list(report_type_eco, 'customer', 'period')), total_amount_eco]


def abc_check(report, grand_total):
    start_letter = 'A'
    tmp_sum = 0
    number_of_periods = [(0, 0, 0) for i in report[0][1]]
    report_total_a, report_total_b, report_total_c = ['Клиенты "A"', number_of_periods, 0], \
                                                     ['Клиенты "B"', number_of_periods, 0], \
                                                     ['Клиенты "C"', number_of_periods, 0]
    report_a, report_b, report_c = [], [], []
    for rep in report:
        rep.append(start_letter)
        tmp_sum += rep[2]
        if grand_total * 0.95 > tmp_sum > grand_total * 0.8:
            start_letter = 'B'
        elif grand_total * 0.95 < tmp_sum:
            start_letter = 'C'
        if rep[3] == 'A':
            report_total_a[1] = list(map(lambda x: (x[0][0] + x[1][0], 0, 0), list(zip(rep[1], report_total_a[1]))))
            report_total_a[2] += rep[2]
            report_a.append(rep)
        elif rep[3] == 'B':
            report_total_b[1] = list(map(lambda x: (x[0][0] + x[1][0], 0, 0), list(zip(rep[1], report_total_b[1]))))
            report_total_b[2] += rep[2]
            report_b.append(rep)
        elif rep[3] == 'C':
            report_total_c[1] = list(map(lambda x: (x[0][0] + x[1][0], 0, 0), list(zip(rep[1], report_total_c[1]))))
            report_total_c[2] += rep[2]
            report_c.append(rep)
    report_total_a.append('A')
    report_total_b.append('B')
    report_total_c.append('C')
    report.append(report_total_a)
    report.append(report_total_b)
    report.append(report_total_c)


def abc_out_lists(customers_period, report, eco):
    r_eco = []
    for letter in ['A', 'B', 'C']:
        tmp = GroupMarketingFigures(letter, eco)
        tmp.set_figures(customers_period, report)
        r_eco.append(tmp)
    r_sum = sum_abc(r_eco)
    r_eco.append(r_sum)
    return out_client_table(r_eco)


def out_client_table(r):
    a, b, c, abc = r[0], r[1], r[2], r[3]
    abc_out = []
    i = -1
    for y in a.__dict__:
        i += 1
        abc_out.append([a.russian_name(y)])
        for x in [a, b, c, abc]:
            element = getattr(x, y)
            if not isinstance(element, str) and y != 'sales_per_client':
                element = f'{int(element):,}'
            elif y == 'sales_per_client':
                element = str(round(element, 2))
            abc_out[i].append(element)
    del abc_out[1]
    return abc_out



