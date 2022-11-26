from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from maket.models import Order_imports, Makety, Films, Additional_Files
from django.db.models import Q
from django.core.paginator import Paginator


def file_manage(request):
    context = {'aciive': 'active6'}
    return render(request, 'file_manage/file_manage.html', context)
