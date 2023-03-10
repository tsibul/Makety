from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer_groups
from salesreport.models import ReportPeriod, Sales_docs, Sales_doc_imports


def client_transactions(request, client_id, period_id):
    period = ReportPeriod.objects.get(id=period_id)
    customer = Customer_all.objects.get(id=client_id)
    group = customer.customer_group
    if not group:
        transactions = Sales_docs.objects.filter(customer=customer, sales_doc_date__gte=period.date_begin,
                                                 sales_doc_date__lte=period.date_end).order_by('sales_doc_date')
        name = customer.name.replace('"', '')
    else:
        transactions = Sales_docs.objects.filter(customer__customer_group=group,
                                                 sales_doc_date__gte=period.date_begin,
                                                 sales_doc_date__lte=period.date_end).order_by('sales_doc_date')
        name = group.group_name

    context = {'transactions': transactions, 'name': name, 'period': period}
    return render(request, 'salesreport/client_transactions.html', context)


def detail(request, salesdoc_id):
    operations = Sales_doc_imports.objects.filter(sales_doc__id=salesdoc_id)
    context = {'operations': operations}
    return render(request, 'salesreport/detail.html', context)
