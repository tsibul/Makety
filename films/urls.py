from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    path('', views.films, name='films'),
    path('upload_film', views.upload_film, name='upload_film'),
    path('download_film/<int:id>', views.download_film, name='download_film'),
    path('vieworder/<int:id>', views.vieworder, name='vieworder'),

]