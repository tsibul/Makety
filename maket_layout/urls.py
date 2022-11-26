from django.urls import path
from . import views

app_name = 'maket_layout'

urlpatterns = [

    path('<int:id>/<int:mk_id>', views.maket_print, name='maket_print'),
    path('maket_print_empty/<int:id>/<int:mk_id>', views.maket_print_empty, name='maket_print_empty'),

    path('update_maket/<int:id>', views.update_maket, name='update_maket'),
    path('update_maket_empty/<int:id>', views.update_maket_empty, name='update_maket_empty'),

]