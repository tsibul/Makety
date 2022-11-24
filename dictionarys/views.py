from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from maket.models import Color_scheme, Print_type, Print_place, Print_position, Item_color, Detail_set, Customer, \
    Print_group

from maket.views import count_errors


def other(request):
    navi = 'dicts'
    color_scheme = Color_scheme.objects.all()

    print_type = Print_type.objects.all()
    print_place = Print_place.objects.all().order_by('detail_name', 'place_name')
    print_group = Print_group.objects.all().order_by('code')
    print_position = Print_position.objects.all().order_by('print_group')

    context = {'navi': navi, 'color_scheme': color_scheme, 'print_type': print_type, 'print_place': print_place,
               'print_position': print_position, 'active2': 'active', 'print_group': print_group}
    context.update(count_errors())
    return render(request, 'dictionarys/other.html', context)


def print_position(request):
    navi = 'dicts'
    print_place = Print_place.objects.all().order_by('detail_name', 'place_name')
    print_group = Print_group.objects.all().order_by('code')
    print_position = Print_position.objects.all().order_by('print_group', 'position_place', 'orientation_id')

    context = {'navi': navi,  'print_place': print_place,
               'print_position': print_position, 'active2': 'active', 'print_group': print_group}
    context.update(count_errors())
    return render(request, 'dictionarys/print_position.html', context)


def print_group(request):
    navi = 'print_group'
    print_group = Print_group.objects.all().order_by('code')
    first = print_group.first()
    scale = round(first.item_width / first.item_width_initial * 100, 3)
    context = {'navi': navi, 'active2': 'active', 'print_group': print_group, 'scale': scale}
    context.update(count_errors())
    return render(request, 'dictionarys/print_group.html', context)


def colors(request):
    navi = 'colors'
    color = Item_color.objects.all().order_by('-color_scheme', 'color_id')
    color_scheme = Color_scheme.objects.all()
    context = {'navi': navi, 'color': color, 'active2': 'active', 'color_scheme': color_scheme}
    context.update(count_errors())
    return render(request, 'dictionarys/colors.html', context)


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


def customers(request):
    navi = 'customers'
    customers = Customer.objects.all().order_by('name')

    context = {'navi': navi, 'customers': customers, 'active2': 'active'}
    context.update(count_errors())
    return render(request, 'dictionarys/customers.html', context)


def update_cst(request, id):
    cst = Customer.objects.get(id=id)
    nm = request.POST['nm']
    gr = request.POST['gr']
    tp = request.POST['tp']
    rg = request.POST['rg']
    in_ = request.POST['in_']
    ad = request.POST['ad']
    cst.name = nm
    cst.group = gr
    cst.type = tp
    cst.region = rg
    cst.inn = in_
    cst.address = ad
    cst.save()
    return HttpResponseRedirect(reverse('dictionarys:customers'))


def add_detail(request):
    item_code = request.POST['dt_it_art']
    name = request.POST['dt_it_nm']
    cs = request.POST['dt_it_clr']
    pg = request.POST['dt_it_pg']
    try:
        color_scheme = Color_scheme.objects.get(scheme_name=cs)
    except:
        color_scheme = None
    try:
        print_group = Print_group.objects.get(code=pg)
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

    det_set = Detail_set(item_name=item_code, name=name, color_scheme=color_scheme, print_group=print_group,
                         detail1_name=detail1_name, detail1_place=detail1_place,
                         detail2_name=detail2_name, detail2_place=detail2_place,
                         detail3_name=detail3_name, detail3_place=detail3_place,
                         detail4_name=detail4_name, detail4_place=detail4_place,
                         detail5_name=detail5_name, detail5_place=detail5_place,
                         detail6_name=detail6_name, detail6_place=detail6_place)
    det_set.save()
    return HttpResponseRedirect(reverse('dictionarys:goods'))


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


