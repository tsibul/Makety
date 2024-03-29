import datetime
from datetime import date, datetime, timedelta
import os

from django.shortcuts import render, HttpResponseRedirect, reverse
from salesreport.models import Sales_doc_imports, Sales_docs, CustomerPeriodsYear, CustomerPeriodsQuarter, \
    CustomerPeriodsMonth, CustomerPeriodsWeek
from django.core.files.storage import default_storage
from django.db.models import Q, F
from salesreport.views.service import *
from salesreport.reports import ReportPeriod


def management(request):
    navi = 'Управление'
    try:
        date_last = max(Sales_doc_imports.objects.values_list('import_date', flat=True))
    except:
        date_last = datetime(2000, 1, 1).date()
    try:
        date_last_cst = max(Customer_all.objects.values_list('date_import', flat=True))
    except:
        date_last_cst = datetime(2000, 1, 1).date()
    customers_all_quantity = Customer_all.objects.all().count()
    customers_active_quantity = Customer_all.objects.filter(active=True, internal=False).count()
    no_inn = Customer_all.objects.filter(Q(active=True) & Q(internal=False) & (Q(inn='') | Q(inn__isnull=True))).count()

    groups_active_quantity = Customer_groups.objects.filter(active=True).count()
    groups_quantity = Customer_groups.objects.all().count()

    clients_active_quantity = Customer_all.objects.filter(active=True, internal=False,
                                                          customer_group__isnull=True).count() + \
                              Customer_groups.objects.filter(active=True).count()
    clients_quantity = Customer_all.objects.filter(customer_group__isnull=True).count() + \
                       Customer_groups.objects.all().count()

    sales_doc_quantity = Sales_docs.objects.all().count()
    transactions_quantity = Sales_doc_imports.objects.all().count()
    no_doc = Sales_doc_imports.objects.filter(sales_doc__isnull=True).count()
    no_cust = Sales_docs.objects.filter(customer__isnull=True).count()
    no_good = Sales_doc_imports.objects.filter(detail_set__isnull=True).count()
    sinhronized = Customer.objects.filter(~(Q(customer_all__isnull=False) &
                                            (Q(customer_group=F('customer_all__customer_group')) |
                                             Q(customer_group__isnull=True) & Q(
                                                        customer_all__customer_group__isnull=True)) &
                                            (Q(customer_type=F('customer_all__customer_type')) |
                                             Q(customer_type__isnull=True) & Q(
                                                        customer_all__customer_type__isnull=True)) &
                                            Q(inn=F('customer_all__inn')) &
                                            Q(name__endswith=F('customer_all__name'))
                                            )).count()
    date_now = datetime.today().date()
    context = {'navi': navi, 'date_last_cst': date_last_cst,
               'customers_active_quantity': customers_active_quantity, 'sinhronized': sinhronized,
               'date_last': date_last, 'sales_doc_quantity': sales_doc_quantity,
               'customers_all_quantity': customers_all_quantity,
               'transactions_quantity': transactions_quantity, 'no_doc': no_doc, 'no_cust': no_cust, 'no_good': no_good,
               'groups_quantity': groups_quantity, 'groups_active_quantity': groups_active_quantity,
               'clients_quantity': clients_quantity, 'clients_active_quantity': clients_active_quantity,
               'date_now': date_now, 'no_inn': no_inn}
    return render(request, 'salesreport/management.html', context)


