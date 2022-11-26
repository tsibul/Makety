from django.urls import path
from . import views

app_name = 'maket'

urlpatterns = [
    path('maket_base', views.maket_base, name='maket_base'),
    path('maket/maket', views.maket, name='maket'),

    path('maket_status/<int:id>/<str:status>/<str:source>', views.maket_status, name='maket_status'),
    path('save_to_film/<int:id>/<int:film>', views.save_to_film, name='save_to_film'),
    path('upload_maket/<str:look_up>', views.upload_maket, name='maket_order'),
    path('download_maket/<int:id>', views.download_maket, name='download_maket'),
    path('look_up/<str:navi>', views.look_up, name='look_up'),
    path('delete_maket', views.delete_maket, name='delete_maket'),
    path('maket_check_status/<int:id>', views.maket_check_status, name='maket_check_status'),
    path('look_up_not_finished/<str:navi>', views.look_up_not_finished, name='look_up_not_finished'),
]