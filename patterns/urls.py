from django.urls import path
from . import views

app_name = 'patterns'

urlpatterns = [
    path('patterns', views.patterns, name='patterns'),
    path('upload_pattern', views.upload_pattern, name='upload_pattern'),
    path('download_pattern/<int:id>', views.download_pattern, name='download_pattern'),
]