def import_report(request):
    report_file = request.FILES['importReport']
    start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
    Sales_doc_imports.objects.filter(sales_doc_date__gte=start_date).delete()
    try:
        Sales_docs.objects.filter(sales_doc_date__gte=start_date).delete()
    except:
        pass
    try:
        os.remove('report_file')
    except:
        pass
    file_name = default_storage.save('report_file', report_file)

    with open(file_name, newline='', encoding='utf-8') as cust_csv:
        records_list = []
        customer_list = []
        for line in enumerate(cust_csv, 1):
            row = line[1].rstrip('\r\n').split(';')
            sales_doc_date = datetime.strptime(row[13], '%d.%m.%Y').strftime("%Y-%m-%d")
            sales_doc_date = datetime.strptime(sales_doc_date, '%Y-%m-%d').date()
            if sales_doc_date < start_date:
                continue
            import_date = datetime.today().date()
            code_imp = row[0]
            code_list = code_imp.split('.')
            code = code_list[0]
            code_list.pop(0)
            if len(code_list) >= 1 and len(code_list[0]) > 1:
                main_color = code_list[0]
                color_code = '.'.join(code_list)
            elif len(code_list) > 1 and len(code_list[0]) == 1:
                main_color = code_list[1]
                color_code = '.'.join(code_list)
            elif len(code_list) == 1 and len(code_list[0]) == 1:
                main_color = None
                color_code = code_list[1]
            else:
                main_color = None
                color_code = None
            try:
                detail_set = Detail_set.objects.get(item_name=code)
            except:
                detail_set = None
            try:
                item_color = Item_color.objects.get(color_id=main_color, color_scheme=detail_set.color_scheme)
            except:
                item_color = None
            series_id = row[1]
            good_id = row[2]
            good_group_id = row[3]
            good_group = row[4]
            good_title = row[5]
            good_name = row[6]
            code_1 = row[9]
            quantity = float(row[10].replace(',', '.'))
            sales_doc_name = row[11]
            sales_doc_no = row[12]
            buy_without_vat = float(row[14].replace(',', '.'))
            buy_with_vat = float(row[15].replace(',', '.'))
            sales_quantity = float(row[17].replace(',', '.'))
            sale_without_vat = float(row[16].replace(',', '.'))
            sale_with_vat = float(row[18].replace(',', '.'))
            sale_price_vat = float(row[19].replace(',', '.'))
            customer_name = row[21]
            customer_frigat_id = row[20]
            try:
                customer_all = Customer_all.objects.get(frigat_id=customer_frigat_id)
            except:
                customer_all = Customer_all(frigat_id=customer_frigat_id, date_first=datetime(2000, 1, 1).date(),
                                            date_last=datetime(2000, 1, 1).date(), name=customer_name)
            if sales_doc_date < customer_all.date_first or customer_all.date_first == datetime(2000, 1, 1).date():
                customer_all.date_first = sales_doc_date
                customer_all.save()
            if sales_doc_date > customer_all.date_last:
                customer_all.date_last = sales_doc_date
                customer_all.save()
            report_record = Sales_doc_imports(import_date=import_date, code=code, detail_set=detail_set,
                                              color_code=color_code, main_color=main_color, item_color=item_color,
                                              series_id=series_id, good_id=good_id, good_group_id=good_group_id,
                                              good_group=good_group, good_title=good_title, good_name=good_name,
                                              code_1=code_1, quantity=quantity, sales_doc_name=sales_doc_name,
                                              sales_doc_no=sales_doc_no, sales_doc_date=sales_doc_date,
                                              buy_without_vat=buy_without_vat, buy_with_vat=buy_with_vat,
                                              sales_quantity=sales_quantity, sale_without_vat=sale_without_vat,
                                              sale_with_vat=sale_with_vat, sale_price_vat=sale_price_vat,
                                              customer_name=customer_name, customer_all=customer_all)
            records_list.append(report_record)
            customer_list.append(customer_all)
        tmp_records = filter(lambda x: x.customer_all == None, records_list)
        new_records = Sales_doc_imports.objects.bulk_create(records_list)
    #        new_customers = Customer.objects.bulk_update(customer_list, ['frigat_id', 'date_first', 'name', 'date_last'])
    return HttpResponseRedirect(reverse('salesreport:management'))


def sales_docs(request):
    sls_docs()
    return HttpResponseRedirect(reverse('salesreport:management'))


