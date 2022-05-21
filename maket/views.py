from django.shortcuts import render

from django.db import models
from django.utils import timezone
# Create your views here.
import datetime
from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from . import models
from django.db.models.lookups import GreaterThan, LessThan
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.urls import reverse
from django.db import transaction
from django.core.files import File
from django.views.generic import ListView
import csv