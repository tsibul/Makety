import re

from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from django.core.paginator import Paginator


def groups(request):
    navi = 'Группы'
    cst_groups = Customer_groups.objects.all().order_by('group_name')
    cst_types = Customer_types.objects.all()
    group_quan = Customer_groups.objects.all().order_by('group_name').count()

    paginator = Paginator(cst_groups, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'navi': navi, 'active2': 'active', 'page_obj': page_obj, 'cst_types': cst_types,
               'group_quan': group_quan}
    return render(request, 'salesreport/customer_groups.html', context)


def update_cst_group(request):
    page_no = '?page=' + request.POST['page_no']
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
    return HttpResponseRedirect(reverse('salesreport:groups') + page_no)


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
                    customer.region == other.region) and other not in customers_other_list):
                customers_other_list.append(other)
    if not customers.count():
        for other in customers_other:
            if group.group_name in other.name:
                customers_other_list.append(other)
    return customers_other_list