import datetime
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.db.models import Q
from salesreport.views.service import *
from salesreport.report_period import ReportPeriod
from maket.models import Customer_types

region_code = {
    '01': 'Адыгея республика',
    '02': 'Башкортостан республика',
    '03': 'Бурятия республика',
    '04': 'Алтай республика',
    '05': 'Дагестан республика',
    '06': 'Ингушетия республика',
    '07': 'Кабардино-Балкарская республика',
    '08': 'Калмыкия республика',
    '09': 'Карачаево-Черкесская республика',
    '10': 'Карелия республика',
    '11': 'Коми республика',
    '12': 'Марий Эл республика',
    '13': 'Мордовия республика',
    '14': 'Саха /Якутия/ республика',
    '15': 'Северная Осетия - Алания республика',
    '16': 'Татарстан республика',
    '17': 'Тыва республика',
    '18': 'Удмуртская республика',
    '19': 'Хакасия республика',
    '20': 'Чеченская республика',
    '21': 'Чувашская Республика - Чувашия',
    '22': 'Алтайский край',
    '23': 'Краснодарский край',
    '24': 'Красноярский край',
    '25': 'Приморский край',
    '26': 'Ставропольский край',
    '27': 'Хабаровский край',
    '28': 'Амурская область',
    '29': 'Архангельская область',
    '30': 'Астраханская область',
    '31': 'Белгородская область',
    '32': 'Брянская область',
    '33': 'Владимирская область',
    '34': 'Волгоградская область',
    '35': 'Вологодская область',
    '36': 'Воронежская область',
    '37': 'Ивановская область',
    '38': 'Иркутская область',
    '39': 'Калининградская область',
    '40': 'Калужская область',
    '41': 'Камчатский край',
    '42': 'Кемеровская область',
    '43': 'Кировская область',
    '44': 'Костромская область',
    '45': 'Курганская область',
    '46': 'Курская область',
    '47': 'Ленинградская область',
    '48': 'Липецкая область',
    '49': 'Магаданская область',
    '50': 'Московская область',
    '51': 'Мурманская область',
    '52': 'Нижегородская область',
    '53': 'Новгородская область',
    '54': 'Новосибирская область',
    '55': 'Омская область',
    '56': 'Оренбургская область',
    '57': 'Орловская область',
    '58': 'Пензенская область',
    '59': 'Пермский край',
    '60': 'Псковская область',
    '61': 'Ростовская область',
    '62': 'Рязанская область',
    '63': 'Самарская область',
    '64': 'Саратовская область',
    '65': 'Сахалинская область',
    '66': 'Свердловская область',
    '67': 'Смоленская область',
    '68': 'Тамбовская область',
    '69': 'Тверская область',
    '70': 'Томская область',
    '71': 'Тульская область',
    '72': 'Тюменская область',
    '73': 'Ульяновская область',
    '74': 'Челябинская область',
    '75': 'Забайкальский край',
    '76': 'Ярославская область',
    '77': 'Москва город',
    '78': 'Санкт-Петербург город',
    '79': 'Еврейская автономная область',
    '83': 'Ненецкий автономный округ',
    '86': 'Ханты-Мансийский Автономный округ - Югра автономный округ',
    '87': 'Чукотский автономный округ',
    '89': 'Ямало-Ненецкий автономный округ',
    '91': 'Крым республика',
    '92': 'Севастополь город',
    '99': 'Байконур город'
}


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
    grand_total_eco = sum(customers_period.values_list(report_type_eco, flat=True))
    grand_total_no_eco = sum(customers_period.values_list(report_type_no_eco, flat=True))
    report_eco, report_no_eco = [], []
    customers_types = Customer_types.objects.all().order_by('-group_discount')
    for type in customers_types:
        customers_periods = Class.objects.filter(Q(period__in=periods) & (
                Q(group__isnull=True) & Q(customer__customer_type=type) | Q(group__group_type=type)))
        total_amount_eco = sum(list(customers_periods.values_list(report_type_eco, flat=True)))
        total_amount_no_eco = sum(list(customers_periods.values_list(report_type_no_eco, flat=True)))
        list_eco_type, list_no_eco_type, list_eco_region, list_no_eco_region = [], [], [], []
        for period in periods:
            cst_periods_tmp = customers_periods.filter(period=period)
            list_eco_type.append([sum(cst_periods_tmp.values_list(report_type_eco, flat=True)), period.id])
            list_no_eco_type.append([sum(cst_periods_tmp.values_list(report_type_no_eco, flat=True)), period.id])
            '''
            region_iter = filter(lambda x: x in cst_periods_tmp.values_list('customer__region', flat=True), region_code.keys())
            for region in region_iter:
                cst_region_tmp = cst_periods_tmp.filter(customer__region=region)
                list_eco_region.append([sum(cst_region_tmp.values_list(report_type_eco, flat=True)), period.id, region])
                list_no_eco_region.append([sum(cst_region_tmp.values_list(report_type_no_eco, flat=True)), period.id, region])
            '''
        if total_amount_no_eco:
            report_no_eco.append([type.type_name, list_no_eco_type, total_amount_no_eco])
        #                [type.type_name, list(customers_periods.filter(~Q(**{report_type_no_eco: 0})).values_list(report_type_no_eco, 'period')),
        #                 total_amount_no_eco])
        if total_amount_eco:
            report_eco.append([type.type_name, list_eco_type, total_amount_eco])
    #            report_eco.append(
    #                [type.type_name, list(customers_periods.filter(~Q(**{report_type_eco: 0})).values_list(report_type_eco, 'period')), total_amount_eco])

    context = {'navi': navi, 'report_type': report_type, 'date_begin': date_start, 'report_eco': report_eco,
               'report_no_eco': report_no_eco, 'grand_total_no_eco': grand_total_no_eco,
               'grand_total_eco': grand_total_eco, 'date_end': date_finish, 'per_type': period_type,
               'period_types': period_types, 'periods': periods}
    return render(request, 'salesreport/reports/customer_geography.html', context)
