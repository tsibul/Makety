import datetime
from datetime import date
from functools import partial
from salesreport.reports import *
from django.shortcuts import render, HttpResponseRedirect, reverse
from salesreport.views.service import *
from salesreport.report_period import ReportPeriod


class GroupMarketingFigures:

    def __init__(self, *args):
        if len(args) == 10:
            self.abc_group = args[0]
            self.eco_group = args[1]
            self.quantity = args[2]
            self.sales = args[3]
            self.profit = args[4]
            self.no_sales = args[5]
            self.average_check = args[6]
            self.average_profit_per_client = args[7]
            self.average_sales_per_client = args[8]
            self.sales_per_client = args[9]
        elif len(args) == 2:
            self.abc_group = args[0]
            self.eco_group = args[1]
            self.quantity = 0
            self.sales = 0
            self.profit = 0
            self.no_sales = 0
            self.average_check = 0
            self.average_profit_per_client = 0
            self.average_sales_per_client = 0
            self.sales_per_client = 0
        else:
            raise TypeError("wrong number of args")

    def russian_name(self, name):
        translate_args = {'abc_group': 'Группа',
                          'eco_group': 'Эко',
                          'quantity': 'Кол-во клиентов',
                          'sales': 'Продажи',
                          'profit': 'Прибыль',
                          'no_sales': 'Кол-во продаж',
                          'average_check': 'Средний чек',
                          'average_profit_per_client': 'Прибыль на клиента',
                          'average_sales_per_client': 'Продажи на клиента',
                          'sales_per_client': 'Кол-во продаж на клиента'
                          }
        return translate_args[name]

    def set_figures(self, customers_periods, report):
        map_obj = map(lambda x: x[0] if x[3] == self.abc_group else '', report)
        customers_periods = customers_periods.filter(name__in=map_obj)
        self.quantity = sum(map(lambda x: x[3] == self.abc_group, report)) - 1
        self.sales = sum(customers_periods.values_list('sales_with_vat_' + self.eco_group, flat=True))
        self.profit = sum(customers_periods.values_list('profit_' + self.eco_group, flat=True))
        self.no_sales = sum(customers_periods.values_list('no_sales_' + self.eco_group, flat=True))
        self.average_check = self.sales / self.no_sales
        self.average_profit_per_client = self.profit / self.quantity
        self.average_sales_per_client = self.sales / self.quantity
        self.sales_per_client = self.no_sales / self.quantity


def sum_abc(a: GroupMarketingFigures, b: GroupMarketingFigures, c: GroupMarketingFigures):
    abc_group = 'A+B+C'
    eco_group = a.eco_group
    quantity = a.quantity + b.quantity + c.quantity
    sales = a.sales + b.sales + c.sales
    profit = a.profit + b.profit + c.profit
    no_sales = a.no_sales + b.no_sales + c.no_sales
    average_check = sales / no_sales
    average_profit_per_client = profit / quantity
    average_sales_per_client = sales / quantity
    sales_per_client = no_sales / quantity
    return GroupMarketingFigures(abc_group, eco_group, quantity, sales, profit, no_sales, average_check,
                                 average_profit_per_client, average_sales_per_client, sales_per_client)


def report_customer_period(request):
    print(datetime.datetime.now().time())
    navi = 'ABC-Клиенты'
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
    names = set(customers_period.values_list('name', flat=True))
    grand_total_eco = sum(customers_period.values_list(report_type_eco, flat=True))
    grand_total_no_eco = sum(customers_period.values_list(report_type_no_eco, flat=True))
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
    abc_check(report_eco, grand_total_eco)
    abc_check(report_no_eco, grand_total_no_eco)

    a_eco = GroupMarketingFigures('A', 'eco')
    a_eco.set_figures(customers_period, report_eco)
    b_eco = GroupMarketingFigures('B', 'eco')
    b_eco.set_figures(customers_period, report_eco)
    c_eco = GroupMarketingFigures('C', 'eco')
    c_eco.set_figures(customers_period, report_eco)
    abc_total_eco = sum_abc(a_eco, b_eco, c_eco)
    abc_eco = out_client_table(a_eco, b_eco, c_eco, abc_total_eco)

    a_no_eco = GroupMarketingFigures('A', 'no_eco')
    a_no_eco.set_figures(customers_period, report_no_eco)
    b_no_eco = GroupMarketingFigures('B', 'no_eco')
    b_no_eco.set_figures(customers_period, report_no_eco)
    c_no_eco = GroupMarketingFigures('C', 'no_eco')
    c_no_eco.set_figures(customers_period, report_no_eco)
    abc_total_no_eco = sum_abc(a_no_eco, b_no_eco, c_no_eco)
    abc_no_eco = out_client_table(a_no_eco, b_no_eco, c_no_eco, abc_total_no_eco)

    print(datetime.datetime.now().time())
    context = {'navi': navi, 'report_eco': report_eco, 'report_no_eco': report_no_eco, 'periods': periods,
               'period_types': period_types, 'report_type': report_type, 'date_begin': date_start,
               'date_end': date_finish, 'per_type': period_type, 'grand_total_eco': grand_total_eco,
               'grand_total_no_eco': grand_total_no_eco, 'abc_eco': abc_eco, 'abc_no_eco': abc_no_eco}
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
    report_total_a = ['Клиенты "A"', number_of_periods, 0]
    report_total_b = ['Клиенты "B"', number_of_periods, 0]
    report_total_c = ['Клиенты "C"', number_of_periods, 0]
    report_a = []
    report_b = []
    report_c = []
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


def out_client_table(a, b, c, abc):
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
