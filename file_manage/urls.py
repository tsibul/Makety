from django.urls import path
from . import views

app_name = 'file_manage'

urlpatterns = [
    path('', views.file_manage, name='file_manage'),
]

