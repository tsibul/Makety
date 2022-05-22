from django.urls import path
from . import views

app_name = 'maket'

urlpatterns = [
    path('', views.index, name='index'),
    path('main', views.main_maket, name='main_maket'),

    path('dicts', views.dicts, name='dicts'),
    path('update_clr_sch/<int:id>', views.update_clr_sch, name='update_clr_sch'),
    path('add_clr_sch', views.add_clr_sch, name='add_clr_sch'),
    path('update_prt_typ/<int:id>', views.update_prt_typ, name='update_prt_typ'),
    path('add_prt_typ', views.add_prt_typ, name='add_prt_typ'),
    path('update_prt_plc/<int:id>', views.update_prt_plc, name='update_prt_plc'),
    path('add_prt_plc', views.add_prt_plc, name='add_prt_plc'),
    path('update_prt_pos/<int:id>', views.update_prt_pos, name='update_prt_pos'),
    path('add_prt_pos', views.add_prt_pos, name='add_prt_pos'),

    path('admin', views.admin, name='admin'),
    path('maket/maket', views.maket, name='maket'),

]