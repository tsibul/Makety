import os
from django.db.models import Q, F
from maket.models import Print_position, Print_place, Print_color, Item_imports, Order_imports, Print_imports, \
    Additional_Files, Makety, Print_group, Films, Customer, Customer_groups, Customer_types, Item_color, Detail_set, \
    Print_in_Maket, Itemgroup_in_Maket


def count_errors():
    lost_imports_len = Item_imports.objects.filter(item=None).count()
    lost_deleted_len = Item_imports.objects.filter(order=None).count() + Print_imports.objects.filter(item=None).count()
    print_colors = list(Print_color.objects.values_list('print_item_id', flat=True))
    lost_colors_len = Print_imports.objects.filter(Q(print_place__isnull=True) |
                                                   ~Q(id__in=print_colors)).order_by('-place').count()
    changed_customers_len = Order_imports.objects.filter(~Q(customer__name=F('customer_name'))).count()
    lost_hex_len = Item_imports.objects.filter(Q(detail1_hex='') & ~Q(detail1_color='') |
                                               Q(detail2_hex='') & ~Q(detail2_color='') |
                                               Q(detail3_hex='') & ~Q(detail3_color='') |
                                               Q(detail4_hex='') & ~Q(detail4_color='') |
                                               Q(detail5_hex='') & ~Q(detail5_color='') |
                                               Q(detail6_hex='') & ~Q(detail6_color='')).count()
    lost_position_len = Print_imports.objects.filter(Q(print_position__isnull=True) |
                                                     ~Q(print_position__position_place=F('print_place')) |
                                                     ~Q(print_position__print_group=F('item__item__print_group'))).count()
    order_errors_len = Order_imports.objects.filter(to_check=True).order_by('-order_date', 'order_id').count()
    additional_files_len = Additional_Files.objects.filter(additional_file__isnull=True).count()
    err_len = lost_position_len + lost_deleted_len + lost_colors_len + changed_customers_len + \
              lost_hex_len + order_errors_len + additional_files_len

    maket_files_diff = len(os.listdir('files/makety')) - Makety.objects.filter(uploaded=True).count()
    order_files_diff = len(os.listdir('files/orders')) - Order_imports.objects.filter(order_upload=True).count()
    films_files_diff = len(os.listdir('files/films')) - Films.objects.filter(film_upload=True).count()
    patterns_files_diff = len(os.listdir('files/patterns')) - Print_group.objects.filter(~Q(pattern_file='')).count()
    additional_files_diff = len(os.listdir('files/additional')) - Additional_Files.objects.all().count() + \
        Additional_Files.objects.filter(additional_file__isnull=True).count()
    total_files_diff = maket_files_diff + order_files_diff + films_files_diff + patterns_files_diff + additional_files_diff

    context = {'lost_imports_len': lost_imports_len,
               'lost_deleted_len': lost_deleted_len, 'lost_colors_len': lost_colors_len,
               'changed_customers_len': changed_customers_len, 'lost_hex_len': lost_hex_len, 'lost_position_len':
               lost_position_len, 'err_len': err_len, 'order_errors_len': order_errors_len, 'maket_files_diff': maket_files_diff,
               'order_files_diff': order_files_diff, 'films_files_diff': films_files_diff,
               'patterns_files_diff': patterns_files_diff, 'additional_files_diff': additional_files_diff,
               'total_files_diff': total_files_diff, 'additional_files_len': additional_files_len}
    return context


def print_position_and_color_from_print_obj(place, prt_obj):
    try:
        print_position = Print_position.objects.get(
            Q(position_place=place) & Q(print_group=prt_obj.item.item.print_group))
    except:
        print_position = ''
    return print_position


def place_obj_from_place(place):
    if place != 'Стандартное ProEcoPen':
        print_place_tmp = place.split(' ')
    else:
        print_place_tmp = [place]
    try:
        place_obj = Print_place.objects.get(
            Q(detail_name__iexact=print_place_tmp[0]) & Q(place_name__iexact=print_place_tmp[1]))
    except:
        if len(print_place_tmp) == 1:
            place_obj = Print_place.objects.get(place_name__iexact=print_place_tmp[0])
        else:
            place_obj = Print_place.objects.get(place_name__iexact=print_place_tmp[1])
    return place_obj