def import_cst(request):
    cust_file = request.FILES['cust']
    try:
        os.remove('cust_file')
    except:
        pass
    file_name = default_storage.save('cust_file', cust_file)

    with open(file_name, newline='', encoding='utf-8') as cust_csv:
        #        tmp_lst = []
        for line in enumerate(cust_csv, 1):
            row = line[1].rstrip('\r\n').split(';')
            fr_id = row[0]
            if not customer_check_row(row):
                #                tmp_lst.append(line)
                #                tmp_lst.append(row)
                continue
            try:
                customer = Customer_all.objects.get(frigat_id=fr_id)
                if customer_import_compare(row, customer):
                    continue
            except:
                customer = Customer_all(frigat_id=fr_id, date_import=datetime.today().date())
            customer.name = row[1]
            customer.form = row[2]
            inn = row[3]
            if len(inn) == 9 or len(inn) == 11:
                inn = '0' + str(inn)
            customer.inn = inn
            try:
                customer.region = row[3][0:2]
            except:
                customer.region = ''
            customer.address = row[5]
            customer.phone = row[6]
            customer.mail = row[7]
            customer.comment = row[8]
            customer.our_manager = row[10]
            type_tmp = row[11]
            customer.all_mails = row[12]
            customer.all_phones = row[13]
            try:
                customer.customer_type = customer_type_chose(type_tmp, customer.region)
            except:
                pass
            customer.save()
            if customer.inn != '':
                try:
                    customer_maket = Customer.objects.get(inn=customer.inn)
                    customer_maket.customer_all = customer
                    customer_maket.save()
                except:
                    pass
            else:
                #                tmp_lst.append(line)
                #                tmp_lst.append(row)
                try:
                    customer_maket = Customer.objects.get(Q(name__endswith=customer.name))
                    customer_maket.customer_all = customer
                    customer_maket.save()
                except:
                    pass
    return HttpResponseRedirect(reverse('salesreport:management'))


def cst_sinhro_group(request):
    customers = Customer.objects.filter((~Q(customer_group=F('customer_all__customer_group')) |
                                         ~Q(customer_type=F('customer_all__customer_type')) |
                                         ~Q(region=F('customer_all__region'))) & Q(customer_all__isnull=False))
    for customer in customers:
        customer_all = customer.customer_all
        customer.customer_group = customer_all.customer_group
        if customer.customer_type:
            customer_all.customer_type = customer.customer_type
            customer_all.save()
        elif customer_all.customer_type:
            customer.customer_type = customer_all.customer_type
        customer.region = customer_all.region
        customer.save()
    return HttpResponseRedirect(reverse('salesreport:management'))


def cst_set_inactive(request):
    no_weeks = int(request.POST['weeks'])
    d_n = datetime.today().date() - timedelta(weeks=no_weeks)
    customers_list = Customer_all.objects.all()
    for cst in customers_list:
        if cst.date_last < d_n:
            cst.active = False
        else:
            cst.active = True
    Customer_all.objects.bulk_update(customers_list, ['active'])
    return HttpResponseRedirect(reverse('salesreport:management'))


def set_frigat_id(request):
    transations = Sales_doc_imports.objects.filter(customer_frigat_id__isnull=True)

    for transation in transations:
        transation.customer_frigat_id = transation.customer_all.frigat_id
    Sales_doc_imports.objects.bulk_update(transations, ['customer_frigat_id'])
    return HttpResponseRedirect(reverse('salesreport:management'))


def group_set_inactive(request):
    weeks_no = int(request.POST['group_weeks'])
    d_n = datetime.today().date() - timedelta(weeks=weeks_no)
    groups_list = Customer_groups.objects.all()
    #    map(lambda x: x.active = False, groups_list)
    for grp in groups_list:
        if grp.date_last < d_n:
            grp.active = False
        else:
            grp.active = True
    Customer_groups.objects.bulk_update(groups_list, ['active'])
    return HttpResponseRedirect(reverse('salesreport:management'))


def group_set_dates(request):
    groups_list = Customer_groups.objects.all()
    for grp in groups_list:
        try:
            date_first = min(Customer_all.objects.filter(customer_group=grp).values_list('date_first', flat=True))
        except:
            date_first = datetime(2000, 1, 1).date()
        try:
            date_last = max(Customer_all.objects.filter(customer_group=grp).values_list('date_last', flat=True))
        except:
            date_last = datetime(2000, 1, 1).date()
        grp.date_first = date_first
        grp.date_last = date_last
    Customer_groups.objects.bulk_update(groups_list, ['date_first', 'date_last'])
    return HttpResponseRedirect(reverse('salesreport:management'))


def lost_goods(request):
    sales = Sales_doc_imports.objects.filter(detail_set__isnull=True).order_by('sales_doc_date')
    context = {'sales': sales}
    return render(request, 'salesreport/lost_goods.html', context)


