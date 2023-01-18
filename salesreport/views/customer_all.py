from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from django.core.paginator import Paginator


def customers_all(request):
    navi = 'Все Клиенты'
    customers = Customer_all.objects.all().order_by('name')
    paginator = Paginator(customers, 50)  # Show 50 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'navi': navi, 'page_obj': page_obj}
    return render(request, 'salesreport/customers_all.html', context)


