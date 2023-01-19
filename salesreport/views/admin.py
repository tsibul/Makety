from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color, Order_imports
from salesreport.models import Sales_doc_imports, Sales_docs

def admin(request):
    navi = 'Admin'
    context = {'navi': navi}
    return render(request, 'salesreport/admin.html', context)


def transaction_delete(request):
    Sales_docs.objects.all().delete()
    Sales_doc_imports.objects.all().delete()
    return HttpResponseRedirect(reverse('salesreport:admin'))

def customer_all_delete(request):
    Customer_all.objects.all().delete()
    customers_id = set(Order_imports.objects.all().values_list('customer', flat=True))
    Customer.objects.exclude(id__in=customers_id).delete()
    fr_id = [''] * Customer.objects.all().count()
    customers = Customer.objects.all()
    for customer in customers:
        customer.frigat_id = ''
    Customer.objects.bulk_update(customers, ['frigat_id'])
    return HttpResponseRedirect(reverse('salesreport:admin'))
