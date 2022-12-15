from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def notes(request):
    return render(request, 'notes.html')


def service(request):
    print('GET', request.GET)
    print('POST', request.POST)

    return render(request, 'service.html')

