from django.urls import path
from . import views

app_name = 'maket'

urlpatterns = [
    path('order', views.index, name='index'),
    path('reload', views.index, name='reload'),
    path('order/<str:id_str>', views.reload, name='reload2'),

    path('import_order', views.import_order, name='import_order'),

    path('maket_base', views.maket_base, name='maket_base'),
    path('maket/maket', views.maket, name='maket'),
    path('delete_order', views.delete_order, name='delete_order'),

    path('maket_status/<int:id>/<str:status>/<str:source>', views.maket_status, name='maket_status'),
    path('save_to_film/<int:id>/<int:film>', views.save_to_film, name='save_to_film'),
    path('upload_order', views.upload_order, name='upload_order'),
    path('download_order/<int:id>', views.download_order, name='download_order'),
    path('upload_maket/<str:look_up>', views.upload_maket, name='maket_order'),
    path('download_maket/<int:id>', views.download_maket, name='download_maket'),
    path('look_up/<str:navi>', views.look_up, name='look_up'),
    path('delete_maket', views.delete_maket, name='delete_maket'),
    path('order_edit/<int:id>', views.order_edit, name='order_edit'),
    path('order_save', views.order_save, name='order_save'),
    path('maket_check_status/<int:id>', views.maket_check_status, name='maket_check_status'),
    path('additional_files/<int:id>', views.additional_files, name='additional_files'),
    path('add_file/<int:id>', views.add_file, name='add_file'),
    path('download_add_file/<int:id>', views.download_add_file, name='download_add_file'),
    path('delete_additional_file/<int:id>', views.delete_additional_file, name='delete_additional_file'),
    path('look_up_not_finished/<str:navi>', views.look_up_not_finished, name='look_up_not_finished'),
    path('order_errors', views.order_errors, name='order_errors'),

]