from django.urls import path
from . import views

app_name = 'maket'

urlpatterns = [
    path('', views.index, name='index'),
    path('reload', views.index, name='reload'),
    path('vieworder/<int:id>', views.vieworder, name='vieworder'),
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
    path('maket_base', views.maket_base, name='maket_base'),
    path('maket/maket', views.maket, name='maket'),
    path('delete_order/<int:id>', views.delete_order, name='delete order'),
    path('add_detail', views.add_detail, name='add_detail'),
    path('add_clr', views.add_clr, name='add_clr'),
    path('update_clr/<int:id>', views.update_clr, name='update_clr'),
    path('maket_print/<int:id>/<int:mk_id>', views.maket_print, name='maket_print'),
    path('update_cst/<int:id>', views.update_cst, name='update_cst'),
    path('maket_print/update_maket/<int:id>', views.update_maket, name='update_maket'),
    path('goods', views.goods, name='goods'),
    path('update_goods/<int:id>', views.upd_goods, name='update_goods'),
    path('update_pg/<int:id>', views.upd_pg, name='update_pg'),
    path('add_pg', views.add_pg, name='add_pg'),
    path('maket_status/<int:id>/<str:status>/<str:source>', views.maket_status, name='maket_status'),
    path('films', views.films, name='films'),
    path('lost_imports/<int:id>', views.lost_imports, name='lost_imports'),
    path('save_to_film/<int:id>/<int:film>', views.save_to_film, name='save_to_film'),
    path('update_to_film/<str:data_to_film>', views.update_to_film, name='update_to_film'),

]