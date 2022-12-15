from django.core.management.base import BaseCommand
from salons import models as salons_models
from django.core.files.base import ContentFile
from hashlib import md5
import random
import datetime

class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        SPECIALIZATIONS = (
            "Парикмахерские услуги",
            "Ногтевой сервис",
            "Макияж"
        )
        with open('media/coming_soon.jpg', 'rb') as default_photo:
            image = ContentFile(
                default_photo.read(),
                name=md5(default_photo.read()).hexdigest()
            )

        PROCEDURES = {
            "Парикмахерские услуги": {
                "Окрашивание волос": {
                    'image': image,
                    'price': 5000
                },
                "Укладка волос": {
                    'image': image,
                    'price': 1500
                }
            },
            "Ногтевой сервис": {
                "Маникюр. Классический": {
                    'image': image,
                    'price': 1400
                },
                "Педикюр": {
                    'image': image,
                    'price': 1400
                },
                "Наращивание ногтей": {
                    'image': image,
                    'price': 1400
                }
            },
            "Макияж": {
                "Дневной макияж": {
                    'image': image,
                    'price': 1400 
                },
                "Свадебный макияж": {
                    'image': image,
                    'price': 3000
                },
                "Вечерний макияж": {
                    'image': image,
                    'price': 2000
                }
            }
        }
        specialization_objects = []
        procedures_objects = []
        for specialization, procedures in PROCEDURES.items():
            specialization_object, _ = salons_models.Specialization.objects.get_or_create(
                specialization=specialization
            )
            specialization_objects.append(specialization_object)
            for procedure, procedure_info in procedures.items():
                procedure, _ = salons_models.Procedure.objects.get_or_create(
                    title=procedure,
                    image=procedure_info['image'],
                    price=procedure_info['price'],
                    specialization=specialization_object
                )
                procedures_objects.append(procedure)

        admin, _ = salons_models.Staff.objects.get_or_create(
            firstname='Админ',
            lastname='Админов',
            phonenumber=f'+7911{random.randint(1000000, 9999999)}',
            started_working_at=datetime.date(
                year=random.randint(2000, 2022),
                month=random.randint(1, 12),
                day=random.randint(1, 28)
            ),
            is_administrator=True,
            image=image
        )
        
        SALONS = (
            {
                'title': 'Salon1',
                'address': 'Невский 1',
                'phonenumber': f'+7812{random.randint(1000000, 9999999)}',
                'email': 'salon1@email.ru'
            },
            {
                'title': 'Salon2',
                'address': 'Невский 23',
                'phonenumber': f'+7812{random.randint(1000000, 9999999)}',
                'email': 'salon2@email.ru'
            },
            {
                'title': 'Salon3',
                'address': 'Невский 45',
                'phonenumber': f'+7812{random.randint(1000000, 9999999)}',
                'email': 'salon3@email.ru'
            },
        )
        salons_objects = list()
        for salon in SALONS:
            salon_object, created = salons_models.Salon.objects.get_or_create(
                title=salon['title'],
                address=salon['address'],
                image=image,
                phonenumber=salon['phonenumber'],
                email=salon['email']
            )
            salons_objects.append(salon_object)
            if not created:
                procedures = random.choices(procedures_objects, k=5)
                for procedure in procedures:
                    salon_object.procedures.add(procedure)
                    salon_object.save()
        
        NAMES = ("Ольга", "Мария", "Алевтина", "Инна", "Инга", "Анастасия", "Наталья")
        LASTNAMES = ("Иванова", "Петрова", "Краснова", "Романова")

        for i in range(10):
            master, _ = salons_models.Master.objects.get_or_create(
                firstname=random.choice(NAMES),
                lastname=random.choice(LASTNAMES),
                phonenumber=f'+7911{random.randint(1000000, 9999999)}',
                started_working_at=datetime.date(
                    year=random.randint(2000, 2022),
                    month=random.randint(1, 12),
                    day=random.randint(1, 28)
                ),
                image=image,
                specialization=random.choice(specialization_objects)
            )
            for num, _ in salons_models.WEEK_DAYS:
                is_free = random.choice((None, 1))
                if is_free:
                    start=datetime.time(hour=10, minute=0, second=0)
                    finish=datetime.time(hour=22, minute=0, second=0)
                else:
                    start, finish = None, None
                salons_models.MasterSchedule.objects.get_or_create(
                    salon=random.choice(salons_objects),
                    master=master,
                    week_day=num,
                    start_at=start,
                    finish_at=finish
                )

        SOCIALS = {
            'vk': 'https://vk.com',
            'google': 'https://google.com',
            'yandex': 'https://ya.ru'
        }

        for salon in salons_objects:
            for social, url in SOCIALS.items():
                salons_models.SocialNetwork.objects.get_or_create(
                    salon=salon,
                    title=social,
                    image=image,
                    link=url
                )

            for num, _ in salons_models.WEEK_DAYS:
                salons_models.SalonSchedule.objects.get_or_create(
                    salon=salon,
                    week_day=num,
                    open=datetime.time(hour=10, minute=0, second=0),
                    close=datetime.time(hour=22, minute=0, second=0)
                )
