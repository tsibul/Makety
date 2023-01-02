from datetime import date
import os


from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types
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
        date_last_cst = max(Customer_all.objects.values_list('date_import', flat=True))
    except:
        date_last_cst = '2010-01-01'
    customers_quantity = Customer_all.objects.all().count()
    customers_active_quantity = Customer.objects.all().count()
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
               'customers_active_quantity': customers_active_quantity, 'sinhronized': sinhronized}
    return render(request, 'salesreport/index.html', context)


def import_report(request):
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
            customer.inn = row[3]
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
    customers = Customer.objects.all().order_by('name')
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

