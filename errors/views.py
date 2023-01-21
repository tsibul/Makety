from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from maket.models import Item_color, Order_imports, Item_imports, Customer, Customer_groups, Customer_types,\
    Print_imports, Detail_set, Makety, Additional_Files, Print_color
from django.db.models import Q, F


from maket.views import count_errors, print_position_and_color_from_print_obj, print_color_check, place_obj_from_place


def other(request):
    navi = 'admin'
    customers = Customer.objects.all().count()
    customer_groups = Customer_groups.objects.all().count

    context = {'navi': navi, 'active4': 'active', 'customers': customers, 'customer_groups': customer_groups,
               }
    context.update(count_errors())
    return render(request, 'errors/other.html', context)


def import_repairs(request):
    navi = 'admin'
    lost_imports = []
    l_imports = Item_imports.objects.filter(item=None).order_by('code')
    for l_imp in l_imports:
        try:
            l_det = Detail_set.objects.get(item_name=l_imp.item_group)
            lost_imports.append([l_imp, l_det])
        except:
            pass
    lost_imports_len = len(lost_imports)

    context = {'navi': navi, 'active4': 'active', 'lost_imports': lost_imports, 'lost_imports_len': lost_imports_len}
    context.update(count_errors())
    return render(request, 'errors/import_repairs.html', context)


def deleted_repairs(request):
    navi = 'admin'
    lost_deleted_items = list(Item_imports.objects.filter(order=None))
    lost_deleted_prints = list(Print_imports.objects.filter(item=None))
    context = {'navi': navi, 'active4': 'active', 'lost_deleted_prints': lost_deleted_prints,
               'lost_deleted_items': lost_deleted_items}
    context.update(count_errors())
    return render(request, 'errors/deleted_repairs.html', context)


def color_place_repairs(request):
    navi = 'admin'
    print_colors = list(Print_color.objects.values_list('print_item_id', flat=True))
    print_objects = Print_imports.objects.filter(Q(print_place__isnull=True) | ~Q(id__in=print_colors)).order_by('-place')
    context = {'navi': navi, 'active4': 'active', 'print_objects': print_objects}
    context.update(count_errors())
    return render(request, 'errors/color_place_repairs.html', context)


def customer_repairs(request):
    navi = 'admin'
    orders = Order_imports.objects.all().order_by('-order_date')
    changed_customers = []
    for order in orders:
        if order.customer_name != order.customer.name:
            changed_customers.append(order)
    changed_customers_len = len(changed_customers)
    context = {'navi': navi, 'active4': 'active', 'changed_customers': changed_customers,'changed_customers_len': changed_customers_len}
    context.update(count_errors())
    return render(request, 'errors/customer_repairs.html', context)


def hex_repairs(request):
    navi = 'admin'
    items = list(Item_imports.objects.filter(Q(detail1_hex='') & ~Q(detail1_color='') | \
                                        Q(detail2_hex='') & ~Q(detail2_color='') | \
                                        Q(detail3_hex='') & ~Q(detail3_color='') | \
                                        Q(detail4_hex='') & ~Q(detail4_color='') | \
                                        Q(detail5_hex='') & ~Q(detail5_color='') | \
                                        Q(detail6_hex='') & ~Q(detail6_color='')))
    lost_hex_len = len(items)
    context = {'navi': navi, 'active4': 'active',  'lost_hex': items, 'lost_hex_len': lost_hex_len}
    context.update(count_errors())
    return render(request, 'errors/hex_repairs.html', context)


def print_position_repairs(request):
    navi = 'admin'
    print_imports = Print_imports.objects.filter(Q(print_position__isnull=True) |
                                                 ~Q(print_position__position_place=F('print_place')) |
                                                 ~Q(print_position__print_group=F('item__item__print_group')))
#    error_print_position_id = []
#    for prt_imports in print_imports:
#        if prt_imports.print_position is not None:
#           if prt_imports.print_position.position_place != prt_imports.print_place or \
#              prt_imports.print_position.print_group != prt_imports.item.item.print_group:
#              error_print_position_id.append(prt_imports.id)
#    position_objects = Print_imports.objects.filter(Q(id__in=error_print_position_id) | Q(print_position__isnull=True))
#    position_count = position_objects.count()
    position_count = print_imports.count()
    context = {'navi': navi, 'active4': 'active', 'position_objects': print_imports, 'position_count': position_count}
    context.update(count_errors())
    return render(request, 'errors/print_position_repairs.html', context)


def changed_customers(request, id):
    order = Order_imports.objects.get(id=id)
    order.customer_name = order.customer.name
    order.save()
    return HttpResponseRedirect(reverse('errors:customer_repairs'))


def lost_hex(request):
    items = Item_imports.objects.filter(Q(detail1_hex='') & ~Q(detail1_color='') | \
                                        Q(detail2_hex='') & ~Q(detail2_color='') | \
                                        Q(detail3_hex='') & ~Q(detail3_color='') | \
                                        Q(detail4_hex='') & ~Q(detail4_color='') | \
                                        Q(detail5_hex='') & ~Q(detail5_color='') | \
                                        Q(detail6_hex='') & ~Q(detail6_color=''))
    for item in items:
        itm_clr = item.item_color.split('.')
        num_details = len(itm_clr)
        x = range(num_details)
        for n in x:
            detail = 'detail' + str(n + 1) + '_color'
            detail_color = getattr(item, detail)
            detail_hex = 'detail' + str(n + 1) + '_hex'
            try:
                hex_color = Item_color.objects.get(Q(color_id=detail_color) & Q(color_scheme=item.item.color_scheme)).color_code
                setattr(item, detail_hex, hex_color)
            except:
                pass
        item.save()
    return HttpResponseRedirect(reverse('errors:hex_repairs'))


