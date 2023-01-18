from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from django.core.paginator import Paginator
from Makety.service import *


def customer_sales(request):
    navi = 'Клиенты'
    customers = Customer.objects.all().order_by('customer_all__name')
    paginator = Paginator(customers, 20)  # Show 20 contacts per page.

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


def customer_active(request):
    navi = 'Клиенты'
    customers = Customer.objects.filter(active=True, internal=False).order_by('customer_all__name')
    paginator = Paginator(customers, 20)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'navi': navi, 'page_obj': page_obj}
    return render(request, 'salesreport/customers.html', context)


def update_cst(request):
    page_no = '?page=' + request.POST['page_no']
    cst_id = request.POST['id']
    cst = Customer.objects.get(id=cst_id)
    nm = request.POST['nm']
    gr_old = request.POST['gr_o']
    gr_id = request.POST['gr_id']
    try:
        gr = request.POST['gr']
    except:
        gr = None
    tp_old = request.POST['tp_o']
    rg = request.POST['rg']
    in_ = request.POST['in_']
    ad = request.POST['ad']
    try:
        tp = request.POST['tp']
        type = Customer_types.objects.get(id=tp)
        cst.customer_type = type
    except:
        pass
    if gr != '' or gr_id != '':
        try:
            group = Customer_groups.objects.get(id=gr)
        except:
            try:
                group = Customer_groups.objects.get(group_name=gr_old)
            except:
                group = Customer_groups(group_name=gr_old)
                try:
                    group.group_type = type
                except:
                    pass
                group.save()
        cst.customer_group = group
    cst.name = nm
    cst.group = gr_old
    cst.type = tp_old
    cst.region = rg
    cst.inn = in_
    cst.address = ad
    cst.save()
    cst.customer_all.group = cst.group
    cst.customer_all.type = cst.type
    cst.customer_all.customer_group = cst.customer_group
    cst.customer_all.customer_type = cst.customer_type
    cst.customer_all.region = cst.region
    cst.customer_all.save()
    try:
        lookup_str = request.POST['look_up']
        lookup = request.POST['lookup']
        return render(request, 'dictionarys/customers.html', look_up_cst(lookup))
    except:
        return HttpResponseRedirect(reverse('salesreport:customers') + page_no)
