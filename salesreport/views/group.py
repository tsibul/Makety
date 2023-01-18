from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from django.core.paginator import Paginator


def groups(request):
    navi = 'Группы'
    cst_groups = Customer_groups.objects.all().order_by('group_name')
    cst_types = Customer_types.objects.all()
    group_quan = Customer_groups.objects.all().order_by('group_name').count()

    paginator = Paginator(cst_groups, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'navi': navi, 'active2': 'active', 'page_obj': page_obj, 'cst_types': cst_types, 'group_quan': group_quan}
    return render(request, 'salesreport/customer_groups.html', context)


def update_cst_group(request):
    page_no = '?page=' + request.POST['page_no']
    group_name = request.POST['gr_nm']
    type_id = request.POST['tp']
    gr_tp = Customer_types.objects.get(id=type_id)
    try:
        group_id = request.POST['gr_id']
        group = Customer_groups.objects.get(id=group_id)
        group.group_name = group_name
    except:
        group = Customer_groups(group_name=group_name)
    group.group_type = gr_tp
    group.save()
    return HttpResponseRedirect(reverse('salesreport:groups') + page_no)
