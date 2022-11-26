import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from maket.models import Print_position, Item_imports, Makety, Itemgroup_in_Maket, Print_in_Maket, Print_color
from django.db.models import Q

from maket.views import order_imports, prt_imports


def maket_print(request, id, mk_id):
    ord_imp = order_imports(id)[0]
    item_import = order_imports(id)[1]
    print_import = order_imports(id)[2]
    print_import_color_print = []
    for prt_import in print_import:
        print_color = Print_color.objects.filter(print_item=prt_import)
        colors = []
        for prt_color in print_color:
            colors.append(prt_color.color_pantone)
        print_import_color_print.append([prt_import, colors])
    context = {'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import_color_print}

    order_id = ord_imp.id
    product_range = prt_imports(order_id, print_import, ord_imp, mk_id)[1]
    context_imp = prt_imports(order_id, print_import, ord_imp, mk_id)[0]
    context.update({'product_range': product_range, 'mk_id': mk_id})
    context.update(context_imp)

    mkt = Makety.objects.filter(order=ord_imp).order_by('maket_id')
    maket_id_list = []
    for mk in mkt:
        maket_id_list.append(mk.maket_id)
    context.update({'maket_id_list': maket_id_list, 'len_maket': len(maket_id_list) + 1})
    try:
        maket = Makety.objects.get(order=ord_imp, maket_id=mk_id)
        itemgroup_in_maket = Itemgroup_in_Maket.objects.filter(maket=maket)
        print_in_maket = Print_in_Maket.objects.filter(maket=maket)
        context.update({'maket': maket})
        for ig in itemgroup_in_maket:
            ig_id = ig.item.item.print_group.code
            ig_ch = ig.checked
            context.update({ig_id: ig_ch})
    except:
        pass

    return render(request, 'maket_layout/maket_print.html', context)


def maket_print_empty(request, id, mk_id):
    ord_imp = order_imports(id)[0]
    item_import = order_imports(id)[1]
    print_import = order_imports(id)[2]
    context = {'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import}

    order_id = ord_imp.id
    product_range = prt_imports(order_id, print_import, ord_imp, mk_id)[1]
    context_imp = prt_imports(order_id, print_import, ord_imp, mk_id)[0]
    context.update({'product_range': product_range, 'mk_id': mk_id})
    context.update(context_imp)

    mkt = Makety.objects.filter(order=ord_imp).order_by('maket_id')
    maket_id_list = []
    for mk in mkt:
        maket_id_list.append(mk.maket_id)
    context.update({'maket_id_list': maket_id_list, 'len_maket': len(maket_id_list) + 1})
    try:
        maket = Makety.objects.get(order=ord_imp, maket_id=mk_id)
        itemgroup_in_maket = Itemgroup_in_Maket.objects.filter(maket=maket)
        print_in_maket = Print_in_Maket.objects.filter(maket=maket)
        context.update({'maket': maket})
        for ig in itemgroup_in_maket:
            ig_id = ig.item.item.print_group.code
            ig_ch = ig.checked
            context.update({ig_id: ig_ch})
    except:
        pass

    return render(request, 'maket_layout/maket_print_empty.html', context)


def update_maket(request, id):
    maket_id = request.POST['maket_id']
    ord_imp = order_imports(id)[0]
    item_import = order_imports(id)[1]
    print_import = order_imports(id)[2]
    order_id = ord_imp.id
    product_range = prt_imports(order_id, print_import, ord_imp, maket_id)[1]
    all_checked = True
    try:
        maket = Makety.objects.get(Q(maket_id=maket_id) & Q(order=ord_imp))
        maket.date_modified = datetime.date.today()
    except:
        maket = Makety(maket_id=maket_id, order=ord_imp, date_create=datetime.date.today(), order_num=ord_imp.order_id,
                       order_date=ord_imp.order_date, date_modified=datetime.date.today())
    maket.save()
    for pr_rg in product_range:
        prt = 'chck_' + pr_rg[2] + '_' + pr_rg[9]
        itemgroup = pr_rg[5]
        items_checked = []
        itm_checked = Item_imports.objects.filter(Q(item__print_group__code=itemgroup) & Q(order=ord_imp) & \
                                                  Q(print_name=pr_rg[10])).first()
        try:
            item_checked = Itemgroup_in_Maket.objects.get(
                Q(item=itm_checked) & Q(maket=maket) & Q(print_name=pr_rg[10]))
        except:
            item_checked = Itemgroup_in_Maket(item=itm_checked, maket=maket, print_name=pr_rg[10])
        try:
            sel_item = request.POST[prt]
            if sel_item == 'on':
                item_checked.checked = True
        except:
            item_checked.checked = False
            all_checked = False
        item_checked.maket = maket
        item_checked.save()
        items_checked.append(item_checked)  # ////
        ord_imp.maket_status = 'P'
    ord_imp.save()
    for pi in print_import:
        try:
            pr_in_maket = Print_in_Maket.objects.get(Q(print_item=pi) & Q(maket=maket))
        except:
            pr_in_maket = Print_in_Maket(print_item=pi, maket=maket)
        chck = 'chck_' + pi.item.item.print_group.code + '_' + \
               pi.item.print_name.replace(' ', '_').replace(',', '').replace('+', '_') + '_' + str(pi.id)
        try:
            pi_maket = request.POST[chck]
            pr_in_maket.checked = True
        except:
            pr_in_maket.checked = False
        if pi.item.item.print_group.options > 1 and pi.type != 'Soft Touch':
            pen_pos = 'pen_pos_' + str(pi.id)
            option = request.POST[pen_pos]
            prt_position = Print_position.objects.get(Q(position_place=pi.print_place) & Q(print_group=pi.item.item.print_group)\
                                                        & Q(orientation_id=option))
            pr_in_maket.option = option
        else:
            pr_in_maket.option = 0
            prt_position = Print_position.objects.get(Q(position_place=pi.print_place) & Q(print_group=pi.item.item.print_group) \
                                                      & Q(orientation_id=1))
        pi.print_position = prt_position
        pi.save()
        pr_in_maket.save()
        colors = list(Print_color.objects.filter(print_item=pi))
        for color in colors:
            try:
                color_input = request.POST[str(pi.id) + '_' + str(color.color_number_in_item)]
                color.color_pantone = color_input
                color.save()
            except:
                pass
    return HttpResponseRedirect(reverse('maket_layout:maket_print', args=[id, maket_id]))


def update_maket_empty(request, id):
    maket_id = request.POST['maket_id']
    ord_imp = order_imports(id)[0]
    item_import = order_imports(id)[1]
    print_import = order_imports(id)[2]
    order_id = ord_imp.id
    product_range = prt_imports(order_id, print_import, ord_imp, maket_id)[1]
    all_checked = True
    try:
        maket = Makety.objects.get(Q(maket_id=maket_id) & Q(order=ord_imp))
        maket.date_modified = datetime.date.today()
    except:
        maket = Makety(maket_id=maket_id, order=ord_imp, date_create=datetime.date.today(), order_num=ord_imp.order_id,
                       order_date=ord_imp.order_date, date_modified=datetime.date.today())
    maket.save()
    for pr_rg in product_range:
        prt = 'chck_' + pr_rg[2] + '_' + pr_rg[9]
        itemgroup = pr_rg[5]
        items_checked = []
        itm_checked = Item_imports.objects.filter(Q(item__print_group__code=itemgroup) & Q(order=ord_imp) & \
                                                  Q(print_name=pr_rg[10])).first()
        try:
            item_checked = Itemgroup_in_Maket.objects.get(
                Q(item=itm_checked) & Q(maket=maket) & Q(print_name=pr_rg[10]))
        except:
            item_checked = Itemgroup_in_Maket(item=itm_checked, maket=maket, print_name=pr_rg[10])
        try:
            sel_item = request.POST[prt]
            if sel_item == 'on':
                item_checked.checked = True
        except:
            item_checked.checked = False
            all_checked = False
        item_checked.maket = maket
        item_checked.save()
        items_checked.append(item_checked)  # ////
        ord_imp.maket_status = 'P'
    ord_imp.save()
    return HttpResponseRedirect(reverse('maket_layout:maket_print_empty', args=[id, maket_id]))


