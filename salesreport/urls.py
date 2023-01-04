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
    path('cst_sinhro_inn', views.cst_sinhro_inn, name='cst_sinhro_inn'),
    path('cst_sinhro_err', views.cst_sinhro_err, name='cst_sinhro_err'),
    path('cst_sinhro_no', views.cst_sinhro_no, name='cst_sinhro_no'),
    path('sales_docs', views.sales_docs, name='sales_docs'),
    path('customer_date', views.customer_date, name='customer_date'),
]