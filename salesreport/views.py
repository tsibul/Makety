import datetime
from datetime import date
import os


from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from .models import Sales_doc_imports, Sales_docs
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.db.models import Q, F


def customer_import_compare(row, customer):
    return customer.name == row[1] and \
           customer.form == row[2] and \
           customer.inn == row[3] and \
           customer.address == row[5] and \
           customer.phone == row[6] and \
           customer.mail == row[7] and \
           customer.comment == row[8] and \
           customer.all_phones == row[13] and \
           customer.all_mails == row[12]


def customer_check_row(row):
    result = (len(row) == 14)
    empty = True
    for i in range(2, len(row)):
        empty = empty and (row[i] == '' or row[i] == '0')
    return result and not empty


def customer_type_chose(type, region):
    if 'Конечник' in type and (region == '77' or region == '50'):
        type_obj = Customer_types.objects.get(type_name='Конечник Москва')
    elif 'Конечник' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Конечник Регион')
    elif 'рекламщик' in type and region == '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Рекламщик Москва')
    elif 'рекламщик' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Рекламщик Регион')
    elif 'Агентство' in type and region == '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Агентство Москва')
    elif 'Агентство' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Агентство Регион')
    elif 'Дилер' in type and region == '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Дилер Москва')
    elif 'Дилер' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Дилер Регион')
    elif 'точка' in type and region != '77' and region != '50':
        type_obj = Customer_types.objects.get(type_name='Розничная Точка')
    else:
        type_obj = ''
    return type_obj


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
    customers_quantity = Customer_all.objects.all().count()
    customers_active_quantity = Customer.objects.all().count()
    sales_doc_quantity = Sales_docs.objects.all().count()
    transactions_quantity = Sales_doc_imports.objects.all().count()
    no_doc = Sales_doc_imports.objects.filter(sales_doc__isnull=True).count()
    no_cust = Sales_docs.objects.filter(customer__isnull=True).count()
    no_good = Sales_doc_imports.objects.filter(detail_set__isnull=True).count()
    sinhronized = Customer.objects.filter(Q(customer_all__isnull=False) &
                                          Q(group=F('customer_all__group')) &
                                          Q(type=F('customer_all__type')) &
                                          (Q(customer_group=F('customer_all__customer_group')) |
                                          Q(customer_group__isnull=True) & Q(customer_all__customer_group__isnull=True)) &
                                          (Q(customer_type=F('customer_all__customer_type')) |
                                          Q(customer_type__isnull=True) & Q(customer_all__customer_type__isnull=True)) &
                                          Q(inn=F('customer_all__inn')) &
                                          Q(name__endswith=F('customer_all__name'))
                                          ).count()
    context = {'navi': navi, 'date_last_cst': date_last_cst, 'customers_quantity': customers_quantity,
               'customers_active_quantity': customers_active_quantity, 'sinhronized': sinhronized,
               'date_last': date_last, 'sales_doc_quantity': sales_doc_quantity,
               'transactions_quantity': transactions_quantity, 'no_doc': no_doc, 'no_cust': no_cust, 'no_good': no_good}
    return render(request, 'salesreport/index.html', context)


def import_report(request):
    report_file = request.FILES['importReport']
    start_date = datetime.datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
    Sales_doc_imports.objects.filter(sales_doc_date__gte=start_date).delete()
    Sales_docs.objects.filter(sales_doc_date__gte=start_date).delete()
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
                pass
            try:
                customer = Customer.objects.get(frigat_id=customer_frigat_id)
            except:
                customer = Customer(frigat_id=customer_frigat_id,
                                    date_first=sales_doc_date,
                                    name=(customer_all.form + ' ' + customer_all.name), address=customer_all.address,
                                    inn=customer_all.inn, region=customer_all.region, type=customer_all.type,
                                    group=customer_all.group, customer_type=customer_all.customer_type,
                                    customer_group=customer_all.customer_group, customer_all=customer_all)
            if customer.date_first == datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date() \
                    or sales_doc_date < customer.date_first:
                customer.date_first = sales_doc_date
            if customer.date_last == datetime.datetime.strptime('2100-01-01', '%Y-%m-%d').date() \
                    or sales_doc_date > datetime.datetime.strptime(str(customer.date_last), '%Y-%m-%d').date():
                customer.date_last = sales_doc_date
            report_record = Sales_doc_imports(import_date=import_date, code=code, detail_set=detail_set,
                                              color_code=color_code, main_color=main_color, item_color=item_color,
                                              series_id=series_id, good_id=good_id, good_group_id=good_group_id,
                                              good_group=good_group, good_title=good_title, good_name=good_name,
                                              code_1=code_1, quantity=quantity, sales_doc_name=sales_doc_name,
                                              sales_doc_no=sales_doc_no, sales_doc_date=sales_doc_date,
                                              buy_without_vat=buy_without_vat, buy_with_vat=buy_with_vat,
                                              sales_quantity=sales_quantity, sale_without_vat=sale_without_vat,
                                              sale_with_vat=sale_with_vat, sale_price_vat=sale_price_vat,
                                              customer_name=customer_name, customer_frigat_id=customer_frigat_id,
                                              customer=customer, customer_all=customer_all)
            records_list.append(report_record)
            customer_list.append(customer)
        new_records = Sales_doc_imports.objects.bulk_create(records_list)
        new_customers = Customer.objects.bulk_update(customer_list, ['frigat_id', 'date_first', 'name', 'address', 'inn',
                                                                     'region', 'type', 'group', 'customer_type',
                                                                     'customer_group', 'customer_all', 'date_last'])
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
        sales_object.eco = eco >= sales_object.total_sale_without_vat
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
                customer.type = customer.customer_type.type_name
            except:
                pass
            customer.save()

    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_sinhro_inn(request):
    customers = Customer.objects.filter(~Q(inn='') &
                                        (Q(customer_all__isnull=True) |
                                        (~Q(group=F('customer_all__group'))) |
                                        (~Q(type=F('customer_all__type'))) |
                                        (~Q(customer_group=F('customer_all__customer_group')) &
                                        (Q(customer_group__isnull=False) & Q(customer_all__customer_group__isnull=False))) |
                                        (~Q(customer_type=F('customer_all__customer_type')) &
                                        (Q(customer_type__isnull=False) & Q(customer_all__customer_type__isnull=False)))
                                         ))
    for customer in customers:
        if customer.customer_all and customer.inn == customer.customer_all.inn:
            customer_all = customer.customer_all
            customer_all.group = customer.group
            customer_all.customer_group = customer.customer_group
            customer_all.type = customer.type
            customer_all.customer_type = customer.customer_type
            customer_all.save()
        elif customer.inn != '' and not customer.inn:
            customer_all = Customer_all.objects.filter(inn=customer.inn).order_by('frigat_id').last()
            customer.customer_all = customer_all
            customer.frigat_id = customer_all.frigat_id
            customer.save()
            customer_all.group = customer.group
            customer_all.customer_group = customer.customer_group
            customer_all.type = customer.type
            customer_all.customer_type = customer.customer_type
            customer_all.save()
    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_sinhro_group(request):
    customers = Customer.objects.filter(~Q(group=F('customer_all__group')) |
                                        ~Q(type=F('customer_all__type')) |
                                        ~Q(customer_group=F('customer_all__customer_group')) |
                                        ~Q(customer_type=F('customer_all__customer_type')) |
                                        ~Q(region=F('customer_all__region')))
    for customer in customers:
        customer_all = customer.customer_all
        customer_all.group = customer.group
        customer_all.customer_group = customer.customer_group
        customer_all.type = customer.type
        customer_all.customer_type = customer.customer_type
        customer_all.region = customer.region
        customer_all.save()
    return HttpResponseRedirect(reverse('salesreport:index'))



