from django.shortcuts import render, HttpResponseRedirect, reverse

# Create your views here.

def index(request):
    context = {}
    return render(request, 'salesreport/index.html', context)


def customer_sales(request):
    context = {}
    return render(request, 'salesreport/customers.html', context)


def customer_groups(request):
    context = {}
    return render(request, 'salesreport/groups.html', context)


def import_report(request):
    return HttpResponseRedirect(reverse('salesreport:index'))
