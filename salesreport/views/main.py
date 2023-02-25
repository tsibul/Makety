import datetime
from datetime import date
import os

from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from salesreport.models import Sales_doc_imports, Sales_docs
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.db.models import Q, F
from salesreport.views.service import *


def index(request):
    navi = 'Главная'
    try:
        date_last = max(Sales_doc_imports.objects.values_list('import_date', flat=True))
    except:
        date_last = '2000-01-01'
    try:
        date_last_cst = max(Customer_all.objects.values_list('date_import', flat=True))
    except:
        date_last_cst = '2010-01-01'
    customers_all_quantity = Customer_all.objects.all().count()
    customers_active_quantity = Customer_all.objects.filter(active=True, internal=False).count()

    groups_active_quantity = Customer_groups.objects.filter(active=True).count()
    groups_quantity = Customer_groups.objects.all().count()

    clients_active_quantity = Customer_all.objects.filter(active=True, internal=False, customer_group__isnull=True).count() + \
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
                                          Q(customer_group__isnull=True) & Q(customer_all__customer_group__isnull=True)) &
                                          (Q(customer_type=F('customer_all__customer_type')) |
                                          Q(customer_type__isnull=True) & Q(customer_all__customer_type__isnull=True)) &
                                          Q(inn=F('customer_all__inn')) &
                                          Q(name__endswith=F('customer_all__name'))
                                          )).count()
    context = {'navi': navi, 'date_last_cst': date_last_cst,
               'customers_active_quantity': customers_active_quantity, 'sinhronized': sinhronized,
               'date_last': date_last, 'sales_doc_quantity': sales_doc_quantity, 'customers_all_quantity': customers_all_quantity,
               'transactions_quantity': transactions_quantity, 'no_doc': no_doc, 'no_cust': no_cust, 'no_good': no_good,
               'groups_quantity': groups_quantity, 'groups_active_quantity': groups_active_quantity,
               'clients_quantity': clients_quantity, 'clients_active_quantity': clients_active_quantity}
    return render(request, 'salesreport/index.html', context)


def import_report(request):
    report_file = request.FILES['importReport']
    start_date = datetime.datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
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
            sales_doc_date = datetime.datetime.strptime(row[13], '%d.%m.%Y').strftime("%Y-%m-%d")
            sales_doc_date = datetime.datetime.strptime(sales_doc_date, '%Y-%m-%d').date()
            if sales_doc_date < start_date:
                continue
            import_date = date.today()
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
                customer_all = Customer_all(frigat_id=customer_frigat_id, date_first=datetime.date(2000, 1, 1),
                                    date_last=datetime.date(2000, 1, 1), name=customer_name)
            if customer_all.date_first == datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date() \
                    or sales_doc_date < customer_all.date_first:
                customer_all.date_first = sales_doc_date
            if customer_all.date_last == datetime.datetime.strptime('2100-01-01', '%Y-%m-%d').date() \
                    or sales_doc_date > datetime.datetime.strptime(str(customer_all.date_last), '%Y-%m-%d').date():
                customer_all.date_last = sales_doc_date
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
        new_records = Sales_doc_imports.objects.bulk_create(records_list)
        new_customers = Customer.objects.bulk_update(customer_list, ['frigat_id', 'date_first', 'name', 'date_last'])
    return HttpResponseRedirect(reverse('salesreport:index'))


def sales_docs(request):
    sales_docs = set(Sales_doc_imports.objects.filter(sales_doc__isnull=True).values_list('sales_doc_name',
                                                                                          'sales_doc_no',
                                                                                          'sales_doc_date', 'customer'))
    for sales_doc in sales_docs:
        sales_object = Sales_docs(sales_document=sales_doc[0], sales_doc_number=sales_doc[1],
                                  sales_doc_date=sales_doc[2], customer=Customer.objects.get(id=sales_doc[3]))
        sales_object.save()
        sales_docs_imports = Sales_doc_imports.objects.filter(sales_doc_name=sales_doc[0], sales_doc_no=sales_doc[1],
                                                              sales_doc_date=sales_doc[2], customer__id=sales_doc[3])
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


    return HttpResponseRedirect(reverse('salesreport:index'))


