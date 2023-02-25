from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from django.core.paginator import Paginator
from Makety.service import *


def customer_active(request):
    navi = 'Клиенты'
    customers = Customer_all.objects.filter(active=True, internal=False).order_by('name')
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
    cst.name = nm
    cst.region = rg
    cst.inn = in_
    cst.address = ad
    cst.save()
    cst.customer_all.customer_group = cst.customer_group
    cst.customer_all.customer_type = cst.customer_type
    cst.customer_all.region = cst.region
    cst.customer_all.save()
    try:
        lookup_str = request.POST['look_up']
        lookup = request.POST['lookup']
        return render(request, 'salesreport/customers.html', look_up_cst(lookup))
    except:
        return HttpResponseRedirect(reverse('salesreport:customers') + page_no)
