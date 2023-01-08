import datetime
import os

from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from Makety.service import *

from .models import Print_place, Print_position, Item_color, Order_imports, Item_imports, \
    Print_imports, Detail_set, Customer, Makety, Films, Itemgroup_in_Maket, Print_group, \
    Print_in_Maket, Print_color, Additional_Files, Customer_types, Customer_groups
from django.views.decorators.csrf import csrf_exempt


def main_maket(request):
    template = loader.get_template('maket/main.html')
    context = {}
    return HttpResponse(template.render({}, request, context))


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

#   date_range = []
#    for i in range(page_obj.paginator.num_pages):
#        page_obj2 = paginator.get_page(i + 1)
#        date_tmp = page_obj2.object_list[-1][0].order_date.strftime('%d.%m.%Y') + ' - ' + \
#                   page_obj2.object_list[0][0].order_date.strftime('%d.%m.%Y')
#        date_range.append([i + 1, date_tmp])

    context = {'navi': navi, 'active5': 'active', 'f_maket': f_maket, 'page_obj': page_obj, 'films': films,
               'current_date': current_date, 'last_film': last_film, 'look_up': False}
    context.update(count_errors())
    return render(request, 'maket/maket_base.html', context)


def maket(request):
    navi = 'maket'
    context = {'navi': navi}
    context.update(count_errors())
    return render(request, 'maket/index.html', context)


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
            return render(request, 'orders/index.html', context)
        except:
            return HttpResponseRedirect(reverse('orders:index'))
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
        if len(f_maket) == 0:
            return HttpResponseRedirect(reverse('maket:maket_base'))
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
            return HttpResponseRedirect(reverse('films:films'))

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
        if len(f_group) == 0:
            return HttpResponseRedirect(reverse('films:films'))
        context = {'navi': navi, 'active7': 'active', 'f_group': f_group, 'look_up': True}
        context.update(count_errors())
        return render(request, 'films/films.html', context)

    elif navi == 'customers':
        try:
            lookup = request.POST['look_up']
        except:
            return HttpResponseRedirect(reverse('dictionarys:customers'))
        if lookup == '':
            return HttpResponseRedirect(reverse('dictionarys:customers'))
        context = look_up_cst(lookup)
        if not context:
            return HttpResponseRedirect(reverse('dictionarys:customers'))
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
        return render(request, 'orders/index.html', context)

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




