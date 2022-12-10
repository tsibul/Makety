from django.urls import path
from . import views

app_name = 'salesreport'

urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.customer_sales, name='customers'),
    path('groups', views.customer_groups, name='groups'),
    path('import_report', views.import_report, name='import_report'),
]