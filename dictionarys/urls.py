from django.urls import path
from . import views

app_name = 'dictionarys'

urlpatterns = [
    path('goods', views.goods, name='goods'),
    path('update_goods/<int:id>', views.upd_goods, name='update_goods'),

    path('customers', views.customers, name='customers'),
    path('update_cst/<int:id>', views.update_cst, name='update_cst'),

    path('colors', views.colors, name='colors'),
    path('add_clr', views.add_clr, name='add_clr'),

    path('print_group', views.print_group, name='print_group'),
    path('update_pg', views.update_pg, name='update_pg'),

    path('print_position', views.print_position, name='print_position'),
    path('update_prt_pos/<int:id>', views.update_prt_pos, name='update_prt_pos'),
    path('add_prt_pos', views.add_prt_pos, name='add_prt_pos'),
    path('delete_print_position/<int:id>', views.delete_print_position, name='delete_print_positon'),

    path('other', views.other, name='other'),

    path('update_clr_sch/<int:id>', views.update_clr_sch, name='update_clr_sch'),
    path('add_clr_sch', views.add_clr_sch, name='add_clr_sch'),

    path('update_prt_typ/<int:id>', views.update_prt_typ, name='update_prt_typ'),
    path('add_prt_typ', views.add_prt_typ, name='add_prt_typ'),

    path('update_prt_plc/<int:id>', views.update_prt_plc, name='update_prt_plc'),
    path('add_prt_plc', views.add_prt_plc, name='add_prt_plc'),
    path('delete_print_place/<int:id>', views.delete_print_place, name='delete_print_place'),

    path('update_crm_type/<int:id>', views.update_crm_type, name='update_crm_type'),
    path('add_crm_type', views.add_crm_type, name='add_prt_plc'),
    path('delete_crm_type/<int:id>', views.delete_crm_type, name='delete_crm_type'),

    path('scale', views.scale, name='scale'),

]

