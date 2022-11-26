from django.urls import path
from . import views

app_name = 'addfiles'

urlpatterns = [
    path('<int:id>', views.additional_files, name='additional_files'),
    path('add_file/<int:id>', views.add_file, name='add_file'),
    path('download_add_file/<int:id>', views.download_add_file, name='download_add_file'),
    path('delete_additional_file/<int:id>', views.delete_additional_file, name='delete_additional_file'),
]

