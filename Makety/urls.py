"""Makety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('maket/', include('maket.urls')),
    path('dicts/', include('dictionarys.urls')),
    path('patterns/', include('patterns.urls')),
    path('errors/', include('errors.urls')),
    path('films/', include('films.urls')),
    path('maket_layout/', include('maket_layout.urls')),
    path('addfiles/', include('addfiles.urls')),
    path('orders/', include('orders.urls')),
    path('file_manage/', include('file_manage.urls')),
    path('salesreport/', include('salesreport.urls')),

]
