import os
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from maket.models import Order_imports, Makety, Films, Additional_Files, Print_group
from django.db.models import Q
from django.core.paginator import Paginator

from maket.views import count_errors


def files_orders(request):
    path_orders = 'files/orders'
    files_in_orders_list = os.listdir(path_orders)
    files_list = []
    for file in files_in_orders_list:
        try:
            order = Order_imports.objects.get(order_file=file)
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_orders.html', context)


def all_files_orders(request):
    path_orders = 'files/orders'
    files_in_orders_list = os.listdir(path_orders)
    files_list = []
    for file in files_in_orders_list:
        try:
            order = Order_imports.objects.get(order_file=file)
            files_list.append([order, file])
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_orders.html', context)


def delete_files_orders(request):
    file_name = request.POST['file_name']
    return HttpResponseRedirect(reverse('file_manage:files_orders'))


def files_makety(request):
    path_makety = 'files/makety'
    files_in_makety_list = os.listdir(path_makety)
    files_list = []
    for file in files_in_makety_list:
        try:
            maket = Makety.objects.get(maket_file=file)
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_makety.html', context)


def all_files_makety(request):
    path_makety = 'files/makety'
    files_in_makety_list = os.listdir(path_makety)
    files_in_makety_list.sort()
    files_list = []
    for file in files_in_makety_list:
        try:
            maket = Makety.objects.get(maket_file=file)
            files_list.append([maket, file])
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_makety.html', context)


def delete_files_makety(request):
    file_name = request.POST['file_name']
    return HttpResponseRedirect(reverse('file_manage:files_makety'))


def files_films(request):
    path_films = 'files/films'
    files_in_films_list = os.listdir(path_films)
    files_list = []
    for file in files_in_films_list:
        try:
            film = Films.objects.get(film_file=file)
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_films.html', context)


def all_files_films(request):
    path_films = 'files/films'
    files_in_films_list = os.listdir(path_films)
    files_list = []
    for file in files_in_films_list:
        try:
            film = Films.objects.get(film_file=file)
            files_list.append([film, file])
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_films.html', context)


def delete_files_films(request):
    file_name = request.POST['file_name']
    return HttpResponseRedirect(reverse('file_manage:files_films'))


def files_additional(request):
    path_additional = 'files/additional'
    files_in_additional_list = os.listdir(path_additional)
    files_list = []
    for file in files_in_additional_list:
        try:
            additional = Additional_Files.objects.get(additional_file=file)
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_additional.html', context)


def all_files_additional(request):
    path_additional = 'files/additional'
    files_in_additional_list = os.listdir(path_additional)
    files_list = []
    for file in files_in_additional_list:
        try:
            additional = Additional_Files.objects.get(additional_file=file)
            files_list.append([additional, file])
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_additional.html', context)


def delete_files_additional(request):
    file_name = request.POST['file_name']
    return HttpResponseRedirect(reverse('file_manage:files_additional'))


def files_patterns(request):
    path_patterns = 'files/patterns'
    files_in_patterns_list = os.listdir(path_patterns)
    files_list = []
    for file in files_in_patterns_list:
        try:
            pattern = Print_group.objects.get(pattern_file=file)
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_patterns.html', context)


def all_files_patterns(request):
    path_patterns = 'files/patterns'
    files_in_patterns_list = os.listdir(path_patterns)
    files_list = []
    for file in files_in_patterns_list:
        try:
            pattern = Print_group.objects.get(pattern_file=file)
            files_list.append([pattern, file])
        except:
            files_list.append(['', file])
    context = {'active6': 'active', 'files_list': files_list}
    context.update(count_errors())
    return render(request, 'file_manage/files_patterns.html', context)


def delete_files_patterns(request):
    file_name = request.POST['file_name']
    return HttpResponseRedirect(reverse('file_manage:files_patterns'))
