import csv
import datetime
import os

from bs4 import BeautifulSoup
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from maket.models import Item_color, Order_imports, Item_imports, Print_imports, Detail_set, Customer, Manger, Makety, \
     Additional_Files, Customer_types, Customer_all, Customer_groups
from django.db.models import Q
from django.core.paginator import Paginator

from maket.views import count_errors, place_obj_from_place, print_color_check, print_position_and_color_from_print_obj


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
            date_tmp = page_obj2.object_list[-1].order_date.strftime('%d.%m.%Y') +  ' - ' + \
                       page_obj2.object_list[0].order_date.strftime('%d.%m.%Y')
            date_range.append([i + 1, date_tmp])
        context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
                   'orders': orders, 'active1': 'active', 'page_obj': page_obj, 'date_range': date_range}
    except:
        context = {'navi': navi}

    context.update(count_errors())
    return render(request, 'orders/index.html', context)


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
    context.update(count_errors())
    return render(request, 'orders/index.html', context)


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
            type = order_no[slice(13, 14)]
            type2 = order_no[slice(14, 15)]
            typegroup_in = type + type2
            if customer.customer_type != typegroup_in:
                customer.customer_type = typegroup_in
                customer.save()
    except:
        region = customer_inn[slice(0, 2)]
        type = order_no[slice(13, 14)]
        type2 = order_no[slice(14, 15)]
        typegroup_in = type + type2
        try:
            typegroup = Customer_types.objects.get(code=typegroup_in)
        except:
            typegroup = ''
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
        if len(customer_inn) >= 10:
            customer_all = Customer_all.objects.filter(inn=customer_inn).order_by('frigat_id').last()
        else:
            customer_all = Customer_all.objects.filter(customer_name__in=customer_name).order_by('frigat_id').last()
        customer = Customer(name=customer_name, address=customer_address, inn=customer_inn, region=region,
                            type=type, customer_type=typegroup, date_first=order_date, customer_all=customer_all,
                            frigat_id=customer_all.frigat_id)
        customer_all.customer_type = typegroup
        customer_all.type = type
        customer_all.save()
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
            if len(itm_clr[1]) > 2:
                itm_clr[0] = str(itm_clr[0]) + '.' + str(itm_clr[1])
                itm_clr.pop(1)
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
            print_pos = print_position_and_color_from_print_obj(place, print_item)
            if print_pos != '':
                print_item.print_position = print_pos
                print_item.save()
            print_color_check(print_item)
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

    return HttpResponseRedirect(reverse('orders:reload', kwargs={'id_str': tmp}))


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
    tmp = str(ord_imp.id) + '_'
    return HttpResponseRedirect(reverse('orders:reload', kwargs={'id_str': tmp}))


def delete_order(request):
    id = request.POST['object_to_delete']
    order_d = Order_imports.objects.get(id=id)
    makets = Makety.objects.filter(order=order_d)
    for maket in makets:
        maket.maket_file.delete()
    additional_files = Additional_Files.objects.filter(order_id=order_d)
    for additional_file in additional_files:
        additional_file.additional_file.delete()
    order_d.delete()
    return HttpResponseRedirect(reverse('orders:index'))


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
        order.number_orders = 1
        order.save()
    except:
        pass
    return HttpResponseRedirect(reverse('orders:index'))


def download_order(request, id):
    order = Order_imports.objects.get(id=id)
    try:
        return FileResponse(open(order.order_file.path, 'rb'), content_type='application/pdf')
    except:
        order.order_upload = False
        order.save()
        return HttpResponse('<script type="text/javascript">window.close();</script>')


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

    return render(request, 'orders/order_edit.html', context)


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

    return HttpResponseRedirect(reverse('orders:order_edit', kwargs={'id': id}))


def order_errors(request):
    navi = 'admin'
    orders = Order_imports.objects.filter(to_check=True).order_by('-order_date', 'order_id')
    ord_imp = orders.order_by('-order_date', '-id').first()
    try:
        item_import = list(Item_imports.objects.filter(order=ord_imp.id).order_by('code'))
    except:
        return HttpResponseRedirect(reverse('maket:index'))
    print_import = ()
    for item in item_import:
        print_import = print_import + tuple(Print_imports.objects.filter(item=item))
    print_import = list(print_import)

    context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
               'orders': orders, 'active4': 'active', 'look_up': True}
    context.update(count_errors())
    return render(request, 'orders/index.html', context)

