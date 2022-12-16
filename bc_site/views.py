import phonenumbers

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from salons import models as salons_models
import json
from hashlib import md5
from customers.models import Customer 
from salons.models import Staff

has_code_request = False
telephone = ''

def index(request):
    global login_code, has_code_request, telephone

    if request.method == 'POST':
        if has_code_request:
            has_code_request = False

            if request.POST['num1'] == login_code['num1'] and request.POST['num2'] == login_code['num2'] and request.POST['num3'] == login_code['num3'] and request.POST['num4'] == login_code['num4']:
                request.user.username = telephone

                try:
                    staff = Staff.objects.get(
                        phonenumber = telephone
                    )

                    if staff.is_administrator:
                        return render(request, 'admin.html')
                    else:
                        return render(request, 'notes.html')
                except ObjectDoesNotExist:
                    customer = Customer.objects.get_or_create(
                        firstname = 'Имя',
                        phonenumber = telephone
                    )

                    return render(request, 'notes.html')
            else:
                telephone = ''
                return render(request, 'wrongLoginCode.html')
        else:
            phone_number = phonenumbers.parse(request.POST['tel'])

            if phonenumbers.is_possible_number(phone_number):
                telephone = request.POST['tel']
                telephone = telephone.replace(" ", "")
                telephone = telephone.replace("-", "")
                telephone = telephone.replace("(", "")
                telephone = telephone.replace(")", "")

                login_code = {
                    'num1': telephone[8],
                    'num2': telephone[9],
                    'num3': telephone[10],
                    'num4': telephone[11],
                }

                telephone = request.POST['tel']

                context = {
                   'tel': request.POST['tel']
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

            try:
                staff = Staff.objects.get(
                    phonenumber = telephone
                )

                context = {
                    'is_staff': staff.is_administrator
                }

                return render(request, 'index.html', context)
            except ObjectDoesNotExist:
                return render(request, 'index.html')
        else:
            context = {
                'is_staff': False
            }
        
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
    else:
        return render(request, 'notLogged.html')

    context = dict()
    context['salons'] = [
        {
            'title': salon.title,
            'address': salon.address
        }
        for salon in salons_models.Salon.objects.all()
    ]


    context['json_salons'] = dict()
    for salon in salons_models.Salon.objects.all():
        all_procedures = dict()
        for specialization, procedures in salon.get_procedures().items():
            all_procedures[specialization.specialization] = [
                {'title': procedure.title, 'price': procedure.price}
                for procedure in procedures
            ]
        context['json_salons'][salon.title] = {
            'address': salon.address,
            'procedures': all_procedures
        }       
    print(context['json_salons'])     
    context['json_salons'] = json.dumps(context['json_salons'])
    print(context['json_salons'])
    
    context['data'] = json.dumps(
        [
            {
                'name': f'{master.firstname} {master.lastname}',
                'image': master.image.url,
                'specialization': master.specialization.specialization,
            } 
            for master in salons_models.Master.objects.all()
        ]
    )
    context['specializations'] = [
            {"hash": md5(bytes(specialization.specialization, 'utf-8')).hexdigest(),
            "value": specialization.specialization}
            for specialization in salons_models.Specialization.objects.all()
    ]

    context['json_specializations'] = json.dumps(
        [
            {"hash": md5(bytes(specialization.specialization, 'utf-8')).hexdigest(),
            "value": specialization.specialization}
            for specialization in salons_models.Specialization.objects.all()
        ]
    )
    

    return render(request, 'service.html', context)


def admin_page(request):
    return render(request, 'admin.html')


def service_finally(request):
    if telephone:
        request.user.username = telephone

    return render(request, 'serviceFinally.html')


def exit(request):
    global telephone

    telephone = ''
    request.user.username = telephone

    return redirect('start_page')