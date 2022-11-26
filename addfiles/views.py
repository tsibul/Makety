from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from maket.models import Print_place, Print_position, Item_color, Order_imports, Item_imports, \
    Print_imports, Detail_set, Customer, Manger, Makety, Films, Itemgroup_in_Maket, Print_group, \
    Print_in_Maket, Additional_Files, Print_color
from django.db.models import Q


def additional_files(request, id):
    order = Order_imports.objects.get(id=id)
    maket = list(Makety.objects.filter(order=order))
    additional_files = list(Additional_Files.objects.filter(order_id=order))
    context = {'order': order, 'maket': maket, 'additional_files': additional_files}
    return render(request, 'addfiles/additional_files.html', context)


def download_add_file(request, id):
    add_file = Additional_Files.objects.get(id=id)
    if add_file.file_type == 'pdf':
        try:
            return FileResponse(open(add_file.additional_file.path, 'rb'), content_type='application/pdf')
        except:
            return HttpResponse('<script type="text/javascript">window.close();</script>')
    else:
        try:
            return FileResponse(open(add_file.additional_file.path, 'rb'), content_type='application/force-download')
        except:
            return HttpResponse('<script type="text/javascript">window.close();</script>')


def add_file(request, id):
    order = Order_imports.objects.get(id=id)
    comment = request.POST['comment']
    type = request.POST['file_type']
    a_file = request.FILES['file']
    add_file = Additional_Files(order_id=order, comment=comment, file_type=type, additional_file_name=a_file.name)
    add_file.additional_file.save(a_file.name, a_file)
    order.number_additional += 1
    order.save()
    add_file.save()
    return HttpResponseRedirect(reverse('addfiles:additional_files', args=[id]))


def delete_additional_file(request, id):
    add_file = Additional_Files.objects.get(id=id)
    order = add_file.order_id
    order.number_additional -= 1
    order.save()
    new_id = add_file.order_id.id
    add_file.additional_file.delete()
    add_file.delete()
    return HttpResponseRedirect(reverse('addfiles:additional_files', args=[new_id]))