def sales_docs_recheck(request):
    date_from = request.POST['date']
    Sales_docs.objects.filter(sales_doc_date__gte=date_from).delete()
    sls_docs()
    return HttpResponseRedirect(reverse('salesreport:management'))


def sls_docs():
    sales_docs = set(Sales_doc_imports.objects.filter(sales_doc__isnull=True).values_list('sales_doc_name',
                                                                                          'sales_doc_no',
                                                                                          'sales_doc_date',
                                                                                          'customer_all'))
    for sales_doc in sales_docs:
        try:
            sales_object = Sales_docs.objects.get(sales_document=sales_doc[0], sales_doc_number=sales_doc[1],
                                                  sales_doc_date=sales_doc[2],
                                                  customer=Customer_all.objects.get(id=sales_doc[3]))
            continue
        except:
            sales_object = Sales_docs(sales_document=sales_doc[0], sales_doc_number=sales_doc[1],
                                      sales_doc_date=sales_doc[2], customer=Customer_all.objects.get(id=sales_doc[3]))
            sales_object.save()
            sales_docs_imports = Sales_doc_imports.objects.filter(sales_doc_name=sales_doc[0],
                                                                  sales_doc_no=sales_doc[1],
                                                                  sales_doc_date=sales_doc[2],
                                                                  customer_all__id=sales_doc[3])
            eco = 0
            for row in sales_docs_imports:
                row.sales_doc = sales_object
                sales_object.total_sale_with_vat += row.sale_with_vat
                sales_object.total_sale_without_vat += row.sale_without_vat
                sales_object.total_buy_with_vat += row.buy_with_vat
                sales_object.total_buy_without_vat += row.buy_without_vat
                sales_object.quantity += row.quantity
                if row.detail_set is not None and row.detail_set.eco:
                    eco += row.sale_without_vat
                if not row.detail_set:
                    sales_object.good_no_error = False
                row.save()
            sales_object.eco = eco >= sales_object.total_sale_without_vat / 2
            sales_object.save()


def report_periods(request):
    begin_period = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
    end_period = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
    try:
        del_periods = ReportPeriod.objects.filter(date_end__gte=begin_period, date_begin__lte=end_period)
        del_periods.delete()
    except:
        pass
    per = ReportPeriod()
    for period_type in per.calculatableList():
        per.setPeriod(begin_period, period_type)
        while per.date_begin < end_period:
            per.copy().save()
            per.plus(1)
    return HttpResponseRedirect(reverse('salesreport:management'))


def sales_set_periods(request):
    begin_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    sales_documents = Sales_docs.objects.filter(sales_doc_date__gte=begin_date)
    for doc in sales_documents:
        doc.set_periods()
        doc.save()
    return HttpResponseRedirect(reverse('salesreport:management'))


def transactions_set_periods(request):
    begin_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    sales_documents = Sales_doc_imports.objects.filter(sales_doc_date__gte=begin_date)
    for doc in sales_documents:
        doc.set_periods()
        doc.save()
    return HttpResponseRedirect(reverse('salesreport:management'))


def customer_period_sales(request):
    begin_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    period_type = request.POST['period']
    Class = check_class(period_type)
    try:
        items_to_delete = Class.objects.filter(period__date_end__gte=begin_date)
        items_to_delete.delete()
    except:
        pass
    periods = ReportPeriod.objects.filter(period=period_type, date_end__gte=begin_date)
    customer_periods_list = []
    groups = set(Customer_all.objects.filter(date_last__gte=begin_date, customer_group__isnull=False).values_list(
        'customer_group', flat=True))
    for i in groups:
        for period in periods:
            group = Customer_groups.objects.get(id=i)
            customer = Customer_all.objects.filter(customer_group=group, date_last__gte=begin_date).last()
            customer_regular = Class(group=group, period=period, name=group.group_name, customer=customer)
            sales_documents = sales_doc_request_for_period_group(group, period)
            customer_regular.set_sales_data(sales_documents)
            customer_periods_list.append(customer_regular)
    customers = Customer_all.objects.filter(date_last__gte=begin_date, customer_group__isnull=True, internal=False)
    for customer in customers:
        for period in periods:
            customer_regular = Class(customer=customer, period=period, name=customer.name.replace('"', ''))
            sales_documents = sales_doc_request_for_period_customer(customer, period)
            customer_regular.set_sales_data(sales_documents)
            customer_periods_list.append(customer_regular)
    Class.objects.bulk_create(customer_periods_list, batch_size=3000)
    return HttpResponseRedirect(reverse('salesreport:management'))


