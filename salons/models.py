from django.db import models
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField


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


class Schedule(models.Model):
    WEEK_DAYS = (
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    )

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

    def __str__(self):
        return self.title

class Staff(models.Model):
    firstname = models.CharField('Имя', max_length=200)
    lastname = models.CharField('Фамилия', max_length=200)
    patronymic = models.CharField('Отчество', max_length=200, blank=True)

    phonenumber = PhoneNumberField('Телефон')

    started_working_at = models.DateField('Работает с')

    is_administrator = models.BooleanField('Администратор', default=False)
    
    image = models.ImageField('Изображение', upload_to='media/masters')


class Master(Staff):
    specialization = models.CharField('Специализация', max_length=200)

    def get_experience(self) -> tuple[int, int, int]:
        experience = date.today() - self.started_working_at
        years = experience // 365
        months = (experience - years * 365) // 30
        days = experience - years * 365 - months * 30
        return years, months, days

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    