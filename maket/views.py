from django.shortcuts import render

from django.db import models
from django.utils import timezone
# Create your views here.
import datetime
from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Color_scheme, Print_type, Print_place, Print_position, Item_color, Order_imports, Item_imports,\
    Print_imports, Detail_set, Customer
from django.db.models.lookups import GreaterThan, LessThan
from django.db.models import Q
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.urls import reverse
from django.db import transaction
from django.core.files import File
from django.views.generic import ListView
import csv
from .forms import FileForm



def main_maket(request):
    template = loader.get_template('maket/main.html')
    return HttpResponse(template.render({}, request))


def index(request):
    navi = 'orders'
    try:
        ord_i = request.POST['ord_id']
        ord_imp = Order_imports.objects.get(pk=int(ord_i))
    except:
        ord_imp = Order_imports.objects.order_by('-order_date', '-id').first()
    order_id = ord_imp.id
    item_import = list(Item_imports.objects.filter(order=order_id).order_by('code'))
    print_import = ()
    for item in item_import:
        print_import = print_import + tuple(Print_imports.objects.filter(item=item))
    print_import = list(print_import)

    orders = Order_imports.objects.all().order_by('-order_date', '-id')

    context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import, 'orders': orders}
    return render(request, 'maket/index.html', context)

def reload(request, id):
    navi = 'orders'
    ord_i = id
    try:
        ord_imp = Order_imports.objects.get(pk=int(ord_i))
    except:
        ord_imp = Order_imports.objects.order_by('-order_date', '-id').first()
    order_id = ord_imp.id
    item_import = list(Item_imports.objects.filter(order=order_id).order_by('code'))
    print_import = ()
    for item in item_import:
        print_import = print_import + tuple(Print_imports.objects.filter(item=item))
    print_import = list(print_import)

    orders = Order_imports.objects.all().order_by('-order_date', '-id')

    context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import, 'orders': orders}
    return render(request, 'maket/index.html', context)

def dicts(request):
    navi = 'dicts'
    color_scheme = Color_scheme.objects.all()
    color = Item_color.objects.all().order_by('-color_scheme', 'color_id')

    print_type = Print_type.objects.all()
    print_place = Print_place.objects.all()
    print_position = Print_position.objects.all()
    details = Detail_set.objects.all().order_by('item_name')

    context = {'navi': navi, 'color_scheme': color_scheme, 'print_type': print_type, 'print_place': print_place,
               'print_position': print_position, 'details': details, 'color' :color}
    return render(request, 'maket/dicts.html', context)


def admin(request):
    navi = 'admin'
    context = {'navi': navi}
    return render(request, 'maket/index.html', context)


def maket(request):
    navi = 'maket'
    context = {'navi': navi}
    return render(request, 'maket/index.html', context)


def update_clr_sch(request, id):
    clr_sch = request.POST['clr_sch']
    color_scheme = Color_scheme.objects.get(id=id)
    color_scheme.scheme_name = clr_sch
    color_scheme.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def add_clr_sch(request):
    clr_sch = request.POST['clr_sch']
    color_scheme = Color_scheme(scheme_name=clr_sch)
    color_scheme.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def update_prt_typ(request, id):
    prt_typ = request.POST['prt_typ']
    print_type = Print_type.objects.get(id=id)
    print_type.type_name = prt_typ
    print_type.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def add_prt_typ(request):
    prt_typ = request.POST['prt_typ']
    print_type = Print_type(type_name=prt_typ)
    print_type.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def update_prt_plc(request, id):
    prt_det = request.POST['prt_det']
    prt_plc = request.POST['prt_plc']
    print_place = Print_place.objects.get(id=id)
    print_place.detail_name = prt_det
    print_place.place_name = prt_plc
    print_place.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def add_prt_plc(request):
    prt_det = request.POST['prt_det']
    prt_plc = request.POST['prt_plc']
    print_type = Print_place(detail_name=prt_det, place_name=prt_plc)
    print_type.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def update_prt_pos(request, id):
    pos_opt = request.POST['pos_opt']
    pos_orn = request.POST['pos_orn']
    print_position = Print_position.objects.get(id=id)
    print_position.position_option = pos_opt
    print_position.position_orientation = pos_orn
    print_position.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def add_prt_pos(request):
    pos_opt = request.POST['pos_opt']
    pos_orn = request.POST['pos_orn']
    print_position = Print_position(position_option=pos_opt, position_orientation=pos_orn)
    print_position.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def customers(request):
    navi = 'customers'
    customers = Customer.objects.all().order_by('name')

    context = {'navi': navi, 'customers':customers}
    return render(request, 'maket/customers.html', context)