def import_cst(request):
    cust_file = request.FILES['cust']
    try:
        os.remove('cust_file')
    except:
        pass
    file_name = default_storage.save('cust_file', cust_file)

    with open(file_name, newline='', encoding='utf-8') as cust_csv:
        for line in enumerate(cust_csv, 1):
            row = line[1].rstrip('\r\n').split(';')
            fr_id = row[0]
            if not customer_check_row(row):
                continue
            try:
                customer = Customer_all.objects.get(frigat_id=fr_id)
                if customer_import_compare(row, customer):
                    continue
            except:
                customer = Customer_all(frigat_id=fr_id, date_import=date.today())
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
                try:
                    customer_maket = Customer.objects.get(Q(name__endswith=customer.name))
                    customer_maket.customer_all = customer
                    customer_maket.save()
                except:
                    pass
    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_sinhro_inn(request):
    customers = Customer.objects.filter(~Q(inn='') &
                                        (Q(customer_all__isnull=True) |
                                        (~Q(customer_group=F('customer_all__customer_group')) &
                                        (Q(customer_group__isnull=False) & Q(customer_all__customer_group__isnull=False))) |
                                        (~Q(customer_type=F('customer_all__customer_type')) &
                                        (Q(customer_type__isnull=False) & Q(customer_all__customer_type__isnull=False)))
                                         ))
    for customer in customers:
        if customer.customer_all and customer.inn == customer.customer_all.inn:
            customer_all = customer.customer_all
            customer_all.customer_group = customer.customer_group
            customer_all.customer_type = customer.customer_type
            customer_all.save()
        elif customer.inn != '' and not customer.inn:
            customer_all = Customer_all.objects.filter(inn=customer.inn).order_by('frigat_id').last()
            customer.customer_all = customer_all
            customer.frigat_id = customer_all.frigat_id
            customer.save()
            customer_all.customer_group = customer.customer_group
            customer_all.customer_type = customer.customer_type
            customer_all.save()
    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_sinhro_group(request):
    customers = Customer.objects.filter((~Q(customer_group=F('customer_all__customer_group')) |
                                        ~Q(customer_type=F('customer_all__customer_type')) |
                                        ~Q(region=F('customer_all__region'))) & Q(customer_all__isnull=False))
    for customer in customers:
        customer_all = customer.customer_all
        customer_all.customer_group = customer.customer_group
        customer_all.customer_type = customer.customer_type
        customer_all.region = customer.region
        customer_all.save()
    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_sinhro_no(request):
    customers = Customer.objects.filter(Q(inn='') &
                                        (Q(customer_all__isnull=True) |
                                        ~Q(name__endswith=F('customer_all__name')) |
                                        (~Q(customer_group=F('customer_all__customer_group')) &
                                        (Q(customer_group__isnull=False) & Q(customer_all__customer_group__isnull=False))) |
                                        (~Q(customer_type=F('customer_all__customer_type')) &
                                        (Q(customer_type__isnull=False) & Q(customer_all__customer_type__isnull=False)))
                                         ))
    customers_all = Customer_all.objects.filter(inn='')
    for customer in customers:
        for customer_all in customers_all:
            if customer.name.endswith(customer_all.name):
                customer.customer_all = customer_all
                customer.frigat_id = customer_all.frigat_id
                customer.save()
                customer_all.customer_group = customer.customer_group
                customer_all.customer_type = customer.customer_type
                customer_all.save()
    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_sinhro_err(request):
    customers = Customer.objects.filter(~Q(inn=F('customer_all__inn')) & ~Q(inn=''))
    for customer in customers:
        set_inn(customer)
    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_set_inactive(request):
    d_n = datetime.date.today() - datetime.timedelta(weeks=154)
    customers_list = Customer.objects.all()
    for cst in customers_list:
        if cst.date_last < d_n:
            cst.active = False
        else:
            cst.active = True
    Customer.objects.bulk_update(customers_list, ['active'])
    return HttpResponseRedirect(reverse('salesreport:index'))


def group_set_inactive(request):
    d_n = datetime.date.today() - datetime.timedelta(weeks=154)
    groups_list = Customer_groups.objects.all()
#    map(lambda x: x.active = False, groups_list)
    for grp in groups_list:
        if grp.date_last < d_n:
            grp.active = False
        else:
            grp.active = True
    Customer_groups.objects.bulk_update(groups_list, ['active'])
    return HttpResponseRedirect(reverse('salesreport:index'))


def group_set_dates(request):
    groups_list = Customer_groups.objects.all()
    for grp in groups_list:
        try:
            date_first = min(Customer_all.objects.filter(customer_group=grp).values_list('date_first', flat=True))
        except:
            date_first = datetime.date(2000, 1, 1)
        try:
            date_last = max(Customer_all.objects.filter(customer_group=grp).values_list('date_last', flat=True))
        except:
            date_last = datetime.date(2100, 1, 1)
        grp.date_first = date_first
        grp.date_last = date_last
    Customer_groups.objects.bulk_update(groups_list, ['date_first', 'date_last'])
    return HttpResponseRedirect(reverse('salesreport:index'))


def customer_date(request):
    customers = Customer.objects.all()
    for cst in customers:
        if type(cst.date_first) == 'str':
            cst.date_first = datetime.datetime.strptime(cst.date_first, '%Y-%m-%d').date()
    return HttpResponseRedirect(reverse('salesreport:index'))


