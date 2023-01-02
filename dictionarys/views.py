from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from maket.models import Color_scheme, Print_type, Print_place, Print_position, Item_color, Detail_set, Customer, \
    Print_group, Good_crm_type, Good_matrix_type, Customer_types, Customer_groups

from maket.views import count_errors
from decimal import Decimal


def goods(request):
    navi = 'customers'
    goods = Detail_set.objects.all().order_by('item_name')
    clr_scheme = Color_scheme.objects.all()
    goods_matrix = Good_matrix_type.objects.all()
    goods_crm = Good_crm_type.objects.all()
    color_scheme = []
    for clr in clr_scheme:
        color_scheme.append(clr.scheme_name)
    print_group = []
    prt_group = Print_group.objects.all()
    for prt in prt_group:
        print_group.append(prt.code)


    context = {'navi': navi, 'goods': goods, 'active2': 'active', 'color_scheme': color_scheme,
               'print_group': print_group, 'goods_matrix': goods_matrix, 'goods_crm': goods_crm}
    context.update(count_errors())
    return render(request, 'dictionarys/goods.html', context)


def add_detail(request):
    good_id = request.POST['dt_it_id']
    item_code = request.POST['dt_it_art']
    name = request.POST['dt_it_nm']
    cs = request.POST['dt_it_clr']
    pg = request.POST['dt_it_pg']
    eco = request.POST['eco']
    try:
        color_scheme = Color_scheme.objects.get(scheme_name=cs)
    except:
        color_scheme = None
    try:
        matrix_in = request.POST['matrix']
        matrix = Good_matrix_type.objects.get(id=matrix_in)
    except:
        matrix = None
    try:
        crm_in = request.POST['crm']
        crm = Good_crm_type.objects.get(id=crm_in)
    except:
        crm = None
    try:
        print_group = Print_group.objects.get(code=pg).order_by('code')
    except:
        print_group = None

    detail1_name = request.POST['dt1_nm']
    try:
        detail1_place = request.POST['flexCheck_det1']
    except:
        detail1_place = False

    detail2_name = request.POST['dt2_nm']
    if detail2_name != '':
        try:
            detail2_place = request.POST['flexCheck_det2']
        except:
            detail2_place = False
    else:
        detail2_place = False

    detail3_name = request.POST['dt3_nm']
    if detail3_name != '':
        try:
            detail3_place = request.POST['flexCheck_det3']
        except:
            detail3_place = False
    else:
        detail3_place = False

    detail4_name = request.POST['dt4_nm']
    if detail4_name != '':
        try:
            detail4_place = request.POST['flexCheck_det4']
        except:
            detail4_place = False
    else:
        detail4_place = False

    detail5_name = request.POST['dt5_nm']
    if detail5_name != '':
        try:
            detail5_place = request.POST['flexCheck_det5']
        except:
            detail5_place = False
    else:
        detail5_place = False

    detail6_name = request.POST['dt6_nm']
    if detail5_name != '':
        try:
            detail6_place = request.POST['flexCheck_det6']
        except:
            detail6_place = False
    else:
        detail6_place = False
    try:
        det_set = Detail_set.objects.get(id=good_id)
        det_set.item_name = item_code
        det_set.name = name
        det_set.color_scheme = color_scheme
        det_set.print_group = print_group
        det_set.eco = eco
        det_set.crm = crm
        det_set.matrix = matrix
        det_set.detail1_name = detail1_name
        det_set.detail1_place = detail1_place
        det_set.detail2_name = detail2_name
        det_set.detail2_place = detail2_place
        det_set.detail3_name = detail3_name
        det_set.detail3_place = detail3_place
        det_set.detail4_name = detail4_name
        det_set.detail4_place = detail4_place
        det_set.detail5_name = detail5_name
        det_set.detail5_place = detail5_place
        det_set.detail6_name = detail6_name
        det_set.detail6_place = detail6_place
    except:
        det_set = Detail_set(item_name=item_code, name=name, color_scheme=color_scheme, print_group=print_group,
                             eco=eco, crm=crm, matrix=matrix,
                             detail1_name=detail1_name, detail1_place=detail1_place,
                             detail2_name=detail2_name, detail2_place=detail2_place,
                             detail3_name=detail3_name, detail3_place=detail3_place,
                             detail4_name=detail4_name, detail4_place=detail4_place,
                             detail5_name=detail5_name, detail5_place=detail5_place,
                             detail6_name=detail6_name, detail6_place=detail6_place)
    det_set.save()
    return HttpResponseRedirect(reverse('dictionarys:goods'))


