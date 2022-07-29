from django.urls import path
from . import views

app_name = 'maket'

urlpatterns = [
    path('', views.index, name='index'),
    path('reload', views.index, name='reload'),
    path('<int:id>', views.reload, name='reload2'),

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

    path('customers', views.customers, name='customers'),
#    path('FileForm', views.get_file, name='fform'),
    path('import_order', views.import_order, name='import_order'),

    path('admin', views.admin, name='admin'),
    path('maket/maket', views.maket, name='maket'),
    path('delete_order/<int:id>', views.delete_order, name='delete order'),
    path('add_detail', views.add_detail, name='add_detail'),
    path('update_details/<int:id>', views.upd_detail, name='update_details'),
    path('add_clr', views.add_clr, name='add_clr'),
    path('update_clr/<int:id>', views.update_clr, name='update_clr'),
    path('maket_print/<int:id>', views.maket_print, name='maket_print'),

]