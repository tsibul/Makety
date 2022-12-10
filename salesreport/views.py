from django.shortcuts import render, HttpResponseRedirect, reverse

# Create your views here.

def index(request):
    navi = 'Главная'
    context = {'navi': navi}
    return render(request, 'salesreport/index.html', context)


def customer_sales(request):
    navi = 'Клиенты'
    context = {'navi': navi}
    return render(request, 'salesreport/customers.html', context)


def customer_groups(request):
    navi = 'Группы клиентов'
    context = {'navi': navi}
    return render(request, 'salesreport/groups.html', context)


def import_report(request):
    return HttpResponseRedirect(reverse('salesreport:index'))
