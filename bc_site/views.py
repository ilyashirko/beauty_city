import json
import phonenumbers
from datetime import datetime, timezone
from hashlib import md5

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse

from customers.models import Customer, Order, Payment
from salons import models as salons_models
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
                        customer = Customer.objects.get_or_create(
                            firstname = staff.firstname,
                            lastname = staff.lastname,
                            phonenumber = telephone
                        )

                        context = get_customers_orders(telephone)

                        return render(request, 'notes.html', context)
                except ObjectDoesNotExist:
                    try:
                        customer = Customer.objects.get(
                            phonenumber = telephone
                        )
                    except ObjectDoesNotExist:
                        customer = Customer.objects.get_or_create(
                            firstname = 'Имя',
                            phonenumber = telephone
                        )

                    context = get_customers_orders(telephone)
                    print(context)

                    return render(request, 'notes.html', context)
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

    context = get_customers_orders(telephone)

    return render(request, 'notes.html', context)


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


def get_customers_orders(phonenumber):
    current_orders = []
    past_orders = []

    if phonenumber:
        customer = Customer.objects.get(
            phonenumber = phonenumber
        )

        orders = customer.orders.all()

        for order in orders:
            now = datetime.now(timezone.utc)

            order_params = {
                'id': order.id,
                'salon_address': order.salon.address,
                'procedure': order.procedure.title,
                'price': order.procedure.price,
                'master_firstname': order.master.firstname,
                'master_lastname': order.master.lastname,
                'order_hour': order.datetime.hour + 3,
                'order_minute': order.datetime.minute,
                'order_day': order.datetime.day
            }

            if order.datetime.month == 1:
                order_params['order_month'] = 'января'
            elif order.datetime.month == 2:
                order_params['order_month'] = 'февраля'
            elif order.datetime.month == 3:
                order_params['order_month'] = 'марта'
            elif order.datetime.month == 4:
                order_params['order_month'] = 'апреля'
            elif order.datetime.month == 5:
                order_params['order_month'] = 'мая'
            elif order.datetime.month == 6:
                order_params['order_month'] = 'июня'
            elif order.datetime.month == 7:
                order_params['order_month'] = 'июля'
            elif order.datetime.month == 8:
                order_params['order_month'] = 'августа'
            elif order.datetime.month == 9:
                order_params['order_month'] = 'сентября'
            elif order.datetime.month == 10:
                order_params['order_month'] = 'октября'
            elif order.datetime.month == 11:
                order_params['order_month'] = 'ноября'
            elif order.datetime.month == 12:
                order_params['order_month'] = 'декабря'

            if order.datetime.minute == 0:
                order_params['order_minute'] = '00'

            if order.datetime > now:
                try:
                    payment = Payment.objects.get(order=order)

                    order_params['is_paid'] = True
                except ObjectDoesNotExist:
                    order_params['is_paid'] = False    

                current_orders.append(order_params)
            elif order.datetime < now:
                past_orders.append(order_params)

    context = {
        'current_orders': current_orders,
        'past_orders': past_orders
    }

    print(context)

    return context


def make_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    stripe.api_key = settings.STRIPE_API_KEY

    amount =  int(order.procedure.price)*100

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Вы платите за услугу "{order.procedure}", {order.procedure.price} рублей.',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        metadata = {
            'order_id': order_id
        },
        success_url=request.build_absolute_uri(reverse('successed_payment')),
        cancel_url=request.build_absolute_uri(reverse('cancelled_payment')),
    )

    return redirect(session.url, code=303)


def pay_success(request):
    stripe.api_key = settings.STRIPE_API_KEY
    stripe_sessions = stripe.checkout.Session.list(limit=3)
    session = stripe_sessions['data'][0]
    if session['payment_status'] == 'paid':
        order_id = session['metadata']['order_id']
        order = Order.objects.get(id=order_id)
        payment, created = Payment.objects.get_or_create(
            order=order,
            value=order.procedure.price
        )

    return render(request, 'success.html')


def cancelled(request):
    return render(request, 'cancelled.html')