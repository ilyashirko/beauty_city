from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def notes(request):
    return render(request, 'notes.html')


def service(request):
    print('GET', request.GET)
    print('POST', request.POST)

    return render(request, 'service.html')


def admin_page(request):
    return render(request, 'admin.html')


def service_finally(request):
    return render(request, 'serviceFinally.html')