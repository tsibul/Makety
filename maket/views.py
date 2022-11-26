import datetime

from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import FileResponse, Http404

from .models import Print_place, Print_position, Item_color, Order_imports, Item_imports, \
    Print_imports, Detail_set, Customer, Makety, Films, Itemgroup_in_Maket, Print_group, \
    Print_in_Maket, Print_color
from django.views.decorators.csrf import csrf_exempt


def main_maket(request):
    template = loader.get_template('maket/main.html')
    context = {}
    return HttpResponse(template.render({}, request, context))


def count_errors():
    lost_imports_len = Item_imports.objects.filter(item=None).count()
    lost_makets_len = Makety.objects.filter(order=None).count()
    lost_deleted_len = Item_imports.objects.filter(order=None).count() + Print_imports.objects.filter(item=None).count()
    print_colors = list(Print_color.objects.values_list('print_item_id', flat=True))
    lost_colors_len = Print_imports.objects.filter(Q(print_place__isnull=True) | ~Q(id__in=print_colors)).order_by('-place').count()
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
    err_len = lost_position_len + lost_makets_len +lost_deleted_len +lost_colors_len + changed_customers_len + \
              lost_hex_len + order_errors_len

    context = {'lost_imports_len': lost_imports_len, 'lost_makets_len': lost_makets_len,
               'lost_deleted_len': lost_deleted_len, 'lost_colors_len': lost_colors_len,
               'changed_customers_len': changed_customers_len, 'lost_hex_len': lost_hex_len, 'lost_position_len':
               lost_position_len, 'err_len': err_len, 'order_errors_len': order_errors_len}
    return context


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
               'current_date': current_date, 'last_film': last_film, 'date_range': date_range, 'look_up': False}
    context.update(count_errors())
    return render(request, 'maket/maket_base.html', context)


def maket(request):
    navi = 'maket'
    context = {'navi': navi}
    context.update(count_errors())
    return render(request, 'maket/index.html', context)


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


def product_range(ord_imp):
    return product_range


def maket_status(request, id, status, source):
    order = Order_imports.objects.get(id=id)
    order.maket_status = status
    order.save()
    if source == 'order':
        return HttpResponseRedirect(reverse('maket:index'))
    if source == 'maket':
        return HttpResponseRedirect(reverse('maket:maket_base'))


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


def upload_maket(request, look_up):
    id = request.POST['upload_id']
    maket = Makety.objects.get(id=id)
    order = maket.order
    try:
        file = request.FILES['ChoseMaket']
        try:
            maket.maket_file.delete()
        except:
            order.number_makets += 1
        maket.maket_file.save(file.name, file)
        maket.uploaded = True
        maket.save()
        order.maket_status = 'R'
        order.save()
    except:
        pass
    if look_up == 'True':
        return HttpResponseRedirect(reverse('maket:look_up_not_finished', kwargs={'navi': 'maket_base'}))
    else:
        return HttpResponseRedirect(reverse('maket:maket_base'))


def download_maket(request, id):
    maket = Makety.objects.get(id=id)
    try:
        return FileResponse(open(maket.maket_file.path, 'rb'), content_type='application/pdf')
    except:
        maket.uploaded = False
        maket.save()
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
            context.update(count_errors())
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
                   'current_date': current_date, 'last_film': last_film, 'look_up': True, 'lookup': lookup}
        context.update(count_errors())
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
        context.update(count_errors())
        return render(request, 'films/films.html', context)

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
        context.update(count_errors())
        return render(request, 'dictionarys/customers.html', context)

    return


def delete_maket(request):
    id = request.POST['object_to_delete']
    maket = Makety.objects.get(id=id)
    order = maket.order
    order.number_makets -= 1
    order.save()
    maket.maket_file.delete()
    maket.delete()
    return HttpResponseRedirect(reverse('maket:maket_base'))


@csrf_exempt
def maket_check_status(request, id):
    order = Order_imports.objects.get(id=id)
    order.to_check = not order.to_check
    order.save()
    return HttpResponse()


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
    return HttpResponseRedirect(reverse('maket:color_place_repairs'))


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


def look_up_not_finished(request, navi):
    if navi == 'orders':
        orders = Order_imports.objects.filter(Q(maket_status='P') | Q(maket_status='N')).order_by('-order_date', 'order_id')
        ord_imp = orders.order_by('-order_date', '-id').first()
        item_import = list(Item_imports.objects.filter(order=ord_imp.id).order_by('code'))
        print_import = ()
        for item in item_import:
            print_import = print_import + tuple(Print_imports.objects.filter(item=item))
        print_import = list(print_import)

        context = {'navi': navi, 'ord_imp': ord_imp, 'item_import': item_import, 'print_import': print_import,
                   'orders': orders, 'active1': 'active', 'look_up': True}
        context.update(count_errors())
        return render(request, 'maket/index.html', context)

    elif navi == 'maket_base':

        maket = Makety.objects.filter(Q(order__maket_status='P') | Q(order__maket_status='N')).order_by('-order_date', 'maket_id')

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
        context.update(count_errors())
        return render(request, 'maket/maket_base.html', context)
    return

