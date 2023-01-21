from django.urls import path
from . import views

app_name = 'errors'

urlpatterns = [
    path('lost_imports/<int:id>', views.lost_imports, name='lost_imports'),
    path('lost_hex', views.lost_hex, name='lost_hex'),
    path('changed_customers/<int:id>', views.changed_customers, name='changed_customers'),
    path('order_edit/<int:id>', views.order_edit, name='order_edit'),
    path('order_save', views.order_save, name='order_save'),
    path('print_place_connect', views.print_place_connect, name='print_place_connect'),
    path('print_position_fix', views.print_position_fix, name='print_position_fix'),
    path('hex_repairs', views.hex_repairs, name='hex_repairs'),
    path('print_position_repairs', views.print_position_repairs, name='print_position_repairs'),
    path('customer_repairs', views.customer_repairs, name='customer_repairs'),
    path('color_place_repairs', views.color_place_repairs, name='color_place_repairs'),
    path('deleted_repairs', views.deleted_repairs, name='deleted_repairs'),
    path('import_repairs', views.import_repairs, name='import_repairs'),

    path('other', views.other, name='other'),
    path('badge_file_count', views.badge_file_count, name='badge_file_count'),


]


