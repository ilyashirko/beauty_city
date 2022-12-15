import phonenumbers

from django.contrib.auth.models import User
from django.shortcuts import render
from salons import models as salons_models
import json

from customers.models import Customer 


has_code_request = False
telephone = ''

def index(request):
    global login_code, has_code_request, telephone

    if request.method == 'POST':
        if has_code_request:
            has_code_request = False

            if request.POST['num1'] == login_code['num1'] and request.POST['num2'] == login_code['num2'] and request.POST['num3'] == login_code['num3'] and request.POST['num4'] == login_code['num4']:
                request.user.username = telephone

                customer = Customer.objects.get_or_create(
                    firstname = 'Имя',
                    phonenumber = telephone)

                return render(request, 'notes.html')
            else:
                telephone = ''
                return render(request, 'wrongLoginCode.html')
        else:
            phone_number = phonenumbers.parse(request.POST['tel'])

            if phonenumbers.is_possible_number(phone_number):
                telephone = request.POST['tel']

                context = {
                   'tel': request.POST['tel']
                }

                login_code = {
                    'num1': request.POST['tel'][13],
                    'num2': request.POST['tel'][14],
                    'num3': request.POST['tel'][16],
                    'num4': request.POST['tel'][17],
                }

                has_code_request = True
                return render(request, 'confirmPopup.html', context)
            else:
                has_code_request = False
                return render(request, 'notPossiblePhoneNumber.html')
    else:
        has_code_request = False

        if telephone:
            request.user.username = telephone

        return render(request, 'index.html')


def notes(request):
    if telephone:
        request.user.username = telephone

    return render(request, 'notes.html')


def service(request):
    print('GET', request.GET)
    print('POST', request.POST)

    if telephone:
        request.user.username = telephone

    data = json.dumps(
        [
            {
                'name': f'{master.firstname} {master.lastname}',
                'image': master.image.url,
                'specialization': master.specialization.specialization,
            } 
            for master in salons_models.Master.objects.all()
        ]
    )
    print([
            {
                'name': f'{master.firstname} {master.lastname}',
                'image': master.image.url,
                'specialization': master.specialization.specialization
            } 
            for master in salons_models.Master.objects.all()
        ])
    context = {'data': data}
    return render(request, 'service.html', context)


def admin_page(request):
    return render(request, 'admin.html')


def service_finally(request):
    if telephone:
        request.user.username = telephone

    return render(request, 'serviceFinally.html')