def import_order(request):
    file_name = request.POST['Chosen']
    with open(file_name, newline='') as csvfile:
        soup = csv.reader(csvfile, delimiter=';')
        list_soup = list(soup)
    number_strings = len(list_soup)
    order_no = list_soup[0][2]
    order_date = list_soup[0][3]
    order_date = datetime.datetime.strptime(order_date, '%d.%m.%Y').date()
    supplier = list_soup[1][2]
    customer_name = list_soup[2][2]
    customer_inn = list_soup[2][5]
    customer_address = list_soup[2][8]
    ord_imp = Order_imports(order_id=order_no, supplier=supplier, customer_name=customer_name,
                            customer_INN=customer_inn, customer_address=customer_address, order_date=order_date)
    try:
        if customer_inn != '':
            customer = Customer.objects.get(inn=customer_inn)
            ord_imp.customer = customer
        elif customer_inn == '':
            customer = Customer.objects.get(name=customer_name)
            ord_imp.customer = customer
    except:
        region = customer_inn[slice(0, 2)]
        type = order_no[slice(13, 14)]
        type2 = order_no[slice(14, 15)]
        if type == 'Д':
            type = 'Дилер'
        elif type == 'А':
            type ='Агентство'
        elif type == 'Р':
            type ='Рекламщик'
        elif type == 'К':
            type ='Конечник'
        if type2 == 'М':
            type = type + ' Москва'
        elif type2 == 'Р':
            type = type + ' Регион'
        elif type2 == 'Т':
            type = 'Розничная точка'
        elif type2 == 'К':
            type = 'Экспорт'
        customer = Customer(name=customer_name, address=customer_address, inn=customer_inn, region=region,
                            type=type)
        customer.save()
    ord_imp.save()
    order = []
    pk = ord_imp.id
    order_body = range(3, number_strings, 1)
    items_list = []
    print_list = []
    j = 0
    for i in order_body:
        if list_soup[i][0] != '' and list_soup[i][16] == '' and list_soup[i][7] != '':
            itm_clr = list_soup[i][6].split('.')
            itm_group = itm_clr[0]
            itm_clr.pop(0)
            clr = '.'.join(itm_clr)
            num_details = len(itm_clr)
            x = range(num_details)
            item = Item_imports(print_id=list_soup[i][0], code=list_soup[i][6], name=list_soup[i][1],
                                quantity=list_soup[i][11], print_name=list_soup[i][7], order=ord_imp,
                                item_group=itm_group, item_color=clr)
            try:
                itm_obj = Detail_set.objects.get(item_name=itm_group)
                item.item = itm_obj
            except:
                itm_obj = ''

#TODO check if order exists, if no print_name, if no print details
            for n in x:
                detail = 'detail' + str(n+1) + '_color'
                setattr(item, detail, itm_clr[n])
            item.save()
            items_list.append(item)
        elif list_soup[i][0] != '' and list_soup[i][16] == '' and list_soup[i][7] == '':
            j = j + 1
        elif list_soup[i][16] != '':
            for x in items_list:
                if x.name == list_soup[i][1]:
                    prt_item = x
            if list_soup[i][0] != '':
                print_id = prt_item.print_id
            place = list_soup[i][10]
            type = list_soup[i][13]
            colors = list_soup[i][14]
            if list_soup[i][15] == '-':
                second_pass = False
            else:
                second_pass = True
            print_item = Print_imports(place=place, type=type, colors=colors, item=prt_item, print_id=print_id)
            print_item.save()
            print_list.append([place, type, colors, second_pass, print_item, print_id])
    number_items = len(items_list)
    number_prints = len(print_list)
