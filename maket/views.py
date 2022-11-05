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
from django.core.paginator import Paginator
from django.http import FileResponse, Http404

from .models import Color_scheme, Print_type, Print_place, Print_position, Item_color, Order_imports, Item_imports, \
    Print_imports, Detail_set, Customer, Manger, Makety, Films, Item_in_Film, Itemgroup_in_Maket, Print_group, \
    Print_in_Maket, Additional_Files
from django.views.decorators.csrf import csrf_exempt


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
        f_maket2 = list(orders)
        paginator = Paginator(f_maket2, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        orders = list(page_obj.object_list)

        date_range = []
        for i in range(page_obj.paginator.num_pages):
            page_obj2 = paginator.get_page(i + 1)
            try:
                date_tmp = str(page_obj2.object_list[0])
                date_range.append([i + 1, 'до ' + date_tmp])
            except:
                date_range.append(['нет данных'])
        context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
                   'orders': orders, 'active1': 'active', 'page_obj': page_obj, 'date_range': date_range}

    except:
        context = {'navi': navi}

    return render(request, 'maket/index.html', context)


def reload(request, id_str):
    navi = 'orders'
    ord_i = id_str.split('_')[0]
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
    try:
        orders = Order_imports.objects.order_by('-order_date', '-id').filter(
            Q(order_id__icontains=id_str.split('_')[1]) | Q(customer__name__icontains=id_str.split('_')[1]))
        context = {'lookup': id_str.split('_')[1]}
    except:
        orders = Order_imports.objects.all().order_by('-order_date', '-id')
    f_maket2 = list(orders)
    paginator = Paginator(f_maket2, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    orders = list(page_obj.object_list)

    date_range = []
    for i in range(page_obj.paginator.num_pages):
        page_obj2 = paginator.get_page(i + 1)
        try:
            date_tmp = str(page_obj2.object_list[0])
            date_range.append([i + 1, 'до ' + date_tmp])
        except:
            date_range.append(['нет данных'])
    context.update({'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
                    'orders': orders, 'active1': 'active', 'page_obj': page_obj, 'date_range': date_range})

    return render(request, 'maket/index.html', context)


def dicts(request):
    navi = 'dicts'
    color_scheme = Color_scheme.objects.all()

    print_type = Print_type.objects.all()
    print_place = Print_place.objects.all().order_by('detail_name', 'place_name')
    print_group = Print_group.objects.all().order_by('code')
    print_position = Print_position.objects.all().order_by('print_group')

    context = {'navi': navi, 'color_scheme': color_scheme, 'print_type': print_type, 'print_place': print_place,
               'print_position': print_position, 'active2': 'active', 'print_group': print_group}
    return render(request, 'maket/dictionarys/dicts.html', context)


def print_position(request):
    navi = 'dicts'
    print_place = Print_place.objects.all().order_by('detail_name', 'place_name')
    print_group = Print_group.objects.all().order_by('code')
    print_position = Print_position.objects.all().order_by('print_group', 'position_place', 'orientation_id')

    context = {'navi': navi,  'print_place': print_place,
               'print_position': print_position, 'active2': 'active', 'print_group': print_group}
    return render(request, 'maket/dictionarys/print_position.html', context)


def print_group(request):
    navi = 'print_group'
    print_group = Print_group.objects.all().order_by('code')
    context = {'navi': navi, 'active2': 'active', 'print_group': print_group}
    return render(request, 'maket/dictionarys//print_group.html', context)


def colors(request):
    navi = 'colors'
    color = Item_color.objects.all().order_by('-color_scheme', 'color_id')
    color_scheme = Color_scheme.objects.all()
    context = {'navi': navi, 'color': color, 'active2': 'active', 'color_scheme': color_scheme}
    return render(request, 'maket/dictionarys/colors.html', context)


def admin(request):
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

    lost_makets = []
    l_makets = Makety.objects.filter(order=None).order_by('-order_date')
    for l_mak in l_makets:
        try:
            l_order = Order_imports.objects.get(Q(order_id=l_mak.order_num) & Q(order_date=l_mak.order_date))
            lost_makets.append([l_mak, l_order])
        except:
            lost_makets.append([l_mak, ])
    lost_makets_len = len(lost_makets)

    items = list(Item_imports.objects.filter(Q(detail1_hex='') & ~Q(detail1_color='') | \
                                        Q(detail2_hex='') & ~Q(detail2_color='') | \
                                        Q(detail3_hex='') & ~Q(detail3_color='') | \
                                        Q(detail4_hex='') & ~Q(detail4_color='') | \
                                        Q(detail5_hex='') & ~Q(detail5_color='') | \
                                        Q(detail6_hex='') & ~Q(detail6_color='')))
    lost_hex_len = len(items)

    orders = Order_imports.objects.all().order_by('-order_date')
    changed_customers = []
    for order in orders:
        if order.customer_name != order.customer.name:
            changed_customers.append(order)
    changed_customers_len = len(changed_customers)

    lost_deleted_items = list(Item_imports.objects.filter(order=None))
    lost_deleted_prints = list(Print_imports.objects.filter(item=None))


    context = {'navi': navi, 'active4': 'active', 'lost_imports': lost_imports, 'lost_imports_len': lost_imports_len,
               'lost_makets': lost_makets, 'lost_makets_len': lost_makets_len, 'lost_hex': items,
               'lost_hex_len': lost_hex_len, 'changed_customers': changed_customers,
               'changed_customers_len': changed_customers_len, 'lost_deleted_prints': lost_deleted_prints,
               'lost_deleted_items': lost_deleted_items}
    print_objects = Print_imports.objects.filter(print_place__isnull=True).order_by('-place')
    context.update({'print_objects': print_objects})
    return render(request, 'maket/admin.html', context)


def changed_customers(request, id):
    order = Order_imports.objects.get(id=id)
    order.customer_name = order.customer.name
    order.save()
    return HttpResponseRedirect(reverse('maket:admin'))


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
    return HttpResponseRedirect(reverse('maket:admin'))


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
    return HttpResponseRedirect(reverse('maket:admin'))


def maket_base(request):
    navi = 'maket_base'
    maket = Makety.objects.all().order_by('-order_date', 'maket_id').filter(order__isnull=False)
    item_group = Itemgroup_in_Maket.objects.all().order_by('item')
    f_group = {}
    for i in item_group:
        if i.maket not in f_group:
            f_group[i.maket] = []
        if i.checked:
            ig_q = 0
            ig_p = 0
            ig_pp = 0
            try:
                itms = Item_imports.objects.filter(Q(order=i.maket.order) & Q(item__print_group=i.item.item.print_group) \
                                                   & Q(print_name=i.print_name))
                for it in itms:
                    ig_q = ig_q + it.quantity
                    ig_p = ig_p + it.quantity * it.item_price
                    ig_pp = ig_pp + it.quantity * it.print_price
                f_group[i.maket].append([i, ig_q, ig_p, ig_pp])
            except:
                pass
    f_maket = {}
    for m in maket:
        if m.order not in f_maket:
            f_maket[m.order] = {}
        f_maket[m.order].update({m: f_group.get(m)})

    films = Films.objects.filter(status=False).order_by('-date')
    current_date = datetime.date.today()
    try:
        last_film = films.first().film_id + 1
    except:
        last_film = 1

    f_maket2 = list(f_maket.items())
    paginator = Paginator(f_maket2, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    f_maket = dict(page_obj.object_list)

    date_range = []
    for i in range(page_obj.paginator.num_pages):
        page_obj2 = paginator.get_page(i + 1)
        try:
            date_tmp = str(page_obj2.object_list[0][0])
            date_range.append([i + 1, 'до ' + date_tmp])
        except:
            date_range.append(['нет данных'])

    context = {'navi': navi, 'active5': 'active', 'f_maket': f_maket, 'page_obj': page_obj, 'films': films,
               'current_date': current_date, 'last_film': last_film, 'date_range': date_range}
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
    return HttpResponseRedirect(reverse('maket:print_position'))


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
    return HttpResponseRedirect(reverse('maket:print_position'))


def customers(request):
    navi = 'customers'
    customers = Customer.objects.all().order_by('name')

    context = {'navi': navi, 'customers': customers, 'active2': 'active'}
    return render(request, 'maket/dictionarys/customers.html', context)


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
    try:
        ord_imp = Order_imports.objects.get(order_id=order_no)
        ord_imp.delete()
    except:
        pass
    ord_imp = Order_imports(order_id=order_no, supplier=supplier, customer_name=customer_name,
                            customer_INN=customer_inn, customer_address=customer_address, order_date=order_date,
                            order_quantity=order_quantity, order_sum=order_sum, our_manager=our_manager,
                                manager=cust_manager)
    try:
        if len(customer_inn) >= 10:
            customer = Customer.objects.get(inn=customer_inn)
            ord_imp.customer = customer
        elif len(customer_inn) <= 10:
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
    ord_imp.save()
    order_body = range(19, number_tr, 1)
    items_list = []
    print_list = []
    prnt_list = {}
    for i in order_body:
        tr_len = len(trstrings[i])
        if trstrings[i][tr_len - 1] == '1sec_endofline' and trstrings[i][3] != '\xa0':
            itm_clr = trstrings[i][2].split('.')
            itm_group = itm_clr[0]
            prt_name = trstrings[i][3]
            try:
                itm_obj = Detail_set.objects.get(item_name=itm_group)
            except:
                pass

            if len(prt_name) >= 16:
                pr_nm = prt_name[0: 12]
            elif 15 > len(prt_name) > 11:
                pr_nm = prt_name[0: 7]
            else:
                pr_nm = prt_name[0: 3]
            if itm_obj.print_group not in prnt_list:
                prnt_list[itm_obj.print_group] = []
            if len(prnt_list[itm_obj.print_group]) == 0:
                prnt_list[itm_obj.print_group].append(prt_name)
            else:
                tmp = False
                for pr in prnt_list[itm_obj.print_group]:
                    if pr.find(pr_nm) == 0:
                        prt_name = pr
                        tmp = True
                if not tmp:
                    prnt_list[itm_obj.print_group].append(prt_name)
                    tmp = False
            itm_clr.pop(0)
            clr = '.'.join(itm_clr)
            num_details = len(itm_clr)
            x = range(num_details)
            item = Item_imports(print_id=trstrings[i][0], code=trstrings[i][2], name=trstrings[i][1],
                                quantity=trstrings[i][4], print_name=prt_name, order=ord_imp,
                                item_group=itm_group, item_color=clr, item=itm_obj)
            # TODO check if no print_name, if no print details
            for n in x:
                detail = 'detail' + str(n + 1) + '_color'
                detail_hex = 'detail' + str(n + 1) + '_hex'
                setattr(item, detail, itm_clr[n])
                try:
                    hex_color = Item_color.objects.get(
                        Q(color_id=itm_clr[n]) & Q(color_scheme=item.item.color_scheme)).color_code
                    setattr(item, detail_hex, hex_color)
                except:
                    pass
            item.save()
            items_list.append(item)

        elif trstrings[i][tr_len - 1] == '2 sec_endofline':
            max_len = 0
            for v in prnt_list.values():
                if max_len < len(v):
                    max_len = len(v)
            if max_len == 1:
                for x in items_list:
                    if x.name == trstrings[i][1]:
                        prt_item = x
            elif items_list[len(items_list) - 1].print_id == str(len(items_list)):
                ord_imp.to_check = True
                for x in items_list:
                    if x.print_id == trstrings[i][0]:
                        prt_item = x
            else:
                ord_imp.to_check = True
                for x in items_list:
                    if x.name == trstrings[i][1]:
                        prt_item = x

            #            if trstrings[i][0] != '':
            #                print_id = prt_item.print_id
            if tr_len == 9:
                place = trstrings[i][3]
                type = trstrings[i][4]
                colors = trstrings[i][5]
                itm_price = trstrings[i][2].split(',')
                if itm_price != ['\xa0']:
                    try:
                        item_price = float(itm_price[0]) + int(itm_price[1]) / 10 ** len(itm_price[1])
                    except:
                        item_price = float(itm_price[0])
                    itm_for_price = Item_imports.objects.get(id=prt_item.id)
                    itm_for_price.item_price = item_price
                    itm_for_price.save()
                prt_price = trstrings[i][7].split(',')
                try:
                    print_price = float(prt_price[0]) + int(prt_price[1]) / 10 ** len(prt_price[1])
                except:
                    print_price = float(prt_price[0])
                if trstrings[i][6] == '-':
                    second_pass = False
                else:
                    second_pass = True
            place_obj = place_obj_from_place(place)
            print_item = Print_imports(place=place, type=type, colors=colors, item=prt_item, print_id=prt_item.print_id,
                                       second_pass=second_pass, print_price=print_price, print_place=place_obj)
            print_item.save()
            print_list.append([place, type, colors, second_pass, print_item, print_item.print_id])
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
    tmp = str(ord_imp.id) + '_'

    return HttpResponseRedirect(reverse('maket:reload2', kwargs={'id_str': tmp}))


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


def delete_order(request):
    id = request.POST['object_to_delete']
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
    return HttpResponseRedirect(reverse('maket:goods'))


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
    return HttpResponseRedirect(reverse('maket:colors'))


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
        try:
            maket = Makety.objects.get(order=ord_imp, maket_id=mk_id)
            try:
                pt = Print_in_Maket.objects.get(Q(maket=maket) & Q(print_item=print_item))
                if pt.checked:
                    pt_0 = 1
                else:
                    pt_0 = 0
                prt_0_.append([print_item.id, clr_hex, clr, print_item.item.item.print_group.code, pt_0, pt.option, \
                               pt_name.replace(' ', '_').replace(',', '').replace('+', '_')])
                prt_0.append([print_item, clr_hex, print_item.item.item.print_group.code, pt_0, pt.option, \
                              pt_name.replace(' ', '_').replace(',', '').replace('+', '_')])
            except:
                prt_0_.append([print_item.id, clr_hex, clr, print_item.item.item.print_group.code, 0, 1, \
                               pt_name.replace(' ', '_').replace(',', '').replace('+', '_')])
                prt_0.append([print_item, clr_hex, print_item.item.item.print_group.code, 0, 1, \
                              pt_name.replace(' ', '_').replace(',', '').replace('+', '_')])
        except:
            prt_0_.append([print_item.id, clr_hex, clr, print_item.item.item.print_group.code, 0, 1, \
                           pt_name.replace(' ', '_').replace(',', '').replace('+', '_')])
            prt_0.append([print_item, clr_hex, print_item.item.item.print_group.code, 0, 1, \
                          pt_name.replace(' ', '_').replace(',', '').replace('+', '_')])

        context.update({'prt_0': prt_0})
        context.update({'prt_0_': prt_0_})
    product_range = []
    for print_group in print_groups:
        prt_names = Item_imports.objects.filter(Q(item__print_group=print_group) & Q(order=ord_imp))
        prt_nms = []
        for prt_nm in prt_names:
            if prt_nm.print_name not in prt_nms:
                prt_nms.append(prt_nm.print_name)
        for prt_nm in prt_nms:
            items_prt = len(Item_imports.objects.filter(Q(order=order_id) & Q(item__print_group=print_group) & \
                                                        Q(print_name=prt_nm)))
            len_prt = len(Print_imports.objects.filter(Q(item__order=order_id) & Q(item__item__print_group=print_group) \
                                                       & Q(item__print_name=prt_nm)))
            if items_prt != 0:
                try:
                    maket = Makety.objects.get(order=ord_imp, maket_id=mk_id)
                    itemgroup_in_maket = Itemgroup_in_Maket.objects.get(
                        Q(maket=maket) & Q(item__item__print_group=print_group) \
                        & Q(item__print_name=prt_nm))
                    context.update({'maket': maket})
                    if itemgroup_in_maket.checked:
                        ig_ch = 1
                    else:
                        ig_ch = 0
                    product_range.append([print_group.name, len_prt, 'prt_' + print_group.code, items_prt,
                                          'maket/svg/svg' + print_group.code + '.html', print_group.code, ig_ch,
                                          print_group.options, print_group.layout,
                                          prt_nm.replace(' ', '_').replace(',', '').replace('+', '_'), prt_nm])
                except:
                    product_range.append([print_group.name, len_prt, 'prt_' + print_group.code, items_prt,
                                          'maket/svg/svg' + print_group.code + '.html', print_group.code, 1,
                                          print_group.options, print_group.layout,
                                          prt_nm.replace(' ', '_').replace(',', '').replace('+', '_'), prt_nm])

    context.update({'print_groups': print_groups})
    return [context, product_range]


def maket_print(request, id, mk_id):
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
    #    if len(maket_id_list) == 0:
    #       maket_id_list = [1]
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

    return render(request, 'maket/maket_print.html', context)


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
    #    if len(maket_id_list) == 0:
    #       maket_id_list = [1]
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

    return render(request, 'maket/maket_print_empty.html', context)


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
        #                print_name = item.print_name
        #                break
        #        itemgroup = Detail_set.objects.filter(print_group__code=itemgroup).first
        try:
            item_checked = Itemgroup_in_Maket.objects.get(
                Q(item=itm_checked) & Q(maket=maket) & Q(print_name=item.pr_rg[10]))
        except:
            item_checked = Itemgroup_in_Maket(item=itm_checked, maket=maket, print_name=pr_rg[10])
        #        item_checked.print_name = print_name
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
    if all_checked:
        ord_imp.maket_status = 'R'
    else:
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
        if pi.item.item.print_group.options > 1:
            pen_pos = 'pen_pos_' + str(pi.id)
            option = request.POST[pen_pos]
            pr_in_maket.option = option
        else:
            pr_in_maket.option = 0
        pr_in_maket.save()
    return HttpResponseRedirect(reverse('maket:maket_print', args=[id, maket_id]))


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
    return render(request, 'maket/dictionarys/goods.html', context)


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
    return HttpResponseRedirect(reverse('maket:goods'))


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
    pg.save()
    return HttpResponseRedirect(reverse('maket:print_group'))


def add_pg(request):
    cd = request.POST['cd']
    nm = request.POST['pg']
    op = request.POST['op']
    ly = request.POST['ly']
    pg = Print_group(code=cd, name=nm, layout=ly, options=op)
    pg.save()
    return HttpResponseRedirect(reverse('maket:print_group'))


def maket_status(request, id, status, source):
    order = Order_imports.objects.get(id=id)
    order.maket_status = status
    order.save()
    if source == 'order':
        return HttpResponseRedirect(reverse('maket:index'))
    if source == 'maket':
        return HttpResponseRedirect(reverse('maket:maket_base'))


def films(request):
    navi = 'films'

    item_group = Itemgroup_in_Maket.objects.filter(film__isnull=False).order_by('item')
    f_group = {}
    for i in item_group:
        if i.film not in f_group:
            f_group[i.film] = []
        ig_q = 0
        ig_p = 0
        ig_pp = 0
        try:
            itms = Item_imports.objects.filter(Q(order=i.maket.order) & Q(item__print_group=i.item.item.print_group))
            for it in itms:
                ig_q = ig_q + it.quantity
                ig_p = ig_p + it.quantity * it.item_price
                ig_pp = ig_pp + it.quantity * it.print_price
                prints = Print_imports.objects.filter(item=it)
                pr = ''
                len_pr = 0
                for prt in prints:
                    if prt.second_pass:
                        sec_pass = '2 пр., '
                    else:
                        sec_pass = ''
                    if 'Станд' in prt.place:
                        prt_place = 'Станд. ProEcoPen'
                    else:
                        prt_place = prt.place
                    pr += (prt_place + ', ' + prt.type + ', ' + str(prt.colors) + ' цв., ' + sec_pass).ljust(42, '-')
                    len_pr += 1
            f_group[i.film].append([i, ig_q, ig_p, ig_pp, ig_p + ig_pp, pr, len_pr])
        except:
            pass
    for fg in f_group:
        ig_q_all = 0
        ig_p_all = 0
        ig_pp_all = 0
        len_it = 0
        for content in f_group[fg]:
            ig_q_all += content[1]
            ig_p_all += content[2]
            ig_pp_all += content[3]
            len_it += content[6]
        f_group[fg].insert(0, [ig_q_all, ig_p_all, ig_pp_all, ig_pp_all + ig_p_all, len_it])

        f_group2 = list(f_group.items())
        paginator = Paginator(f_group2, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        f_group = dict(page_obj.object_list)

        date_range = []
        for i in range(page_obj.paginator.num_pages):
            page_obj2 = paginator.get_page(i + 1)
            try:
                date_tmp = repr(page_obj2.object_list[0][0])
                date_range.append([i + 1, 'до ' + date_tmp])
            except:
                date_range.append(['нет данных'])
    if f_group == {}:
        page_obj = ''
        date_range = ''
    context = {'navi': navi, 'active7': 'active', 'f_group': f_group, 'page_obj': page_obj, 'date_range': date_range}
    return render(request, 'maket/films.html', context)


@csrf_exempt
def save_to_film(request, id, film):
    item_group = Itemgroup_in_Maket.objects.get(id=id)
    try:
        film = Films.objects.get(id=film)
    except:
        try:
            flm = Films.objects.all().order_by('-date').first.film_id
            flm = flm + 1
        except:
            flm = 1
        film = Films(date=datetime.date.today(), film_id=flm)
        film.save()
    item_group.film = film
    item_group.save()
    return HttpResponse()


def vieworder(request, id):
    ord_i = id
    ord_imp = Order_imports.objects.get(pk=int(ord_i))
    order_id = ord_imp.id
    item_import = list(Item_imports.objects.filter(order=order_id).order_by('code'))
    print_import = ()
    for item in item_import:
        print_import = print_import + tuple(Print_imports.objects.filter(item=item))
    print_import = list(print_import)
    context = {'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import}
    return render(request, 'maket/vieworder.html', context)


@csrf_exempt
def update_to_film(request, data_to_film):
    data = data_to_film.split('_')
    id = data[0]
    date = data[1]
    format = data[2]
    sent = data[3]
    film_id = data[4]
    film = Films.objects.get(id=id)
    film.date = date
    film.format = format
    film.film_id = film_id
    if sent == '':
        film.status = False
    else:
        film.status = True
        film.date_sent = sent
    film.save()
    return HttpResponse()


def upload_order(request):
    id = request.POST['upload_id']
    order = Order_imports.objects.get(id=id)
    try:
        file = request.FILES['ChoseOrder']
        try:
            order.order_file.delete()
        except:
            pass
        order.order_file.save(file.name, file)
        order.order_upload = True
        order.save()
    except:
        pass
    return HttpResponseRedirect(reverse('maket:index'))


def download_order(request, id):
    order = Order_imports.objects.get(id=id)
    try:
        return FileResponse(open(order.order_file.path, 'rb'), content_type='application/pdf')
    except:
        order.order_upload = False
        order.save()
        return HttpResponse('<script type="text/javascript">window.close();</script>')


def upload_maket(request):
    id = request.POST['upload_id']
    maket = Makety.objects.get(id=id)
    try:
        file = request.FILES['ChoseMaket']
        try:
            maket.maket_file.delete()
        except:
            pass
        maket.maket_file.save(file.name, file)
        maket.uploaded = True
        maket.save()
    except:
        pass
    return HttpResponseRedirect(reverse('maket:maket_base'))


def download_maket(request, id):
    maket = Makety.objects.get(id=id)
    try:
        return FileResponse(open(maket.maket_file.path, 'rb'), content_type='application/pdf')
    except:
        maket.uploaded = False
        maket.save()
        return HttpResponse('<script type="text/javascript">window.close();</script>')


def upload_film(request):
    id = request.POST['upload_id']
    film = Films.objects.get(id=id)
    try:
        file = request.FILES['ChoseFilm']
        try:
            film.maket_file.delete()
        except:
            pass
        film.film_file.save(file.name, file)
        film.film_upload = True
        film.save()
    except:
        pass
    return HttpResponseRedirect(reverse('maket:films'))


def download_film(request, id):
    film = Films.objects.get(id=id)
    try:
        return FileResponse(open(film.film_file.path, 'rb'), content_type='application/force-download')
    except:
        film.film_upload = False
        film.save()
        return HttpResponse('<script type="text/javascript">window.close();</script>')


def look_up(request, navi):
    if navi == 'orders':
        try:
            lookup = request.POST['look_up']
        except:
            lookup = navi.split('_')[1]
        try:
            orders = Order_imports.objects.filter(Q(order_id__icontains=lookup) | Q(customer__name__icontains=lookup) | \
                                                  Q(manager__manager__icontains=lookup)).order_by('-order_date')
            ord_imp = orders.order_by('-order_date', '-id').first()
            item_import = list(Item_imports.objects.filter(order=ord_imp.id).order_by('code'))
            print_import = ()
            for item in item_import:
                print_import = print_import + tuple(Print_imports.objects.filter(item=item))
            print_import = list(print_import)

            context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
                       'orders': orders, 'active1': 'active', 'look_up': True, 'lookup': lookup}
            return render(request, 'maket/index.html', context)
        except:
            return HttpResponseRedirect(reverse('maket:index'))
    elif navi == 'maket_base':
        try:
            lookup = request.POST['look_up']
        except:
            pass
        if lookup == '':
            return HttpResponseRedirect(reverse('maket:maket_base'))

        item = Item_imports.objects.filter(print_name__icontains=lookup)
        ord_s = []
        for itm in item:
            if itm.order not in ord_s:
                ord_s.append(itm.order)
        maket = Makety.objects.filter(Q(order__order_id__icontains=lookup) | Q(order__customer__name__icontains=lookup) \
                                      | Q(order__in=ord_s)).order_by('-order_date', 'maket_id')

        item_group = Itemgroup_in_Maket.objects.all().order_by('item')
        f_group = {}
        for i in item_group:
            if i.maket not in f_group:
                f_group[i.maket] = []
            if i.checked:
                ig_q = 0
                ig_p = 0
                ig_pp = 0
                itms = Item_imports.objects.filter(
                    Q(order=i.maket.order) & Q(item__print_group=i.item.item.print_group))
                for it in itms:
                    ig_q = ig_q + it.quantity
                    ig_p = ig_p + it.quantity * it.item_price
                    ig_pp = ig_pp + it.quantity * it.print_price
                f_group[i.maket].append([i, ig_q, ig_p, ig_pp])

        f_maket = {}
        for m in maket:
            if m.order not in f_maket:
                f_maket[m.order] = {}
            f_maket[m.order].update({m: f_group.get(m)})

        films = Films.objects.filter(status=False).order_by('-date')
        current_date = datetime.date.today()
        try:
            last_film = films.first().film_id + 1
        except:
            last_film = 1

        context = {'navi': navi, 'active5': 'active', 'f_maket': f_maket, 'films': films,
                   'current_date': current_date, 'last_film': last_film, 'look_up': True}
        return render(request, 'maket/maket_base.html', context)

    elif navi == 'films':
        try:
            lookup = request.POST['look_up']
        except:
            pass
        if lookup == '':
            return HttpResponseRedirect(reverse('maket:films'))

        item = Item_imports.objects.filter(print_name__icontains=lookup)
        maket = Makety.objects.filter(Q(order__order_id__icontains=lookup) | Q(order__customer__name__icontains=lookup)) \
            .order_by('-order_date', 'maket_id')
        itg_in = Itemgroup_in_Maket.objects.filter(Q(maket__in=maket) | Q(item__in=item))
        flm_s = []
        for itg in itg_in:
            if itg.film not in flm_s and itg.film is not None:
                flm_s.append(itg.film)

        item_group = Itemgroup_in_Maket.objects.filter(film__in=flm_s).order_by('item')
        f_group = {}
        for i in item_group:
            if i.film not in f_group:
                f_group[i.film] = []
            ig_q = 0
            ig_p = 0
            ig_pp = 0
            itms = Item_imports.objects.filter(Q(order=i.maket.order) & Q(item__print_group=i.item.item.print_group))
            for it in itms:
                ig_q = ig_q + it.quantity
                ig_p = ig_p + it.quantity * it.item_price
                ig_pp = ig_pp + it.quantity * it.print_price
                prints = Print_imports.objects.filter(item=it)
                pr = ''
                len_pr = 0
                for prt in prints:
                    if prt.second_pass:
                        sec_pass = '2 пр., '
                    else:
                        sec_pass = ''
                    if 'Станд' in prt.place:
                        prt_place = 'Станд. ProEcoPen'
                    else:
                        prt_place = prt.place
                    pr += (prt_place + ', ' + prt.type + ', ' + str(prt.colors) + ' цв., ' + sec_pass).ljust(42, '-')
                    len_pr += 1
            f_group[i.film].append([i, ig_q, ig_p, ig_pp, ig_p + ig_pp, pr, len_pr])

        for fg in f_group:
            ig_q_all = 0
            ig_p_all = 0
            ig_pp_all = 0
            len_it = 0
            for content in f_group[fg]:
                ig_q_all += content[1]
                ig_p_all += content[2]
                ig_pp_all += content[3]
                len_it += content[6]
            f_group[fg].insert(0, [ig_q_all, ig_p_all, ig_pp_all, ig_pp_all + ig_p_all, len_it])

        context = {'navi': navi, 'active7': 'active', 'f_group': f_group, 'look_up': True}
        return render(request, 'maket/films.html', context)

    elif navi == 'customers':
        try:
            lookup = request.POST['look_up']
        except:
            pass
        if lookup == '':
            return HttpResponseRedirect(reverse('maket:customers'))
        order = Order_imports.objects.filter(manager__manager__icontains=lookup)
        cst_id = []
        for ord in order:
            cst_id.append(ord.customer.id)
        customers = Customer.objects.filter(Q(name__icontains=lookup) | Q(address__icontains=lookup) | \
                                            Q(id__in=cst_id)).order_by('name')

        context = {'navi': navi, 'customers': customers, 'active3': 'active'}
        return render(request, 'maket/customers.html', context)

    return


def delete_maket(request):
    id = request.POST['object_to_delete']
    maket = Makety.objects.get(id=id)
    maket.delete()
    return HttpResponseRedirect(reverse('maket:maket_base'))


def lost_maket(request, id):
    order_id = request.POST['l_order']
    try:
        order = Order_imports.objects.get(id=order_id)
    except:
        return HttpResponseRedirect(reverse('maket:admin'))
    maket_id = id
    maket = Makety.objects.get(id=maket_id)

    maket.order = order
    other_makets_number = max(Makety.objects.filter(order=order).values_list('maket_id'))[0]
    maket.maket_id = other_makets_number + 1
    maket.save()
    return HttpResponseRedirect(reverse('maket:admin'))


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

    return render(request, 'maket/order_edit.html', context)

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

    return HttpResponseRedirect(reverse('maket:order_edit', kwargs={'id': id}))

@csrf_exempt
def maket_check_status(request, id):
    order = Order_imports.objects.get(id=id)
    if order.to_check:
        order.to_check = False
    else:
        order.to_check = True
    order.save()
    return HttpResponse()


def patterns(request):
    print_group = Print_group.objects.all().order_by('code')
    context = {'active8': 'active', 'print_group': print_group}
    print_group = Print_group.objects.all().order_by('code')
    return render(request, 'maket/patterns.html', context)


def download_pattern(request, id):
    print_group = Print_group.objects.get(id=id)
    try:
        return FileResponse(open(print_group.pattern_file.path, 'rb'), content_type='application/pdf')
    except:
        pass
    return HttpResponse('<script type="text/javascript">window.close();</script>')


def upload_pattern(request):
    id = request.POST['upload_id']
    pattern = Print_group.objects.get(id=id)
    try:
        file = request.FILES['ChosePattern']
        try:
            pattern.pattern_file.delete()
        except:
            pass
        pattern.pattern_file.save(file.name, file)
        pattern.save()
    except:
        pass
    return HttpResponseRedirect(reverse('maket:patterns'))


def additional_files(request, id):
    order = Order_imports.objects.get(id=id)
    maket = list(Makety.objects.filter(order=order))
    additional_files = list(Additional_Files.objects.filter(order_id=order))
    context = {'order': order, 'maket': maket, 'additional_files': additional_files}
    return render(request, 'maket/additional_files.html', context)


def download_add_file(request, id):
    add_file = Additional_Files.objects.get(id=id)
    if add_file.file_type == 'pdf':
        try:
            return FileResponse(open(add_file.additional_file.path, 'rb'), content_type='application/pdf')
        except:
            return HttpResponse('<script type="text/javascript">window.close();</script>')
    else:
        try:
            return FileResponse(open(add_file.additional_file.path, 'rb'), content_type='application/force-download')
        except:
            return HttpResponse('<script type="text/javascript">window.close();</script>')


def add_file(request, id):
    order = Order_imports.objects.get(id=id)
    comment = request.POST['comment']
    type = request.POST['file_type']
    a_file = request.FILES['file']
    add_file = Additional_Files(order_id=order, comment=comment, file_type=type, additional_file_name=a_file.name)
    add_file.additional_file.save(a_file.name, a_file)
    add_file.save()
    return HttpResponseRedirect(reverse('maket:additional_files', args=[id]))

def delete_additional_file(request, id):
    add_file = Additional_Files.objects.get(id=id)
    new_id = add_file.order_id.id
    add_file.delete()
    return HttpResponseRedirect(reverse('maket:additional_files', args=[new_id]))


def print_place_connect(request):
    print_objects = Print_imports.objects.filter(print_place__isnull=True).order_by('-place')
    for prt_obj in print_objects:
        place = place_obj_from_place(prt_obj.place)
        prt_obj.print_place = place
        prt_obj.save()
    return HttpResponseRedirect(reverse('maket:admin'))


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


def delete_print_place(request, id):
    print_place = Print_place.objects.get(id=id)
    print_place.delete()
    return HttpResponseRedirect(reverse('maket:dicts'))


def delete_print_position(request, id):
    print_position = Print_position.objects.get(id=id)
    print_position.delete()
    return HttpResponseRedirect(reverse('maket:print_position'))
