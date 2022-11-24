from django.urls import path
from . import views

app_name = 'maket'

urlpatterns = [
    path('order', views.index, name='index'),
    path('reload', views.index, name='reload'),
    path('vieworder/<int:id>', views.vieworder, name='vieworder'),
    path('order/<str:id_str>', views.reload, name='reload2'),

    path('import_order', views.import_order, name='import_order'),

    path('admin', views.admin, name='admin'),
    path('maket_base', views.maket_base, name='maket_base'),
    path('maket/maket', views.maket, name='maket'),
    path('delete_order', views.delete_order, name='delete_order'),

    path('maket_print/<int:id>/<int:mk_id>', views.maket_print, name='maket_print'),
    path('maket_print_empty/<int:id>/<int:mk_id>', views.maket_print_empty, name='maket_print_empty'),

    path('maket_print/update_maket/<int:id>', views.update_maket, name='update_maket'),
    path('maket_print/update_maket_empty/<int:id>', views.update_maket_empty, name='update_maket_empty'),
    path('maket_status/<int:id>/<str:status>/<str:source>', views.maket_status, name='maket_status'),
    path('films', views.films, name='films'),
    path('lost_imports/<int:id>', views.lost_imports, name='lost_imports'),
    path('save_to_film/<int:id>/<int:film>', views.save_to_film, name='save_to_film'),
    path('update_to_film/<str:data_to_film>', views.update_to_film, name='update_to_film'),
    path('upload_order', views.upload_order, name='upload_order'),
    path('download_order/<int:id>', views.download_order, name='download_order'),
    path('upload_maket/<str:look_up>', views.upload_maket, name='maket_order'),
    path('download_maket/<int:id>', views.download_maket, name='download_maket'),
    path('upload_film', views.upload_film, name='upload_film'),
    path('download_film/<int:id>', views.download_film, name='download_film'),
    path('look_up/<str:navi>', views.look_up, name='look_up'),
    path('delete_maket', views.delete_maket, name='delete_maket'),
    path('lost_maket/<int:id>', views.lost_maket, name='lost_maket'),
    path('lost_hex', views.lost_hex, name='lost_hex'),
    path('changed_customers/<int:id>', views.changed_customers, name='changed_customers'),
    path('order_edit/<int:id>', views.order_edit, name='order_edit'),
    path('order_save', views.order_save, name='order_save'),
    path('maket_check_status/<int:id>', views.maket_check_status, name='maket_check_status'),
    path('additional_files/<int:id>', views.additional_files, name='additional_files'),
    path('add_file/<int:id>', views.add_file, name='add_file'),
    path('download_add_file/<int:id>', views.download_add_file, name='download_add_file'),
    path('delete_additional_file/<int:id>', views.delete_additional_file, name='delete_additional_file'),
    path('print_place_connect', views.print_place_connect, name='print_place_connect'),
    path('print_position_fix', views.print_position_fix, name='print_position_fix'),
    path('look_up_not_finished/<str:navi>', views.look_up_not_finished, name='look_up_not_finished'),
    path('hex_repairs', views.hex_repairs, name='hex_repairs'),
    path('print_position_repairs', views.print_position_repairs, name='print_position_repairs'),
    path('customer_repairs', views.customer_repairs, name='customer_repairs'),
    path('color_place_repairs', views.color_place_repairs, name='color_place_repairs'),
    path('deleted_repairs', views.deleted_repairs, name='deleted_repairs'),
    path('maket_repairs', views.maket_repairs, name='maket_repairs'),
    path('import_repairs', views.import_repairs, name='import_repairs'),
    path('order_errors', views.order_errors, name='order_errors'),
    path('badge_file_count', views.badge_file_count, name='badge_file_count'),

]