#        for row in soup:
#            order.append(row)
    return HttpResponseRedirect(reverse('maket:index'), {'order': order})


def delete_order(request, id):
    order_d = Order_imports.objects.get(id=id)
    order_d.delete()
    return HttpResponseRedirect(reverse('maket:index'))


def add_detail(request):
    item_code = request.POST['dt_it_nm']
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

    det_set = Detail_set(item_name=item_code,
                         detail1_name=detail1_name, detail1_place=detail1_place,
                         detail2_name=detail2_name, detail2_place=detail2_place,
                         detail3_name= detail3_name, detail3_place=detail3_place,
                         detail4_name=detail4_name, detail4_place=detail4_place,
                         detail5_name=detail5_name, detail5_place=detail5_place)
    det_set.save()
    return HttpResponseRedirect(reverse('maket:dicts'))
# TODO change add_detail


def upd_detail(request, id):
    item = Detail_set.objects.get(id=id)
    item_code = request.POST['code']
    item.item_name = item_code
    item_name = request.POST['name']
    item.name = item_name
    item_clr = request.POST['ColorSelect']
    if item_clr != 'None':
        item.color_scheme = Color_scheme.objects.get(scheme_name=item_clr)

    detail1_name = request.POST['dt1_nm']
    item.detail1_name = detail1_name
    try:
        detail1_place = request.POST['flexCheck_det1_']
    except:
        detail1_place = False
    item.detail1_place = detail1_place

    detail2_name = request.POST['dt2_nm']
    if detail2_name != '':
        try:
            detail2_place = request.POST['flexCheck_det2_']
        except:
            detail2_place = False
    else:
        detail2_place = False
    item.detail2_name = detail2_name
    item.detail2_place = detail2_place

    detail3_name = request.POST['dt3_nm']
    if detail3_name != '':
        try:
            detail3_place = request.POST['flexCheck_det3_']
        except:
            detail3_place = False
    else:
        detail3_place = False
    item.detail3_name = detail3_name
    item.detail3_place = detail3_place

    detail4_name = request.POST['dt4_nm']
    if detail4_name != '':
        try:
            detail4_place = request.POST['flexCheck_det4_']
        except:
            detail4_place = False
    else:
        detail4_place = False
    item.detail4_name = detail4_name
    item.detail4_place = detail4_place

    detail5_name = request.POST['dt5_nm']
    if detail5_name != '':
        try:
            detail5_place = request.POST['flexCheck_det5_']
        except:
            detail5_place = False
    else:
        detail5_place = False
    item.detail5_name = detail5_name
    item.detail5_place = detail5_place
    item.save()
    return HttpResponseRedirect(reverse('maket:dicts'))


def add_clr(request):
    color_id = request.POST['clr_id']
    color_name = request.POST['clr_nm']
    color_code = request.POST['dt1_hex']
    pantone = request.POST['dt1_ptn']
    color_scheme = request.POST['ColorSelect_add']
    color_scheme = Color_scheme.objects.get(id=color_scheme)
    color = Item_color(color_id=color_id, color_name=color_name, pantone=pantone,
                       color_code=color_code, color_scheme=color_scheme)
    color.save()
    return HttpResponseRedirect(reverse('maket:dicts'))

def update_clr(request, id):
    color = Item_color.objects.get(id=id)
    color_id = request.POST['clrid']
    color.color_id = color_id
    color_name = request.POST['clr_nm']
    color.color_name = color_name
    color_code = request.POST['dt1_hex']
    color.color_code = color_code
    pantone = request.POST['dt1_ptn']
    color.pantone = pantone
    color_scheme = request.POST['ColorSelect2']
    color_scheme = Color_scheme.objects.get(scheme_name=color_scheme)
    color.color_scheme = color_scheme

    color.save()
    return HttpResponseRedirect(reverse('maket:dicts'))

