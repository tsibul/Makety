from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('reload', views.index, name='reload'),
    path('import_order', views.import_order, name='import_order'),
    path('delete_order', views.delete_order, name='delete_order'),
    path('upload_order', views.upload_order, name='upload_order'),
    path('download_order/<int:id>', views.download_order, name='download_order'),
    path('order_edit/<int:id>', views.order_edit, name='order_edit'),
    path('order_save', views.order_save, name='order_save'),
    path('order_errors', views.order_errors, name='order_errors'),
]