def sales_doc_request_for_period_group(group, period: ReportPeriod):
    if period.period == 'WK':
        return Sales_docs.objects.filter(customer__customer_group=group, week=period).exclude(
            sales_doc_number__startswith='О')
    elif period.period == 'MT':
        return Sales_docs.objects.filter(customer__customer_group=group, month=period).exclude(
            sales_doc_number__startswith='О')
    elif period.period == 'QT':
        return Sales_docs.objects.filter(customer__customer_group=group, quarter=period).exclude(
            sales_doc_number__startswith='О')
    else:
        return Sales_docs.objects.filter(customer__customer_group=group, year=period).exclude(
            sales_doc_number__startswith='О')


def sales_doc_request_for_period_customer(customer, period: ReportPeriod):
    if period.period == 'WK':
        return Sales_docs.objects.filter(customer=customer, week=period).exclude(
            sales_doc_number__startswith='О')
    elif period.period == 'MT':
        return Sales_docs.objects.filter(customer=customer, month=period).exclude(
            sales_doc_number__startswith='О')
    elif period.period == 'QT':
        return Sales_docs.objects.filter(customer=customer, quarter=period).exclude(
            sales_doc_number__startswith='О')
    else:
        return Sales_docs.objects.filter(customer=customer, year=period).exclude(
            sales_doc_number__startswith='О')


def region_97(request):
    customers_97 = Customer_all.objects.filter(region='97')
    customers_00 = Customer_all.objects.filter(Q(region='') | Q(region='0'))
    customers_97.update(region='77')
    customers_00.update(region='00')
    return HttpResponseRedirect(reverse('salesreport:management'))


def goods_period_sales(request):
    begin_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
    period_type = request.POST['period']
    Class = check_goods_class(period_type)
    try:
        items_to_delete = Class.objects.filter(period__date_end__gte=begin_date)
        items_to_delete.delete()
    except:
        pass
    periods = ReportPeriod.objects.filter(period=period_type, date_end__gte=begin_date)
    goods_periods_list = []
    goods = Detail_set.objects.all()
    for good in goods:
        colors = Item_color.objects.filter(color_scheme=good.color_scheme)
        for period in periods:
            good_regular = Class(good=good, period=period)
            sales_imports = sales_request_for_period_goods_no_color(good, period)
            good_regular.set_goods_data(sales_imports)
            goods_periods_list.append(good_regular)
            for color in colors:
                good_regular = Class(good=good, period=period, main_color=color)
                sales_imports = sales_request_for_period_goods(good, period, color)
                good_regular.set_goods_data(sales_imports)
                goods_periods_list.append(good_regular)

    Class.objects.bulk_create(goods_periods_list, batch_size=3000)
    return HttpResponseRedirect(reverse('salesreport:management'))


def sales_request_for_period_goods(good, period: ReportPeriod, color):
    if period.period == 'WK':
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__week=period, item_color=color,
                                                customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')
    elif period.period == 'MT':
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__month=period, item_color=color,
                                                customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')
    elif period.period == 'QT':
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__quarter=period, item_color=color,
                                                customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')
    else:
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__year=period, item_color=color,
                                                customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')


def sales_request_for_period_goods_no_color(good, period: ReportPeriod):
    if period.period == 'WK':
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__week=period,
                                                item_color__isnull=True, customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')
    elif period.period == 'MT':
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__month=period,
                                                item_color__isnull=True, customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')
    elif period.period == 'QT':
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__quarter=period,
                                                item_color__isnull=True, customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')
    else:
        return Sales_doc_imports.objects.filter(detail_set=good, sales_doc__year=period,
                                                item_color__isnull=True, customer_all__internal=False).exclude(
            sales_doc_no__startswith='О')
