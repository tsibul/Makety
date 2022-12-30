from datetime import date
import os

from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Customer_all, Customer, Customer_groups, Customer_types
from django.core.paginator import Paginator
from django.core.files.storage import default_storage



def index(request):
    navi = 'Главная'
    try:
        date_last_cst = max(Customer_all.objects.values_list('date_import', flat=True))
    except:
        date_last_cst = '2010-01-01'
    customers_quantity = Customer_all.objects.all().count()
    customers_active_quantity = Customer.objects.all().count()
    context = {'navi': navi, 'date_last_cst': date_last_cst, 'customers_quantity': customers_quantity,
               'customers_active_quantity': customers_active_quantity}
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
            line = line[1].rstrip('\r\n')
            row = line.split(';')
            fr_id = row[0]
            cust = Customer_all.objects
            name = row[1]
            form = row[2]
            inn = row[3]
            try:
                region = inn[0:2]
            except:
                region = ''
            address = row[5]
            phone = row[6]
            mail = row[7]
            comment = row[8]
            our_manager = row[10]
            type = row[11]
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
                type_obj = None
            all_mails = row[12]
            all_phones = row[13]
            date_import = date.today()
            try:
                customer = Customer_all.objects.get(frigat_id=fr_id)
            except:
                customer = Customer_all(frigat_id=fr_id, date_import=date_import)
            customer.name = name
            customer.form = form
            customer.inn = inn
            customer.address = address
            customer.region = region
            customer.comment = comment
            customer.our_manager = our_manager
            customer.phone = phone
            customer.mail = mail
            customer.all_phones = all_phones
            customer.all_mails = all_mails
            try:
                customer.customer_type = type_obj
                customer.type = type_obj.type_name
            except:
                pass
            customer.save()

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
    context = {'navi': navi, 'page_obj': page_obj}
    return render(request, 'salesreport/customers_all.html', context)


def customer_groups(request):
    navi = 'Группы клиентов'
    context = {'navi': navi}
    return render(request, 'salesreport/groups.html', context)

