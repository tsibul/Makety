# Create your views here.
import csv
import datetime
import os

from bs4 import BeautifulSoup
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .models import Color_scheme, Print_type, Print_place, Print_position, Item_color, Order_imports, Item_imports, \
    Print_imports, Detail_set, Customer, Manger, Makety, Films, Item_in_Film, Itemgroup_in_Maket, Print_group, Print_in_Maket


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
    try:
        order_id = ord_imp.id
        item_import = list(Item_imports.objects.filter(order=order_id).order_by('code'))
        print_import = ()
        for item in item_import:
            print_import = print_import + tuple(Print_imports.objects.filter(item=item))
        print_import = list(print_import)
    except:
        pass

    try:
        orders = Order_imports.objects.all().order_by('-order_date', '-id')
        context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
               'orders': orders, 'active1': 'active'}
    except:
        context = {'navi': navi}
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

    context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
               'orders': orders, 'active1': 'active'}
    return render(request, 'maket/index.html', context)


def dicts(request):
    navi = 'dicts'
    color_scheme = Color_scheme.objects.all()
    color = Item_color.objects.all().order_by('-color_scheme', 'color_id')

    print_type = Print_type.objects.all()
    print_place = Print_place.objects.all()
    print_position = Print_position.objects.all()
    print_group = Print_group.objects.all()

    context = {'navi': navi, 'color_scheme': color_scheme, 'print_type': print_type, 'print_place': print_place,
               'print_position': print_position, 'color': color, 'active2': 'active', 'print_group': print_group}
    return render(request, 'maket/dicts.html', context)


def admin(request):
    navi = 'admin'
    context = {'navi': navi, 'active4': 'active'}
    return render(request, 'maket/admin.html', context)

def maket_base(request):
    navi = 'maket_base'
    context = {'navi': navi, 'active5': 'active'}
    return render(request, 'maket/maket_base.html', context)


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

    context = {'navi': navi, 'customers': customers, 'active3': 'active'}
    return render(request, 'maket/customers.html', context)


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
    return HttpResponseRedirect(reverse('maket:customers'))


def import_order(request):
    try:
        os.remove('tmp_file')
    except:
        pass
    file = request.FILES['Chosen']
    file_name = default_storage.save('tmp_file', file)
    tmp = open('tmp_file', 'r', encoding="utf-8")
    demo = tmp.read()
    souphtml = BeautifulSoup(demo, "html.parser")
    souptr = souphtml.find_all("tr")
    trstrings = []
    for tr in souptr:
        tmptr = tr.contents
        tmpstrings = []
        for td in tmptr:
            try:
                tmptd = td.contents[0]
                if tmptd != '':
                    tmpstrings.append(tmptd)
            except:
                pass
        if tmpstrings != []:
            trstrings.append(tmpstrings)

    number_tr = len(trstrings)
    order_no = str(trstrings[2][0])
    order_date = trstrings[1][0]
    order_date = datetime.datetime.strptime(order_date, '%d.%m.%Y').date()
    supplier = str(trstrings[4][0])
    customer_name = str(trstrings[6][0])
    customer_inn = str(trstrings[7][0])
    customer_address = str(trstrings[8][0])
    order_quantity = str(trstrings[10][0])
    ord_sum = str(trstrings[12][0])
    order_sum = ord_sum.replace(',', '.')
    our_manager = str(trstrings[13][0])
#    our_manager_phone = str(trstrings[14][0])
    customer_manager = str(trstrings[15][0])
    customer_manager_phone = str(trstrings[17][0])
    customer_manager_mail = str(trstrings[16][0])
    if customer_manager_mail != '' and customer_manager_mail != '\xa0':
        try:
            imp_manager = Manger.orders.get(manager_mail=customer_manager_mail)
            if imp_manager.manager == customer_manager:
                customer_manager = imp_manager
            else:
                cust_manager = Manger(manager=customer_manager, manager_phone=customer_manager_phone,
                                      manager_mail=customer_manager_mail)
        except:
            cust_manager = Manger(manager=customer_manager, manager_phone=customer_manager_phone,
                                  manager_mail=customer_manager_mail)
    else:
        cust_manager = Manger(manager=customer_manager, manager_phone=customer_manager_phone)
    cust_manager.save()
    ord_imp = Order_imports(order_id=order_no, supplier=supplier, customer_name=customer_name,
                            customer_INN=customer_inn, customer_address=customer_address, order_date=order_date,
                            order_quantity=order_quantity, order_sum=order_sum, our_manager=our_manager,
                            manager=cust_manager)
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
            type = 'Агентство'
        elif type == 'Р':
            type = 'Рекламщик'
        elif type == 'К':
            type = 'Конечник'
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
        ord_imp.customer = customer
    try:
        orderbase = Order_imports.objects.get(order_id=order_no)
        orderbase.order_id = ord_imp.order_id
        orderbase.customer_name = ord_imp.customer_name
        orderbase.customer_INN = ord_imp.customer_INN
        orderbase.customer_address = ord_imp.customer_address
        orderbase.order_date = ord_imp.order_date
        orderbase.customer = ord_imp.customer
        orderbase.order_quantity = ord_imp.order_quantity
        orderbase.order_sum = ord_imp.order_sum
        orderbase.our_manager = ord_imp.our_manager
        orderbase.customer_manager = ord_imp.customer_manager
        orderbase.customer_manager_phone = ord_imp.customer_manager_phone
        orderbase.customer_manager_mail = ord_imp.customer_manager_mail
        orderbase.save()
        ord_imp = orderbase
    except:
        ord_imp.save()
