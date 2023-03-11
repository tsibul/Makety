from django.http import FileResponse
from django.shortcuts import render, HttpResponseRedirect, reverse
import datetime
from maket.models import Customer_all, Customer_groups
from django.core.paginator import Paginator
from Makety.service import *
from django.core.files.storage import default_storage


def customer_active(request):
    navi = 'Клиенты'
    customers = Customer_all.objects.filter(date_last__gt=datetime.date(2017, 1, 1), internal=False).order_by('name')
    customer_types = Customer_types.objects.all()
    customer_groups = Customer_groups.objects.all().order_by('group_name')

    context = {'navi': navi, 'page_obj': customers, 'customer_types': customer_types,
               'customer_groups': customer_groups}
    return render(request, 'salesreport/customers.html', context)


def update_cst(request):
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
    return HttpResponseRedirect(reverse('salesreport:customers_active'))


def import_inn(request):
    customers_no_inn = Customer_all.objects.filter(inn='', internal=False).values_list('frigat_id', flat=True)
    with open('cust_file', newline='', encoding='utf-8') as group_csv:
        for line in enumerate(group_csv, 1):
            row = line[1].rstrip('\r\n').split(';')
            if row[0] in customers_no_inn and row[3] != '':
                inn = row[3]
                if len(inn) == 9 or len(inn) == 11:
                    inn = '0' + str(inn)
                customer = Customer_all.objects.get(frigat_id=row[0])
                customer.inn = inn
                customer.save()
    return HttpResponseRedirect(reverse('salesreport:customers_active'))

def export_cst_types(request):
    customers = Customer_all.objects.filter(customer_type__isnull=False, internal=False)
    customers_int = Customer_all.objects.filter(internal=True)
    date_rep = datetime.date.today().strftime('%d%m%Y')
    export_file_name = 'export_types_' + date_rep + '.csv'

    with open(export_file_name, 'a+', newline='', encoding='utf-8') as export_file:
        for customer in customers:
            string = customer.frigat_id + ';' + customer.customer_type.code + ';' + \
                     str(customer.internal) + ';' + customer.name + ';' + customer.inn + '\n'
            export_file.write(string)
        for customer in customers_int:
            string = customer.frigat_id + ';' + '' + ';' + \
                     str(customer.internal) + ';' + customer.name + ';' + customer.inn + '\n'
            export_file.write(string)
    try:
        return FileResponse(open(export_file_name, 'rb'), content_type='application/force-download')
    except:
        return HttpResponseRedirect(reverse('salesreport:customers_active'))

