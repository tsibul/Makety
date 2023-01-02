from django.urls import path
from . import views

app_name = 'salesreport'

urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.customer_sales, name='customers'),
    path('customers_all', views.customer_all, name='customers_all'),
    path('groups', views.customer_groups, name='groups'),
    path('import_report', views.import_report, name='import_report'),
    path('import_cst', views.import_cst, name='import_cst'),
    path('cst_sinhro', views.cst_sinhro, name='cst_sinhro'),
]