def maket_print(request, id):
    ord_i = id
    try:
        ord_imp = Order_imports.objects.get(pk=int(ord_i))
    except:
        ord_imp = Order_imports.objects.order_by('-order_date', '-id').first()
    order_id = ord_imp.id
    item_import = list(Item_imports.objects.filter(order=order_id).order_by('code'))
    items_34 = len(Item_imports.objects.filter(Q(order=order_id) & (Q(item_group__icontains='34')|
                                                                    Q(item_group__icontains='350'))))
    items_37 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='37')))
    items_310 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='310')))
    items_311 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='311')))
    items_312 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='312')))
    items_3A6 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='3A6')))
    items_3A5 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='3A5')))
    items_3D5 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='3D5')))
    items_101 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='101')))
    items_102 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='102')))
    items_105 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='105')))
    items_115 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='115')))
    items_120 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='120')))
    items_121 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='121')))
    items_703 = len(Item_imports.objects.filter(Q(order=order_id) & Q(item_group__icontains='703')))
    items_701 = len(Item_imports.objects.filter(Q(order=order_id) & (Q(item_group__icontains='701')|
                 Q(item_group__icontains='702')|Q(item_group__icontains='711')|Q(item_group__icontains='712'))))

    print_import = ()
    for item in item_import:
        print_import = print_import + tuple(Print_imports.objects.filter(item=item))
    print_import = list(print_import)
    prt_34_ = []
    prt_310_ = []
    prt_311_ = []
    prt_312_ = []
    prt_3A6_ = []
    prt_3A5_ = []
    prt_3D5_ = []
    prt_37_ = []
    prt_101_ = []
    prt_701_ = []
    prt_703_ = []
    prt_102_ = []
    prt_105_ = []
    prt_115_ = []
    prt_120_ = []
    prt_121_ = []
    prt_34 = []
    prt_310 = []
    prt_311 = []
    prt_312 = []
    prt_3A6 = []
    prt_3A5 = []
    prt_3D5 = []
    prt_37 = []
    prt_101 = []
    prt_701 = []
    prt_703 = []
    prt_102 = []
    prt_105 = []
    prt_115 = []
    prt_120 = []
    prt_121 = []
    for print_item in print_import:
        item_id = print_item.print_id
        item = print_item.item
        clr = item.detail1_color
        item_code = item.item_group
        item = Detail_set.objects.get(item_name=item_code)
        clr_sch = item.color_scheme
        clr_hex = Item_color.objects.get(color_scheme=clr_sch, color_id=clr)
        clr_hex = clr_hex.color_code
        if '34' in item_code or '350' in item_code:
            prt_34_.append([print_item.id, clr_hex, clr])
            prt_34.append([print_item, clr_hex])
        elif '310' in item_code:
            prt_310_.append([print_item.id, clr_hex, clr])
            prt_310.append([print_item, clr_hex])
        elif '311' in item_code:
            prt_311_.append([print_item.id, clr_hex, clr])
            prt_311.append([print_item, clr_hex])
        elif '312' in item_code:
            prt_312_.append([print_item.id, clr_hex, clr])
            prt_312.append([print_item, clr_hex])
        elif '3A6' in item_code:
            prt_3A6_.append([print_item.id, clr_hex, clr])
            prt_3A6.append([print_item, clr_hex])
        elif '3A5' in item_code:
            prt_3A5_.append([print_item.id, clr_hex, clr])
            prt_3A5.append([print_item, clr_hex])
        elif '3D5' in item_code:
            prt_3D5_.append([print_item.id, clr_hex, clr])
            prt_3D5.append([print_item, clr_hex])
        elif '37' in item_code:
            prt_37_.append([print_item.id, clr_hex, clr])
            prt_37.append([print_item, clr_hex])
        elif '101' in item_code:
            prt_101_.append([print_item.id, clr_hex, clr])
            prt_101.append([print_item, clr_hex])
        elif '102' in item_code:
            prt_102_.append([print_item.id, clr_hex, clr])
            prt_102.append([print_item, clr_hex])
        elif '105' in item_code:
            prt_105_.append([print_item.id, clr_hex, clr])
            prt_105.append([print_item, clr_hex])
        elif '115' in item_code:
            prt_115_.append([print_item.id, clr_hex, clr])
            prt_115.append([print_item, clr_hex])
        elif '120' in item_code:
            prt_120_.append([print_item.id, clr_hex, clr])
            prt_120.append([print_item, clr_hex])
        elif '121' in item_code:
            prt_121_.append([print_item.id, clr_hex, clr])
            prt_121.append([print_item, clr_hex])
        elif '703' in item_code:
            prt_703_.append([print_item.id, clr_hex, clr])
            prt_703.append([print_item, clr_hex])
        elif ('701' in item_code) or ('702' in item_code) or ('711' in item_code) or ('712' in item_code):
            prt_701.append([print_item, clr_hex])
            prt_701_.append([print_item.id, clr_hex, clr])

    context = {'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import}
    product_range = []
    if len(prt_34) != 0:
        context.update({'prt_34': prt_34})
        context.update({'prt_34_': prt_34_})
        product_range.append(['ProEcoPen', len(prt_34), 'prt_34', items_34])
    if len(prt_310) != 0:
        context.update({'prt_310': prt_310})
        context.update({'prt_310_': prt_310_})
        product_range.append(['Зажим 65мм', len(prt_310), 'prt_310', items_310])
    if len(prt_311) != 0:
        context.update({'prt_311': prt_311})
        context.update({'prt_311_': prt_311_})
        product_range.append(['Зажим 105мм', len(prt_311), 'prt_311', items_311])
    if len(prt_312) != 0:
        context.update({'prt_312': prt_312})
        context.update({'prt_312_': prt_312_})
        product_range.append(['Зажим с ложкой', len(prt_312), 'prt_312', items_312])
    if len(prt_37) != 0:
        context.update({'prt_37': prt_37})
        context.update({'prt_37_': prt_37_})
        product_range.append(['Чехол', len(prt_37), 'prt_37', items_37])
    if len(prt_3A6) != 0:
        context.update({'prt_3A6': prt_3A6})
        context.update({'prt_3A6_': prt_3A6_})
        product_range.append(['Блокнот А6', len(prt_3A6), 'prt_3A6', items_3A6])
    if len(prt_3A5) != 0:
        context.update({'prt_3A5': prt_3A5})
        context.update({'prt_3A5_': prt_3A5_})
        product_range.append(['Блокнот А5', len(prt_3A5), 'prt_3A5', items_3A5])
    if len(prt_3D5) != 0:
        context.update({'prt_3D5': prt_3D5})
        context.update({'prt_3D5_': prt_3D5_})
        product_range.append(['Блокнот на дисках', len(prt_3D5), 'prt_3D5', items_3D5])
    if len(prt_101) != 0:
        context.update({'prt_101': prt_101})
        context.update({'prt_101_': prt_101_})
        product_range.append(['Автомат', len(prt_101), 'prt_101', items_101])
    if len(prt_102) != 0:
        context.update({'prt_102': prt_102})
        context.update({'prt_102_': prt_102_})
        product_range.append(['Эрроу', len(prt_102), 'prt_102', items_102])
    if len(prt_105) != 0:
        context.update({'prt_105': prt_105})
        context.update({'prt_105_': prt_105_})
        product_range.append(['Болид', len(prt_105), 'prt_105', items_105])
    if len(prt_115) != 0:
        context.update({'prt_115': prt_115})
        context.update({'prt_115_': prt_115_})
        product_range.append(['Прима', len(prt_115), 'prt_115', items_115])
    if len(prt_120) != 0:
        context.update({'prt_120': prt_120})
        context.update({'prt_120_': prt_120_})
        product_range.append(['Спот', len(prt_120), 'prt_120', items_120])
    if len(prt_121) != 0:
        context.update({'prt_121': prt_121})
        context.update({'prt_121_': prt_121_})
        product_range.append(['Спот Люкс', len(prt_121), 'prt_121', items_121])
    if len(prt_701) != 0:
        context.update({'prt_701': prt_701})
        context.update({'prt_701_': prt_701_})
        product_range.append(['Каролина', len(prt_701), 'prt_701', items_701])
    if len(prt_703) != 0:
        context.update({'prt_703': prt_703})
        context.update({'prt_703_': prt_703_})
        product_range.append(['Краваттоне', len(prt_703), 'prt_703',items_703])
    context.update({'product_range': product_range})

    return render(request, 'maket/maket_print.html', context)