def print_color_check(prt_obj):
    for n in range(int(prt_obj.colors)):
        print_color = Print_color(color_number_in_item=n+1, print_item=prt_obj)
        print_color.save()
    return


def look_up_cst(lookup):
    order = Order_imports.objects.filter(manager__manager__icontains=lookup)
    cst_id = []
    for ord in order:
        cst_id.append(ord.customer.id)
    customers = Customer.objects.filter(Q(name__icontains=lookup) | Q(address__icontains=lookup) | \
                                        Q(id__in=cst_id) | Q(customer_all__mail__icontains=lookup)).order_by('name')
    if len(customers) == 0:
        return  False
    cst_groups = Customer_groups.objects.all().order_by('group_name')
    cst_types = Customer_types.objects.all()
    context = {'navi': 'customers', 'page_obj': customers, 'active2': 'active', 'look_up': True, 'lookup': lookup,
               'customer_types': cst_types, 'customer_groups': cst_groups}
    context.update(count_errors())
    return context

def prn_name_errors(id):
    order = Order_imports.objects.get(id=id)
    items_list = list(Item_imports.objects.filter(order__id=id))
    prt_list = {}
    itm_list = {}
    for itm in items_list:
        if itm.item_group not in prt_list:
            prt_list[itm.item_group] = []
        if itm.print_name not in prt_list[itm.item_group]:
            prt_list[itm.item_group].append(str(itm.print_name))
        index_prt = itm.item_group + '_' + itm.print_name
        if index_prt not in itm_list:
            itm_list[index_prt] = []
        itm_list[index_prt].append(itm)

    prt_red = []
    for itm, pr_l in prt_list.items():
        if len(prt_list[itm]) > 1:
            min = prt_list[itm][0]
        for prt in pr_l:
            if (10 < len(prt) and prt[0:len(min) - 7] == min[0:len(min) - 7]) or \
                    (10 >= len(prt) < len(min) and prt[0:4] == min[0:4]):
                if prt != min:
                    if len(prt) < len(min):
                        prt_red.append([itm, prt, min])
                        min = prt
                    else:
                        prt_red.append([itm, min, prt])

    return


def order_imports(id):
    ord_i = id
    #    try:
    ord_imp = Order_imports.objects.get(pk=int(ord_i))
    #    except:
    #        ord_imp = Order_imports.objects.order_by('-order_date', '-id').first()
    order_id = ord_imp.id
    item_import = list(Item_imports.objects.filter(order=order_id).order_by('code'))

    print_import = ()
    for item in item_import:
        print_import = print_import + tuple(Print_imports.objects.filter(item=item))
    print_import = list(print_import)
    return [ord_imp, item_import, print_import]


