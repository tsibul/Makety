import datetime
import os

from django.http import FileResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer_groups, Customer_types
from django.core.files.storage import default_storage


def groups(request):
    navi = 'Группы'
    customer_groups = Customer_groups.objects.all().order_by('group_name')
    cst_groups = []
    for group in customer_groups:
        cst_groups.append([group, Customer_all.objects.filter(customer_group=group).count()])
    cst_types = Customer_types.objects.all()
    group_quan = Customer_groups.objects.all().order_by('group_name').count()

    context = {'navi': navi, 'active2': 'active', 'page_obj': cst_groups, 'cst_types': cst_types,
               'group_quan': group_quan}
    return render(request, 'salesreport/customer_groups.html', context)


def update_cst_group(request):
    group_name = request.POST['gr_nm']
    type_id = request.POST['tp']
    gr_tp = Customer_types.objects.get(id=type_id)
    try:
        group_id = request.POST['gr_id']
        group = Customer_groups.objects.get(id=group_id)
        group.group_name = group_name
    except:
        group = Customer_groups(group_name=group_name)
    group.group_type = gr_tp
    group.save()
    return HttpResponseRedirect(reverse('salesreport:groups'))


def group_lists(request):
    navi = 'Списки групп'
    try:
        group_id = request.POST['group_id']
    except:
        group_id = Customer_groups.objects.first().id
    groups = Customer_groups.objects.all().order_by('group_name')
    group = Customer_groups.objects.get(id=group_id)
    customers = Customer_all.objects.filter(customer_group=group)
    customers_other_list = prepare_other_customers(customers, group)
    group_id = int(group_id)

    context = {'navi': navi, 'groups': groups, 'customers': customers, 'customers_other': customers_other_list,
               'group_id': group_id}
    return render(request, 'salesreport/groups.html', context)


def group_delete(request):
    group_id = request.POST['group_id']
    group = Customer_groups.objects.get(id=group_id)
    members = Customer_all.objects.filter(customer_group=group).count()
    if not members:
        group.delete()
    return HttpResponseRedirect(reverse('salesreport:groups'))


def add_to_group(request):
    navi = 'Списки групп'
    group_id = request.POST['group_id']
    cust_id = request.POST['cust_id']
    group = Customer_groups.objects.get(id=group_id)
    groups = Customer_groups.objects.all().order_by('group_name')
    customer = Customer_all.objects.get(id=cust_id)
    customer.customer_group = group
    customer.save()
    customers = Customer_all.objects.filter(customer_group=group)
    customers_other_list = prepare_other_customers(customers, group)
    group_id = int(group_id)

    context = {'navi': navi, 'groups': groups, 'customers': customers, 'customers_other': customers_other_list,
               'group_id': group_id}
    return render(request, 'salesreport/groups.html', context)


def delete_from_group(request):
    navi = 'Списки групп'
    group_id = request.POST['group_id']
    cust_id = request.POST['cust_id']
    group = Customer_groups.objects.get(id=group_id)
    groups = Customer_groups.objects.all().order_by('group_name')
    customer = Customer_all.objects.get(id=cust_id)
    customer.customer_group = None
    customers = Customer_all.objects.filter(customer_group=group)
    customers_other_list = prepare_other_customers(customers, group)
    group_id = int(group_id)

    context = {'navi': navi, 'groups': groups, 'customers': customers, 'customers_other': customers_other_list,
               'group_id': group_id}
    return render(request, 'salesreport/groups.html', context)


def group_export(request):
    date_rep = datetime.date.today().strftime('%d%m%Y')
    customers = Customer_all.objects.filter(customer_group__isnull=False).order_by('customer_group')
    export_file_name = 'export_groups_' + date_rep + '.csv'

    with open(export_file_name, 'a+', newline='', encoding='utf-8') as export_file:
        for customer in customers:
            string = customer.customer_group.group_name + ';' + customer.customer_group.group_type.code + ';' + \
                     customer.frigat_id + ';' + customer.name + ';' + customer.inn + '\n'
            export_file.write(string)
    try:
        return FileResponse(open(export_file_name, 'rb'), content_type='application/force-download')
    except:
        return HttpResponseRedirect(reverse('salesreport:groups'))


def group_import(request):
    report_file = request.FILES['importGroup']
    try:
        os.remove('report_file')
    except:
        pass
    file_name = default_storage.save('report_file', report_file)
    with open(file_name, newline='', encoding='utf-8') as group_csv:
        for line in enumerate(group_csv, 1):
            groups = Customer_groups.objects.all().values_list('group_name', flat=True)
            row = line[1].rstrip('\r\n').split(';')
            customer = Customer_all.objects.get(frigat_id=row[2])
            customer_maket = Customer_all.objects.get(frigat_id=row[2])
            customer_type = Customer_types.objects.get(code=row[1])
            if row[0] not in groups:
                new_group = Customer_groups(group_name=row[0], group_type=customer_type, phone=customer.phone,
                                            mail=customer.mail)
                new_group.save()
            else:
                new_group = Customer_groups.objects.get(group_name=row[0])
            customer.customer_group = new_group
            if not customer.customer_type:
                customer.customer_type = customer_type
            customer.save()
            customer_maket.customer_group = new_group
            customer_maket.save()
        return HttpResponseRedirect(reverse('salesreport:groups'))


def prepare_other_customers(customers, group):
    customers_other = Customer_all.objects.filter(customer_group__isnull=True, internal=False)
    customers_other_list = []
    for customer in customers:
        c_a = customer.address.replace('ул.', '').replace('г.', '').replace('д.', '').replace('дoм.', ''). \
                  replace('.', '').replace(',', '').replace('-', '').replace(' ', '')[12: 40]
        for other in customers_other:
            o_a = other.address.replace('ул.', '').replace('г.', '').replace('д.', '').replace('дoм.', ''). \
                replace('.', '').replace(',', '').replace('-', '').replace(' ', '')
            if ((c_a in o_a or customer.name[2:-2] in other.name) or (
                    customer.region != '77' and customer.region != '50' and customer.region != '97' and
                    customer.region == other.region) and other not in customers_other_list) or (
                    customer.mail == other.mail and other.mail != ''):
                customers_other_list.append(other)
    if not customers.count():
        for other in customers_other:
            if group.group_name in other.name:
                customers_other_list.append(other)
    return customers_other_list
