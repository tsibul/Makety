from django.urls import path
from . import views

app_name = 'salesreport'

urlpatterns = [
    path('', views.index, name='index'),

    path('customers_active', views.customer_active, name='customers_active'),
    path('region_97', views.region_97, name='region_97'),
    path('customers_all', views.customers_all, name='customers_all'),
    path('update_cst', views.update_cst, name='update_cst'),
    path('import_inn', views.import_inn, name='import_inn'),
    path('export_cst_types', views.export_cst_types, name='export_cst_types'),

    path('groups', views.groups, name='groups'),
    path('update_cst_group', views.update_cst_group, name='update_cst_group'),
    path('group_export', views.group_export, name='group_export'),
    path('group_import', views.group_import, name='group_import'),

    path('group_lists', views.group_lists, name='group_lists'),
    path('group_delete', views.group_delete, name='group_delete'),
    path('add_to_group', views.add_to_group, name='add_to_group'),
    path('delete_from_group', views.delete_from_group, name='delete_from_group'),

    path('import_report', views.import_report, name='import_report'),
    path('import_cst', views.import_cst, name='import_cst'),

    path('cst_sinhro_group', views.cst_sinhro_group, name='cst_sinhro_group'),
    path('cst_set_inactive', views.cst_set_inactive, name='cst_set_inactive'),
    path('set_frigat_id', views.set_frigat_id, name='set_frigat_id'),

    path('group_set_inactive', views.group_set_inactive, name='group_set_inactive'),
    path('group_set_dates', views.group_set_dates, name='group_set_dates'),

    path('sales_docs', views.sales_docs, name='sales_docs'),
    path('sales_docs_recheck', views.sales_docs_recheck, name='sales_docs_recheck'),
    path('unsinhronized', views.cst_unsinhronized, name='cst_unsinhronized'),
    path('no_inn', views.cst_no_inn, name='cst_no_inn'),

    path('management', views.management, name='management'),
    path('report_periods', views.report_periods, name='report_periods'),
    path('sales_set_periods', views.sales_set_periods, name='sales_set_periods'),
    path('lost_goods', views.lost_goods, name='lost_goods'),

    path('customer_period_sales', views.customer_period_sales, name='customer_period_sales'),

    path('admin', views.admin, name='admin'),
    path('transaction_delete', views.transaction_delete, name='transaction_delete'),
    path('customer_all_delete', views.customer_all_delete, name='customer_all_delete'),

    path('report_customer_period', views.report_customer_period, name='report_customer_period'),
    path('report_customer_migrations', views.report_customer_migrations, name='report_customer_migrations'),
    path('report_customer_geography', views.report_customer_geography, name='report_customer_geography'),

    path('client_transactions/<int:client_id>/<int:period_id>', views.client_transactions, name='client_transactions'),
    path('detail/<int:salesdoc_id>', views.detail, name='detail'),

]