def customers(request):
    navi = 'customers'
    customers = Customer.objects.all().order_by('name')
    customer_types = Customer_types.objects.all()
    paginator = Paginator(customers, 25)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cst_range = []
    for i in range(page_obj.paginator.num_pages):
        page_obj2 = paginator.get_page(i + 1)
        try:
            cst_tmp = str(page_obj2.object_list[0])
            cst_range.append([i + 1, '> ' + cst_tmp])
        except:
            cst_range.append(['нет данных'])

    context = {'navi': navi, 'page_obj': page_obj, 'active2': 'active', 'customer_types': customer_types, 'cst_range': cst_range}
    context.update(count_errors())
    return render(request, 'dictionarys/customers.html', context)


def update_cst(request):
    cst_id = request.POST['id']
    cst = Customer.objects.get(id=cst_id)
    nm = request.POST['nm']
    gr_old = request.POST['gr_o']
    gr_id = request.POST['gr_id']
    gr = request.POST['gr']
    tp_old = request.POST['tp_o']
    rg = request.POST['rg']
    in_ = request.POST['in_']
    ad = request.POST['ad']
    try:
        tp = request.POST['tp']
        type = Customer_types.objects.get(id=tp)
        cst.customer_type = type
    except:
        pass
    if gr != '' or gr_id != '':
        try:
            group = Customer_groups.objects.get(id=gr_id)
        except:
            try:
                group = Customer_groups.objects.get(group_name=gr)
            except:
                group = Customer_groups(group_name=gr)
                try:
                    group.group_type = type
                except:
                    pass
                group.save()
        cst.customer_group = group
    cst.name = nm
    cst.group = gr_old
    cst.type = tp_old
    cst.region = rg
    cst.inn = in_
    cst.address = ad
    cst.save()
    return HttpResponseRedirect(reverse('dictionarys:customers'))


def customer_groups(request):
    navi = 'customers'
    cst_groups = Customer_groups.objects.all()
    context = {'navi': navi, 'active2': 'active', 'cst_groups': cst_groups}
    context.update(count_errors())
    return render(request, 'dictionarys/customer_groups.html', context)


def update_cst_group(request):
    return HttpResponseRedirect(reverse('dictionarys:customer_groups'))



def colors(request):
    navi = 'colors'
    color = Item_color.objects.all().order_by('-color_scheme', 'color_id')
    color_scheme = Color_scheme.objects.all()
    context = {'navi': navi, 'color': color, 'active2': 'active', 'color_scheme': color_scheme}
    context.update(count_errors())
    return render(request, 'dictionarys/colors.html', context)


def add_clr(request):
    color_id = request.POST['clr_id']
    color_name = request.POST['clr_nm']
    color_code = request.POST['dt1_hex']
    pantone = request.POST['dt1_ptn']
    color_scheme = request.POST['ColorSelect_add']
    color_scheme = Color_scheme.objects.get(id=color_scheme)
    try:
        id = request.POST['id_id']
        color = Item_color.objects.get(id=id)
        color.color_id = color_id
        color.color_name = color_name
        color.color_code = color_code
        color.pantone = pantone
        color.color_scheme = color_scheme
    except:
        color = Item_color(color_id=color_id, color_name=color_name, pantone=pantone,
                           color_code=color_code, color_scheme=color_scheme)
    color.save()
    return HttpResponseRedirect(reverse('dictionarys:colors'))


