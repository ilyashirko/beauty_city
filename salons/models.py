from django.db import models
from datetime import date, datetime
from phonenumber_field.modelfields import PhoneNumberField

WEEK_DAYS = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    )


class Salon(models.Model):
    title = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=200)
    image = models.ImageField('Изображение', upload_to='media/salons')
    
    phonenumber = PhoneNumberField('Телефон')
    email = models.EmailField('Почта', null=True)

    procedures = models.ManyToManyField(
        'Procedure',
        verbose_name='Procedures',
        related_name='salons'
    )

    def __str__(self):
        return f'{self.title} ({self.address})'

    def get_procedures(self):
        procedures = self.procedures.all()
        all_specs = set(proc.specialization for proc in procedures)
        result = dict()
        for spec in all_specs:
            result[spec] = [procedure for procedure in procedures if procedure.specialization == spec]
        return result

class SocialNetwork(models.Model):
    salon = models.ForeignKey(
        'Salon',
        verbose_name='Salon',
        related_name='social_networks',
        on_delete=models.CASCADE
    )
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Иконка', upload_to='media/icons')
    link = models.URLField('Ссылка')


class SalonSchedule(models.Model):
    salon = models.ForeignKey(
        'Salon',
        verbose_name='Salon',
        related_name='schedule',
        on_delete=models.CASCADE
    )
    week_day = models.CharField('День недели', max_length=30, choices=WEEK_DAYS)
    open = models.TimeField('Открывается в')
    close = models.TimeField('Закрывается в')

    def __str__(self):
        return f'{self.salon} ({self.week_day}): {self.open} - {self.close}'


class Procedure(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='media/services')
    price = models.SmallIntegerField('Стоимость')
    specialization = models.ForeignKey(
        'Specialization',
        verbose_name='Специализация',
        related_name='procedures',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.title

    def find_masters_on_salon(self, salon: Salon):
        return Master.objects.filter(
            specialization=self.specialization,
            schedule__salon=salon
        )

class Staff(models.Model):
    firstname = models.CharField('Имя', max_length=200)
    lastname = models.CharField('Фамилия', max_length=200)
    patronymic = models.CharField('Отчество', max_length=200, blank=True)

    phonenumber = PhoneNumberField('Телефон')

    started_working_at = models.DateField('Работает с')

    is_administrator = models.BooleanField('Администратор', default=False)
    
    image = models.ImageField('Изображение', upload_to='media/masters')


class Specialization(models.Model):
    specialization = models.CharField('Специализация', max_length=200)


class Master(Staff):
    specialization = models.ForeignKey(
        'Specialization',
        verbose_name='Специализация',
        related_name='masters',
        on_delete=models.PROTECT
    )

    def get_experience(self) -> tuple[int, int, int]:
        experience = date.today() - self.started_working_at
        years = experience // 365
        months = (experience - years * 365) // 30
        days = experience - years * 365 - months * 30
        return years, months, days

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    

class MasterSchedule(models.Model):
    salon = models.ForeignKey(
        'Salon',
        verbose_name='Salon',
        related_name='master_schedule',
        on_delete=models.CASCADE
    )
    master = models.ForeignKey(
        'Master',
        verbose_name='Master',
        related_name='schedule',
        on_delete=models.CASCADE
    )
    week_day = models.CharField('День недели', max_length=30, choices=WEEK_DAYS)
    start_at = models.TimeField('Начинает работу в', null=True)
    finish_at = models.TimeField('Заканчивает работу в', null=True)

    def __str__(self):
        return f'{self.salon} ({self.week_day}): {self.start_at} - {self.finish_at}'