def lost_imports(request, id):
    l_import = Item_imports.objects.get(id=id)
    try:
        detail_id = request.POST['l_det']
        l_import.item = Detail_set.objects.get(id=detail_id)
        l_import.save()
    except:
        #        context = {'l_import': l_import}
        #        render(request, 'maket/item_totally_lost.html', context)
        pass
    return HttpResponseRedirect(reverse('errors:import_repairs'))



def order_edit(request, id):
    ord_imp = Order_imports.objects.get(id=id)
    item_import = list(Item_imports.objects.filter(order=id).order_by('code'))
    print_import = ()
    print_ids = []
    for item in item_import:
        print_count = Print_imports.objects.filter(item=item).count()
        print_import = print_import + tuple(Print_imports.objects.filter(item=item))
        print_ids.append([item, print_count])
    print_import = list(print_import)
    context = {'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
               'print_ids': print_ids}

    return render(request, 'errors/order_edit.html', context)


def order_save(request):
    id = request.POST['order_id']
    item_import = Item_imports.objects.filter(order=id)
    print_change_list = []
    for item in item_import:
        tmp_print_id = request.POST[str(item.print_id)]
        if item.print_id != int(tmp_print_id) and [int(tmp_print_id), item.print_id] not in print_change_list:
            print_change_list.append([item.print_id, int(tmp_print_id)])
    for print_change in print_change_list:
        item_old = Item_imports.objects.get(Q(order_id=id) & Q(print_id=print_change[0]))
        prt_old = list(Print_imports.objects.filter(Q(print_id=print_change[0]) & Q(item=item_old)))
        item_new = Item_imports.objects.get(Q(order_id=id) & Q(print_id=print_change[1]))
        prt_new = list(Print_imports.objects.filter(Q(print_id=print_change[1]) & Q(item=item_new)))
        for prt_o in prt_old:
            prt_o.item = item_new
            prt_o.print_id = item_new.print_id
            prt_o.save()
        for prt_n in prt_new:
            prt_n.item = item_old
            prt_n.print_id = item_old.print_id
            prt_n.save()

    return HttpResponseRedirect(reverse('errors:order_edit', kwargs={'id': id}))


def badge_file_count(request):
    orders = Order_imports.objects.all()
    page_no = '?page=' + request.POST['page_no']
    for order in orders:
        if order.order_upload:
            order.number_orders = 1
        order.number_makets = Makety.objects.filter(Q(order=order) & Q(uploaded=True)).count()
        order.number_additional = Additional_Files.objects.filter(order_id=order).count()
        order.save()
    return HttpResponseRedirect(reverse('orders:index') + page_no)


def print_place_connect(request):
    print_colors = list(Print_color.objects.values_list('print_item_id', flat=True))
    print_objects = Print_imports.objects.filter(Q(print_place__isnull=True) | ~Q(id__in=print_colors)).order_by('-place')
    for prt_obj in print_objects:
        place = place_obj_from_place(prt_obj.place)
        print_pos = print_position_and_color_from_print_obj(place, prt_obj)
        if print_pos != '':
            prt_obj.print_position = print_pos
        if prt_obj.place != '':
            prt_obj.print_place = place
        if prt_obj.place != '' or print_pos != '':
            prt_obj.save()
        if prt_obj.id not in print_colors:
            if print_colors.count(prt_obj.id) != prt_obj.colors:
                Print_color.objects.filter(print_item=prt_obj).delete()
            print_color_check(prt_obj)
    return HttpResponseRedirect(reverse('errors:color_place_repairs'))


def print_position_fix(request):
    print_imports = Print_imports.objects.all()
    for prt_imports in print_imports:
        if prt_imports.print_position is not None and \
                (prt_imports.print_position.position_place != prt_imports.print_place or
                 prt_imports.print_position.print_group != prt_imports.item.item.print_group) or \
                prt_imports.print_position is None:
            print_pos = print_position_and_color_from_print_obj(prt_imports.print_place, prt_imports)
            if print_pos != '':
                prt_imports.print_position = print_pos
                prt_imports.save()
    return HttpResponseRedirect(reverse('errors:print_position_repairs'))
#TODO change cycle to Query


def additional(request):
    navi = 'admin'
    additional_files = Additional_Files.objects.filter(additional_file__isnull=True)
    context = {'navi': navi, 'active4': 'active', 'additional_files': additional_files}
    context.update(count_errors())
    return render(request, 'errors/additional_repairs.html', context)


def delete_additional_file_from_table(request):
    add_file_id = request.POST['file_id']
    add_file = Additional_Files.objects.get(id=add_file_id)
    return HttpResponseRedirect(reverse('errors:additional_repairs'))