def cst_sinhro_no(request):
    customers = Customer.objects.filter(Q(inn='') &
                                        (Q(customer_all__isnull=True) |
                                        ~Q(name__endswith=F('customer_all__name')) |
                                        (~Q(group=F('customer_all__group'))) |
                                        (~Q(type=F('customer_all__type'))) |
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
                customer_all.group = customer.group
                customer_all.customer_group = customer.customer_group
                customer_all.type = customer.type
                customer_all.customer_type = customer.customer_type
                customer_all.save()
    return HttpResponseRedirect(reverse('salesreport:index'))


def cst_unsinhronized(request):
    unsinhronized = Customer.objects.filter(~(Q(customer_all__isnull=False) &
                                          Q(group=F('customer_all__group')) &
                                          Q(type=F('customer_all__type')) &
                                          (Q(customer_group=F('customer_all__customer_group')) |
                                          Q(customer_group__isnull=True) & Q(customer_all__customer_group__isnull=True)) &
                                          (Q(customer_type=F('customer_all__customer_type')) |
                                          Q(customer_type__isnull=True) & Q(customer_all__customer_type__isnull=True)) &
                                          Q(inn=F('customer_all__inn')) &
                                          Q(name__endswith=F('customer_all__name'))
                                          ))
    context = {'customers': unsinhronized}

    return render(request, 'salesreport/unsinhronized.html', context)


def set_inn(customer):
    cust_all = Customer_all.objects.filter(inn=customer.inn).order_by('frigat_id').last()
    customer.customer_all = cust_all
    customer.frigat_id = cust_all.frigat_id
    customer.save()


def cst_sinhro_err(request):
    customers = Customer.objects.filter(~Q(inn=F('customer_all__inn')) & ~Q(inn=''))
    for customer in customers:
        set_inn(customer)
    return HttpResponseRedirect(reverse('salesreport:index'))



def customer_sales(request):
    navi = 'Клиенты'
    customers = Customer.objects.all().order_by('customer_all__name')
    paginator = Paginator(customers, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cst_range = []
    for i in range(page_obj.paginator.num_pages):
        page_obj2 = paginator.get_page(i + 1)
        try:
            cst_tmp = str(page_obj2.object_list[0])
            cst_range.append([i + 1, '> ' + cst_tmp])
        except:
            cst_range.append(['нет данных'])

    context = {'navi': navi, 'page_obj': page_obj, 'cst_range': cst_range}
    return render(request, 'salesreport/customers.html', context)


def customer_all(request):
    navi = 'Все Клиенты'
    customers = Customer_all.objects.all().order_by('name')
    paginator = Paginator(customers, 50)  # Show 50 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'navi': navi, 'page_obj': page_obj}
    return render(request, 'salesreport/customers_all.html', context)


def customer_groups(request):
    navi = 'Группы клиентов'
    context = {'navi': navi}
    return render(request, 'salesreport/groups.html', context)


def customer_date(request):
    customers = Customer.objects.all()
    for cst in customers:
        if type(cst.date_first) == 'str':
            cst.date_first = datetime.datetime.strptime(cst.date_first, '%Y-%m-%d').date()
    return HttpResponseRedirect(reverse('salesreport:index'))

