import datetime

from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render
from django.urls import reverse
from maket.models import Order_imports, Item_imports, Films, Itemgroup_in_Maket, Print_imports
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from maket.views import count_errors


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
    context.update(count_errors())
    return render(request, 'films/films.html', context)


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
    return HttpResponseRedirect(reverse('films:films'))


def download_film(request, id):
    film = Films.objects.get(id=id)
    try:
        return FileResponse(open(film.film_file.path, 'rb'), content_type='application/force-download')
    except:
        film.film_upload = False
        film.save()
        return HttpResponse('<script type="text/javascript">window.close();</script>')


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
    return render(request, 'films/vieworder.html', context)


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