def print_group(request):
    navi = 'print_group'
    print_group = Print_group.objects.all().order_by('code')
    first = print_group.first()
    scale = round(first.item_width / first.item_width_initial * 100, 3)
    context = {'navi': navi, 'active2': 'active', 'print_group': print_group, 'scale': scale}
    context.update(count_errors())
    return render(request, 'dictionarys/print_group.html', context)


def update_pg(request):
    cd = request.POST['pg_cd']
    nm = request.POST['pg_nm']
    op = request.POST['pg_op']
    ly = request.POST['pg_ly']
    width = request.POST['pg_width']
    height = request.POST['pg_height']
    width_initial = request.POST['pg_width_initial']
    height_initial = request.POST['pg_height_initial']
    try:
        pg_id = request.POST['pg_id']
        pg = Print_group.objects.get(id=pg_id)
        pg.code = cd
        pg.name = nm
        pg.options = op
        pg.layout = ly
        pg.item_width = width
        pg.item_height = height
        pg.item_width_initial = width_initial
        pg.item_height_initial = height_initial
    except:
        pg = Print_group(code=cd, name=nm, layout=ly, options=op, item_width=width, item_height=height,
                         item_width_initial=width_initial, item_height_initial=height_initial)
    pg.save()
    return HttpResponseRedirect(reverse('dictionarys:print_group'))


def print_position(request):
    navi = 'dicts'
    print_place = Print_place.objects.all().order_by('detail_name', 'place_name')
    print_group = Print_group.objects.all().order_by('code')
    print_position = Print_position.objects.all().order_by('print_group', 'position_place', 'orientation_id')

    context = {'navi': navi,  'print_place': print_place,
               'print_position': print_position, 'active2': 'active', 'print_group': print_group}
    context.update(count_errors())
    return render(request, 'dictionarys/print_position.html', context)


def update_prt_pos(request, id):
    orientation_id = request.POST['pos_opt']
    pos_orn = request.POST['pos_orn']
    print_group_id = request.POST['print_group']
    print_place_id = request.POST['position_place']
    print_group = Print_group.objects.get(id=print_group_id)
    place = Print_place.objects.get(id=print_place_id)
    print_position = Print_position.objects.get(id=id)
    print_position.orientation_id = orientation_id
    print_position.position_orientation = pos_orn
    print_position.print_group = print_group
    print_position.position_place = place
    print_position.save()
    return HttpResponseRedirect(reverse('dictionarys:print_position'))


def add_prt_pos(request):
    orientation_id = request.POST['pos_opt']
    pos_orn = request.POST['pos_orn']
    print_place_id = request.POST['position_place']
    print_group_id = request.POST['print_group']
    print_group = Print_group.objects.get(id=print_group_id)
    place = Print_place.objects.get(id=print_place_id)
    print_position = Print_position(orientation_id=orientation_id, position_orientation=pos_orn, print_group=print_group,
                                    position_place=place)
    print_position.save()
    return HttpResponseRedirect(reverse('dictionarys:print_position'))


def delete_print_position(request, id):
    print_position = Print_position.objects.get(id=id)
    print_position.delete()
    return HttpResponseRedirect(reverse('dictionarys:print_position'))


def good_groups(request):
    navi = 'dicts'
    good_groups = Good_matrix_type.objects.all()
    good_crm_types = Good_crm_type.objects.all()
    context = {'navi': navi, 'active2': 'active', 'good_groups': good_groups, 'good_crm_types': good_crm_types}
    context.update(count_errors())
    return render(request, 'dictionarys/good_groups.html', context)


def update_matrix_type(request, id):
    matrix_type = request.POST['good_matrix']
    good_matrix = Good_matrix_type.objects.get(id=id)
    good_matrix.matrix_name = matrix_type
    good_matrix.save()
    return HttpResponseRedirect(reverse('dictionarys:good_groups'))


def add_matrix_type(request):
    matrix_type = request.POST['matrix_type']
    good_matrix = Good_matrix_type(matrix_name=matrix_type)
    good_matrix.save()
    return HttpResponseRedirect(reverse('dictionarys:good_groups'))