def prt_imports(id, print_import, ord_imp, mk_id):
    context = {}
    order_id = id
    print_groups = Print_group.objects.all().order_by('code')
    prt_0 = []
    prt_0_ = []
    for print_item in print_import:
        item = print_item.item
        clr = item.detail1_color
        item_code = item.item_group
        item = Detail_set.objects.get(item_name=item_code)
        clr_sch = item.color_scheme
        clr_hex = Item_color.objects.get(color_scheme=clr_sch, color_id=clr)
        clr_hex = clr_hex.color_code
        pt_name = print_item.item.print_name
        colors = Print_color.objects.filter(print_item=print_item)
        positions = Print_position.objects.filter(Q(print_group=print_item.item.item.print_group) &\
                                                  Q(position_place=print_item.print_place))
        position_list = []
        for position in positions:
            position_list.append([position.orientation_id, (position.position_orientation).split(' ')[0]])
        colors_list = []
        for color in colors:
            colors_list.append(color.color_pantone)
        if print_item.type != 'Soft Touch':
            try:
                maket = Makety.objects.get(order=ord_imp, maket_id=mk_id)
                try:
                    pt = Print_in_Maket.objects.get(Q(maket=maket) & Q(print_item=print_item))
                    if pt.checked:
                        pt_0 = 1
                    else:
                        pt_0 = 0
                    prt_0_.append([print_item.id, clr_hex, clr, print_item.item.item.print_group.code, pt_0, pt.option, \
                                   pt_name.replace(' ', '_').replace(',', '').replace('+', '_'), colors_list])
                    prt_0.append([print_item, clr_hex, print_item.item.item.print_group.code, pt_0, pt.option, \
                                  pt_name.replace(' ', '_').replace(',', '').replace('+', '_'), colors_list, position_list])
                except:
                    prt_0_.append([print_item.id, clr_hex, clr, print_item.item.item.print_group.code, 0, 1, \
                                   pt_name.replace(' ', '_').replace(',', '').replace('+', '_'), colors_list])
                    prt_0.append([print_item, clr_hex, print_item.item.item.print_group.code, 0, 1, \
                                      pt_name.replace(' ', '_').replace(',', '').replace('+', '_'), colors_list, position_list])
            except:
                prt_0_.append([print_item.id, clr_hex, clr, print_item.item.item.print_group.code, 0, 1, \
                               pt_name.replace(' ', '_').replace(',', '').replace('+', '_'), colors_list])
                prt_0.append([print_item, clr_hex, print_item.item.item.print_group.code, 0, 1, \
                                  pt_name.replace(' ', '_').replace(',', '').replace('+', '_'), colors_list, position_list])

        context.update({'prt_0': prt_0})
        context.update({'prt_0_': prt_0_})
    product_range = []
    for print_group in print_groups:
        prt_nms = set(Item_imports.objects.filter(Q(item__print_group=print_group) &
                                                  Q(order=ord_imp)).values_list('print_name', flat=True))
        for prt_nm in prt_nms:
            items_prt = len(Item_imports.objects.filter(Q(order=order_id) & Q(item__print_group=print_group) &
                                                        Q(print_name=prt_nm)))
            len_prt = len(Print_imports.objects.filter(Q(item__order=order_id) & Q(item__item__print_group=print_group)
                                                       & Q(item__print_name=prt_nm)))
            if items_prt != 0:
                item_for_color = Item_imports.objects.filter(Q(order=order_id) & Q(item__print_group=print_group) & \
                                                        Q(print_name=prt_nm)).first()
                print_item_for_color = Print_imports.objects.filter(Q(item=item_for_color) & ~Q(type='Soft Touch'))
                list_for_count_colors = []
                for prt_item_for_color in print_item_for_color:
                    list_for_count_colors.append([prt_item_for_color.print_place.id, prt_item_for_color.place,
                                                  list(range(0, prt_item_for_color.colors))])
                try:
                    maket = Makety.objects.get(order=ord_imp, maket_id=mk_id)
                    itemgroup_in_maket = Itemgroup_in_Maket.objects.get(
                        Q(maket=maket) & Q(item__item__print_group=print_group)
                        & Q(item__print_name=prt_nm))
                    context.update({'maket': maket})
                    if itemgroup_in_maket.checked:
                        ig_ch = 1
                    else:
                        ig_ch = 0
                    product_range.append([print_group.name, len_prt, 'prt_' + print_group.code, items_prt,
                                          'maket/svg/svg' + print_group.code + '.html', print_group.code, ig_ch,
                                          print_group.options, print_group.layout,
                                          prt_nm.replace(' ', '_').replace(',', '').replace('+', '_'), prt_nm,
                                          list_for_count_colors])
                except:
                    product_range.append([print_group.name, len_prt, 'prt_' + print_group.code, items_prt,
                                          'maket/svg/svg' + print_group.code + '.html', print_group.code, 1,
                                          print_group.options, print_group.layout,
                                          prt_nm.replace(' ', '_').replace(',', '').replace('+', '_'), prt_nm,
                                          list_for_count_colors])

    context.update({'print_groups': print_groups})
    return [context, product_range]
