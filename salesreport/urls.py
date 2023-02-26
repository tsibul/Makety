from django.urls import path
from . import views

app_name = 'salesreport'

urlpatterns = [
    path('', views.index, name='index'),

    path('customers_active', views.customer_active, name='customers_active'),
    path('customers_all', views.customers_all, name='customers_all'),
    path('update_cst', views.update_cst, name='update_cst'),

    path('groups', views.groups, name='groups'),
    path('update_cst_group', views.update_cst_group, name='update_cst_group'),
    path('group_export', views.group_export, name='group_export'),

    path('group_lists', views.group_lists, name='group_lists'),
    path('add_to_group', views.add_to_group, name='add_to_group'),
    path('delete_from_group', views.delete_from_group, name='delete_from_group'),

    path('import_report', views.import_report, name='import_report'),
    path('import_cst', views.import_cst, name='import_cst'),

    path('cst_sinhro_inn', views.cst_sinhro_inn, name='cst_sinhro_inn'),
    path('cst_sinhro_err', views.cst_sinhro_err, name='cst_sinhro_err'),
    path('cst_sinhro_no', views.cst_sinhro_no, name='cst_sinhro_no'),
    path('cst_sinhro_group', views.cst_sinhro_group, name='cst_sinhro_group'),
    path('cst_set_inactive', views.cst_set_inactive, name='cst_set_inactive'),

    path('group_set_inactive', views.group_set_inactive, name='group_set_inactive'),
    path('group_set_dates', views.group_set_dates, name='group_set_dates'),

    path('sales_docs', views.sales_docs, name='sales_docs'),
    path('customer_date', views.customer_date, name='customer_date'),
    path('unsinhronized', views.cst_unsinhronized, name='cst_unsinhronized'),

    path('admin', views.admin, name='admin'),
    path('transaction_delete', views.transaction_delete, name='transaction_delete'),
    path('customer_all_delete', views.customer_all_delete, name='customer_all_delete'),

]