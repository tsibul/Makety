from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from django.db.models import Q, F


def cst_unsinhronized(request):
    unsinhronized = Customer.objects.filter(~(Q(customer_all__isnull=False) &
                                          Q(group=F('customer_all__group')) &
                                          Q(type=F('customer_all__type')) &
                                          (Q(customer_group=F('customer_all__customer_group')) |
                                          Q(customer_group__isnull=True) & Q(customer_all__customer_group__isnull=True)) &
                                          (Q(customer_type=F('customer_all__customer_type')) |
                                          Q(customer_type__isnull=True) & Q(customer_all__customer_type__isnull=True)) &
                                          Q(inn=F('customer_all__inn')) &
                                          Q(name__endswith=F('customer_all__name'))
                                          ))
    context = {'customers': unsinhronized}

    return render(request, 'salesreport/unsinhronized.html', context)


