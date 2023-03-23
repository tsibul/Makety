import datetime
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.db.models import Q
from salesreport.views.service import *
from salesreport.report_period import ReportPeriod
from maket.models import Good_crm_type, Good_matrix_type
from salesreport.models import Sales_doc_imports


def report_goods_group(request):
    navi = 'Группы товаров'
    period_types = ReportPeriod.calculatableList()
    report_type = request.POST['report_type']
    date_start = datetime.datetime.strptime(request.POST['date_begin'], '%Y-%m-%d').date()
    date_finish = datetime.datetime.strptime(request.POST['date_end'], '%Y-%m-%d').date()
    period_type = request.POST['period_type']
    periods = ReportPeriod.objects.filter(period=period_type, date_end__gte=date_start,
                                          date_begin__lte=date_finish).order_by('date_begin')
    Class = check_goods_class(period_type)

    goods_period = Class.objects.filter(period__in=periods)

    grand_total = sum(goods_period.values_list(report_type, flat=True))
    report = []

    goods_groups = Good_crm_type.objects.all()
    for group in goods_groups:
        goods_periods = Class.objects.filter(period__in=periods, good__crm=group)
        total_amount = sum(list(goods_periods.values_list(report_type, flat=True)))
        list_group = []
        for period in periods:
            grp_periods_tmp = goods_periods.filter(period=period)
            list_group.append([sum(grp_periods_tmp.values_list(report_type, flat=True)), period.id])
        report.append([group.crm_name, list_group, total_amount, group.id])

    context = {'navi': navi, 'report_type': report_type, 'date_begin': date_start, 'report': report,
               'grand_total': grand_total, 'date_end': date_finish, 'per_type': period_type,
               'period_types': period_types, 'periods': periods}
    return render(request, 'salesreport/reports/goods_group_type.html', context)


def report_goods_type(request):
    navi = 'Типы товаров'
    period_types = ReportPeriod.calculatableList()
    report_type = request.POST['report_type']
    date_start = datetime.datetime.strptime(request.POST['date_begin'], '%Y-%m-%d').date()
    date_finish = datetime.datetime.strptime(request.POST['date_end'], '%Y-%m-%d').date()
    period_type = request.POST['period_type']
    periods = ReportPeriod.objects.filter(period=period_type, date_end__gte=date_start,
                                          date_begin__lte=date_finish).order_by('date_begin')
    Class = check_goods_class(period_type)

    goods_period = Class.objects.filter(period__in=periods)

    grand_total = sum(goods_period.values_list(report_type, flat=True))
    report = []

    goods_groups = Good_matrix_type.objects.all()
    for group in goods_groups:
        goods_periods = Class.objects.filter(period__in=periods, good__matrix=group)
        total_amount = sum(list(goods_periods.values_list(report_type, flat=True)))
        list_group = []
        for period in periods:
            grp_periods_tmp = goods_periods.filter(period=period)
            list_group.append([sum(grp_periods_tmp.values_list(report_type, flat=True)), period.id])
        report.append([group.matrix_name, list_group, total_amount, group.id])

    context = {'navi': navi, 'report_type': report_type, 'date_begin': date_start, 'report': report,
               'grand_total': grand_total, 'date_end': date_finish, 'per_type': period_type,
               'period_types': period_types, 'periods': periods}
    return render(request, 'salesreport/reports/goods_group_type.html', context)