#    order = []
#    try:
#        pk = ord_imp.id
#    except:
#        pk = orderbase.id
    order_body = range(19, number_tr, 1)
    items_list = []
    print_list = []
#    j = 0
    for i in order_body:
        tr_len = len(trstrings[i])
        if trstrings[i][tr_len-1] == '1sec_endofline' and trstrings[i][3] != '\xa0':
            itm_clr = trstrings[i][2].split('.')
            itm_group = itm_clr[0]
            itm_clr.pop(0)
            clr = '.'.join(itm_clr)
            num_details = len(itm_clr)
            x = range(num_details)
            item = Item_imports(print_id=trstrings[i][0], code=trstrings[i][2], name=trstrings[i][1],
                                quantity=trstrings[i][4], print_name=trstrings[i][3], order=ord_imp,
                                item_group=itm_group, item_color=clr)
            try:
                itm_obj = Detail_set.objects.get(item_name=itm_group)
                item.item = itm_obj
            except:
                pass

            # TODO check if order exists, if no print_name, if no print details
            for n in x:
                detail = 'detail' + str(n + 1) + '_color'
                setattr(item, detail, itm_clr[n])
            item.save()
            items_list.append(item)
        elif trstrings[i][tr_len-1] == '2 sec_endofline':
            for x in items_list:
                if x.name == trstrings[i][1]:
                    prt_item = x
            if trstrings[i][0] != '':
                print_id = prt_item.print_id
            if tr_len == 9:
                place = trstrings[i][3]
                type = trstrings[i][4]
                colors = trstrings[i][5]
                itm_price = trstrings[i][2].split(',')
                if itm_price != ['\xa0']:
                    try:
                        item_price = float(itm_price[0])+int(itm_price[1])/10
                    except:
                        item_price = float(itm_price[0])
                    itm_for_price = Item_imports.objects.get(id=prt_item.id)
                    itm_for_price.item_price = item_price
                    itm_for_price.save()
                prt_price = trstrings[i][7].split(',')
                try:
                    print_price = float(prt_price[0])+int(prt_price[1])/10
                except:
                    print_price = float(prt_price[0])
                if trstrings[i][6] == '-':
                    second_pass = False
                else:
                    second_pass = True

            print_item = Print_imports(place=place, type=type, colors=colors, item=prt_item, print_id=print_id,
                                       second_pass=second_pass, print_price=print_price)
            print_item.save()
            print_list.append([place, type, colors, second_pass, print_item, print_id])
    itms_for_price = Item_imports.objects.filter(order=ord_imp)
    gross_prt_quantity = 0
    gross_prt_price = 0
    for itm in itms_for_price:
        prts_for_price = Print_imports.objects.filter(item=itm)
        prt_price = 0.0
        prt_quantity = len(prts_for_price)
        for prt in prts_for_price:
            prt_price = prt_price + prt.print_price
        gross_prt_quantity = gross_prt_quantity + prt_quantity * itm.quantity
        gross_prt_price = gross_prt_price + prt_price * itm.quantity
        itm.print_price = prt_price
        itm.num_prints = prt_quantity
        itm.save()
    ord_imp.print_quantity = gross_prt_quantity
    ord_imp.print_sum = gross_prt_price
    ord_imp.save()
    return HttpResponseRedirect(reverse('maket:index'))


def import_csv_order(request):
    try:
        os.remove('tmp_file')
    except:
        pass
    file = request.FILES['Chosen']
    file_name = default_storage.save('tmp_file', file)

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
            type = 'Агентство'
        elif type == 'Р':
            type = 'Рекламщик'
        elif type == 'К':
            type = 'Конечник'
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
#    order = []
#    pk = ord_imp.id
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

            # TODO check if order exists, if no print_name, if no print details
            for n in x:
                detail = 'detail' + str(n + 1) + '_color'
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
    return HttpResponseRedirect(reverse('maket:index'))