def delete_matrix_type(request, id):
    good_matrix = Good_matrix_type.objects.get(id=id)
    good_matrix.delete()
    return HttpResponseRedirect(reverse('dictionarys:good_groups'))


def update_crm_type(request, id):
    crm_type = request.POST['good_crm']
    good_crm = Good_crm_type.objects.get(id=id)
    good_crm.crm_name = crm_type
    good_crm.save()
    return HttpResponseRedirect(reverse('dictionarys:good_groups'))


def add_crm_type(request):
    crm_type = request.POST['crm_type']
    good_crm = Good_crm_type(crm_name=crm_type)
    good_crm.save()
    return HttpResponseRedirect(reverse('dictionarys:good_groups'))


def delete_crm_type(request, id):
    good_crm = Good_crm_type.objects.get(id=id)
    good_crm.delete()
    return HttpResponseRedirect(reverse('dictionarys:good_groups'))



def other(request):
    navi = 'dicts'
    color_scheme = Color_scheme.objects.all()

    print_type = Print_type.objects.all()
    print_place = Print_place.objects.all().order_by('detail_name', 'place_name')
    print_group = Print_group.objects.all().order_by('code')
    print_position = Print_position.objects.all().order_by('print_group')
    customer_types = Customer_types.objects.all()

    context = {'navi': navi, 'color_scheme': color_scheme, 'print_type': print_type, 'print_place': print_place,
               'print_position': print_position, 'active2': 'active', 'print_group': print_group,
               'customer_types': customer_types}
    context.update(count_errors())
    return render(request, 'dictionarys/other.html', context)


def update_clr_sch(request, id):
    clr_sch = request.POST['clr_sch']
    color_scheme = Color_scheme.objects.get(id=id)
    color_scheme.scheme_name = clr_sch
    color_scheme.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def add_clr_sch(request):
    clr_sch = request.POST['clr_sch']
    color_scheme = Color_scheme(scheme_name=clr_sch)
    color_scheme.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def update_prt_typ(request, id):
    prt_typ = request.POST['prt_typ']
    print_type = Print_type.objects.get(id=id)
    print_type.type_name = prt_typ
    print_type.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def add_prt_typ(request):
    prt_typ = request.POST['prt_typ']
    print_type = Print_type(type_name=prt_typ)
    print_type.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def update_prt_plc(request, id):
    prt_det = request.POST['prt_det']
    prt_plc = request.POST['prt_plc']
    print_place = Print_place.objects.get(id=id)
    print_place.detail_name = prt_det
    print_place.place_name = prt_plc
    print_place.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def add_prt_plc(request):
    prt_det = request.POST['prt_det']
    prt_plc = request.POST['prt_plc']
    print_type = Print_place(detail_name=prt_det, place_name=prt_plc)
    print_type.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def delete_print_place(request, id):
    print_place = Print_place.objects.get(id=id)
    print_place.delete()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def update_cst_type(request, id):
    type_name = request.POST['cst_typ']
    grp_dsc = request.POST['grp_dsc']
    code = request.POST['code']
    customer_type = Customer_types.objects.get(id=id)
    customer_type.type_name = type_name
    customer_type.group_discount = grp_dsc
    customer_type.code = code
    customer_type.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def add_cst_type(request):
    type_name = request.POST['cst_type']
    grp_dsc = request.POST['grp_dsc']
    code = request.POST['code']
    customer_type = Customer_types(type_name=type_name, group_discount=grp_dsc, code=code)
    customer_type.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def delete_cst_type(request, id):
    customer_type = Customer_types.objects.get(id=id)
    customer_type.save()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def scale(request):
    scale = Decimal((request.POST['scale'])) / 100
    print_group = Print_group.objects.all()
    for pg in print_group:
        pg.item_width = round(pg.item_width_initial * scale, 3)
        pg.item_height = round(pg.item_height_initial * scale, 3)
        pg.save()
    return HttpResponseRedirect(reverse('dictionarys:print_group'))



