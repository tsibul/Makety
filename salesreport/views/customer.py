from django.shortcuts import render, HttpResponseRedirect, reverse
import datetime
from maket.models import Customer_all, Customer_groups
from django.core.paginator import Paginator
from Makety.service import *


def customer_active(request):
    navi = 'Клиенты'
    customers = Customer_all.objects.filter(date_last__gt=datetime.date(2000, 1,  1), internal=False).order_by('name')
    customer_types = Customer_types.objects.all()
    customer_groups = Customer_groups.objects.all().order_by('group_name')

    paginator = Paginator(customers, 30)  # Show contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'navi': navi, 'page_obj': page_obj, 'customer_types': customer_types, 'customer_groups': customer_groups}
    return render(request, 'salesreport/customers.html', context)


def update_cst(request):
    page_no = '?page=' + request.POST['page_no']
    cst_id = request.POST['id']
    cst = Customer_all.objects.get(id=cst_id)
    nm = request.POST['nm']
    gr_id = request.POST['gr_id']
    try:
        gr = request.POST['gr']
    except:
        gr = None
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
            cst.customer_group = group
        except:
            pass
    try:
        request.POST['in']
        cst.internal = True
    except:
        pass
    cst.name = nm
    cst.region = rg
    cst.inn = in_
    cst.address = ad
    cst.save()
    '''
    try:
        lookup_str = request.POST['look_up']
        lookup = request.POST['lookup']
        return render(request, 'salesreport/customers.html', look_up_cst(lookup))
    except:
    '''
    return HttpResponseRedirect(reverse('salesreport:customers_active') + page_no)
