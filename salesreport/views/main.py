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



