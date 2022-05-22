from django.shortcuts import render

from django.db import models
from django.utils import timezone
# Create your views here.
import datetime
from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Color_scheme, Print_type, Print_place, Print_position
from django.db.models.lookups import GreaterThan, LessThan
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.urls import reverse
from django.db import transaction
from django.core.files import File
from django.views.generic import ListView
import csv


def main_maket(request):
    template = loader.get_template('maket/main.html')
    return HttpResponse(template.render({}, request))


def index(request):
    navi = 'orders'
    context = {'navi': navi}
    return render(request, 'maket/index.html', context)

def dicts(request):
    navi = 'dicts'
    color_scheme = Color_scheme.objects.all()
    print_type = Print_type.objects.all()
    print_place = Print_place.objects.all()
    print_position = Print_position.objects.all()

    context = {'navi': navi, 'color_scheme': color_scheme, 'print_type': print_type, 'print_place':print_place,
               'print_position': print_position}
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

