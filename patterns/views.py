from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from maket.models import Print_group

from maket.views import count_errors


def patterns(request):
    print_group = Print_group.objects.all().order_by('code')
    context = {'active8': 'active', 'print_group': print_group}
    context.update(count_errors())
    return render(request, 'patterns/patterns.html', context)


def download_pattern(request, id):
    print_group = Print_group.objects.get(id=id)
    try:
        return FileResponse(open(print_group.pattern_file.path, 'rb'), content_type='application/pdf')
    except:
        pass
    return HttpResponse('<script type="text/javascript">window.close();</script>')


def upload_pattern(request):
    upload_id = request.POST['upload_id']
    pattern = Print_group.objects.get(id=upload_id)
    try:
        file = request.FILES['ChosePattern']
        try:
            pattern.pattern_file.delete()
        except:
            pass
        pattern.pattern_file.save(file.name, file)
        pattern.save()
    except:
        pass
    return HttpResponseRedirect(reverse('patterns:patterns'))