def delete_order(request, id):
    order_d = Order_imports.objects.get(id=id)
    order_d.delete()
    return HttpResponseRedirect(reverse('maket:index'))


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

    det_set = Detail_set(item_name=item_code, name=name, color_scheme=color_scheme, print_group=print_group,
                         detail1_name=detail1_name, detail1_place=detail1_place,
                         detail2_name=detail2_name, detail2_place=detail2_place,
                         detail3_name=detail3_name, detail3_place=detail3_place,
                         detail4_name=detail4_name, detail4_place=detail4_place,
                         detail5_name=detail5_name, detail5_place=detail5_place)
    det_set.save()
    return HttpResponseRedirect(reverse('maket:goods'))


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


def order_imports(id):
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
    return [ord_imp, item_import, print_import]


def prt_imports(id, print_import):
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
        prt_0_.append([print_item.id, clr_hex, clr, print_item.item.item.print_group.code])
        prt_0.append([print_item, clr_hex, print_item.item.item.print_group.code])
        context.update({'prt_0': prt_0})
        context.update({'prt_0_': prt_0_})
    product_range = []
    for print_group in print_groups:
        items_prt = len(Item_imports.objects.filter(Q(order=order_id) & Q(item__print_group=print_group)))
        len_prt = len(Print_imports.objects.filter(Q(item__order=order_id) & Q(item__item__print_group=print_group)))
        if items_prt != 0:
            product_range.append([print_group.name, len_prt, 'prt_' + print_group.code, items_prt,
                                  'maket/svg/svg' +print_group.code + '.html', print_group.code])
    context.update({'print_groups': print_groups})
    return [context, product_range]


def maket_print(request, id):
    ord_imp = order_imports(id)[0]
    item_import = order_imports(id)[1]
    print_import = order_imports(id)[2]
    context = {'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import}

    order_id = ord_imp.id
    product_range = prt_imports(order_id, print_import)[1]
    context_imp = prt_imports(order_id, print_import)[0]
    context.update({'product_range': product_range})
    context.update(context_imp)

    return render(request, 'maket/maket_print.html', context)


def update_maket(request, id):
    ord_imp = order_imports(id)[0]
    item_import = order_imports(id)[1]
    print_import = order_imports(id)[2]
    order_id = ord_imp.id
    product_range = prt_imports(order_id, print_import)[1]
    maket_id = request.POST['maket_id']
    all_checked = True
    try:
        maket = Makety.objects.get(Q(maket_id=maket_id) & Q(order=ord_imp))
        maket.date_modified = datetime.date.today()
    except:
        maket = Makety(maket_id=maket_id, order=ord_imp, date_create=datetime.date.today(), order_num=ord_imp.order_id,
                       order_date=ord_imp.order_date, date_modified=datetime.date.today())
    maket.save()
    for pr_rg in product_range:
        prt = 'chck_' + pr_rg[5]
        itemgroup = pr_rg[5]
        for item in item_import:
            if itemgroup == item.item.print_group.code:
                print_name = item.print_name
                break
        itemgroup = Detail_set.objects.filter(print_group__code=itemgroup).first()
        try:
            item_checked = Itemgroup_in_Maket.objects.get(item=itemgroup)
        except:
            item_checked = Itemgroup_in_Maket(item=itemgroup)
        item_checked.print_name = print_name
        try:
            sel_item = request.POST[prt]
            if sel_item == 'on':
                item_checked.checked = True
        except:
            item_checked.checked = False
            all_checked = False
        item_checked.maket = maket
        item_checked.save()

    if all_checked:
        ord_imp.maket_status = 'R'
    else:
        ord_imp.maket_status = 'P'
    ord_imp.save()
    return HttpResponseRedirect(reverse('maket:maket_print', args=[id]))


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

    context = {'navi': navi, 'goods': goods, 'active6': 'active', 'color_scheme': color_scheme, 'print_group': print_group}
    return render(request, 'maket/goods.html', context)

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
    item.save()
    return HttpResponseRedirect(reverse('maket:goods'))


def upd_pg(request, id):
    pg = Print_group.objects.get(id=id)
    cd = request.POST['pg_cd']
    pg.code = cd
    nm = request.POST['pg_nm']
    pg.name = nm
    ly = request.POST['pg_ly']
    pg.layout = ly
    pg.save()
    return HttpResponseRedirect(reverse('maket:dicts'))

def add_pg(request):
    cd = request.POST['cd']
    nm = request.POST['pg']
    ly = request.POST['ly']
    pg = Print_group(code=cd, name=nm, layout=ly)
    pg.save()
    return HttpResponseRedirect(reverse('maket:dicts'))
