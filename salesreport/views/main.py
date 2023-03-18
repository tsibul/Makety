import datetime
from salesreport.reports import *

from django.shortcuts import render, HttpResponseRedirect, reverse
from maket.models import Customer_all, Customer, Customer_groups, Customer_types, Detail_set, Item_color
from salesreport.models import Sales_doc_imports, Sales_docs
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.db.models import Q, F
from salesreport.views.service import *


def index(request):
    navi = 'Главная'
    period_types = ReportPeriod.calculatableList()
    date_begin = datetime.date(2017, 1, 1)
    date_begin2 = datetime.date(2020, 1, 1)
    date_end = datetime.date.today()
    context = {'navi': navi, 'period_types': period_types, 'date_begin': date_begin, 'date_end': date_end,
               'date_begin2': date_begin2}
    return render(request, 'salesreport/index.html', context)