def goods(request):
    navi = 'customers'
    goods = Detail_set.objects.all().order_by('item_name')
    clr_scheme = Color_scheme.objects.all()
    color_scheme = []
    for clr in clr_scheme:
        color_scheme.append(clr.scheme_name)
    print_group = []
    prt_group = Print_group.objects.all()
    for prt in prt_group:
        print_group.append(prt.code)

    context = {'navi': navi, 'goods': goods, 'active2': 'active', 'color_scheme': color_scheme,
               'print_group': print_group}
    context.update(count_errors())
    return render(request, 'dictionarys/goods.html', context)


def upd_goods(request, id):
    item = Detail_set.objects.get(id=id)
    item_code = request.POST['art']
    item.item_name = item_code
    item_name = request.POST['nm']
    item.name = item_name
    item_clr = request.POST['ColorSelect']
    if item_clr != 'None':
        item.color_scheme = Color_scheme.objects.get(scheme_name=item_clr)
    prt_group = request.POST['PrtSelect']
    if prt_group != 'None':
        item.print_group = Print_group.objects.get(code=prt_group)
    detail1_name = request.POST['dt1']
    item.detail1_name = detail1_name
    try:
        detail1_place = request.POST['dt1_chck']
    except:
        detail1_place = False
    item.detail1_place = detail1_place
    detail2_name = request.POST['dt2']
    item.detail2_name = detail2_name
    try:
        detail2_place = request.POST['dt2_chck']
    except:
        detail2_place = False
    item.detail2_place = detail2_place
    detail3_name = request.POST['dt3']
    item.detail3_name = detail3_name
    try:
        detail3_place = request.POST['dt3_chck']
    except:
        detail3_place = False
    item.detail3_place = detail3_place
    detail4_name = request.POST['dt4']
    item.detail4_name = detail4_name
    try:
        detail4_place = request.POST['dt4_chck']
    except:
        detail4_place = False
    item.detail4_place = detail4_place
    detail5_name = request.POST['dt5']
    item.detail5_name = detail5_name
    try:
        detail5_place = request.POST['dt5_chck']
    except:
        detail5_place = False
    item.detail5_place = detail5_place
    detail6_name = request.POST['dt6']
    item.detail6_name = detail6_name
    try:
        detail6_place = request.POST['dt6_chck']
    except:
        detail6_place = False
    item.detail6_place = detail6_place
    item.save()
    return HttpResponseRedirect(reverse('dictionarys:goods'))


def upd_pg(request, id):
    pg = Print_group.objects.get(id=id)
    cd = request.POST['pg_cd']
    pg.code = cd
    nm = request.POST['pg_nm']
    pg.name = nm
    op = request.POST['pg_op']
    pg.options = op
    ly = request.POST['pg_ly']
    pg.layout = ly
    width = request.POST['pg_width']
    pg.item_width = width
    height = request.POST['pg_height']
    pg.item_height = height
    width_initial = request.POST['pg_width_initial']
    pg.item_width_initial = width_initial
    height_initial = request.POST['pg_height_initial']
    pg.item_height_initial = height_initial
    pg.save()
    return HttpResponseRedirect(reverse('dictionarys:print_group'))


def add_pg(request):
    cd = request.POST['cd']
    nm = request.POST['pg']
    op = request.POST['op']
    ly = request.POST['ly']
    width = request.POST['width']
    height = request.POST['height']
    width_initial = request.POST['width_initial']
    height_initial = request.POST['height_initial']
    pg = Print_group(code=cd, name=nm, layout=ly, options=op, item_width=width, item_height=height,
                     item_width_initial=width_initial, item_height_initial=height_initial)
    pg.save()
    return HttpResponseRedirect(reverse('dictionarys:print_group'))


def delete_print_place(request, id):
    print_place = Print_place.objects.get(id=id)
    print_place.delete()
    return HttpResponseRedirect(reverse('dictionarys:other'))


def delete_print_position(request, id):
    print_position = Print_position.objects.get(id=id)
    print_position.delete()
    return HttpResponseRedirect(reverse('dictionarys:print_position'))
