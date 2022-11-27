from django.urls import path
from . import views

app_name = 'file_manage'

urlpatterns = [
    path('files_orders', views.files_orders, name='files_orders'),
    path('all_files_orders', views.all_files_orders, name='all_files_orders'),
    path('delete_files_orders', views.delete_files_orders, name='delete_files_orders'),

    path('files_makety', views.files_makety, name='files_makety'),
    path('all_files_makety', views.all_files_makety, name='all_files_makety'),
    path('delete_files_makety', views.delete_files_makety, name='delete_files_makety'),

    path('files_films', views.files_films, name='files_films'),
    path('all_files_films', views.all_files_films, name='all_files_films'),
    path('delete_files_films', views.delete_files_films, name='delete_files_films'),

    path('files_additional', views.files_additional, name='files_additional'),
    path('all_files_additional', views.all_files_additional, name='all_files_additional'),
    path('delete_files_additional', views.delete_files_additional, name='delete_files_additional'),

    path('files_patterns', views.files_patterns, name='files_patterns'),
    path('all_files_patterns', views.all_files_patterns, name='all_files_patterns'),
    path('delete_files_patterns', views.delete_files_patterns, name='delete_files_patterns'),
]

