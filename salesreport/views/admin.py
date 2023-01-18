from django.shortcuts import render, HttpResponseRedirect, reverse

def admin(request):
    navi = 'Admin'
    context = {'navi': navi}
    return render(request, 'salesreport/admin.html', context)
