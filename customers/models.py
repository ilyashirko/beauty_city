from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class Customer(models.Model):
    firstname = models.CharField('Имя', max_length=200)
    lastname = models.CharField('Фамилия', max_length=200, blank=True)
    patronymic = models.CharField('Отчество', max_length=200, blank=True)

    phonenumber = PhoneNumberField('Телефон')
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    # def get_actual_orders(self):
    #     return self.orders.filter('datetime__gt'=datetime.now())


class Order(models.Model):
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Клиент',
        related_name='orders',
        on_delete=models.PROTECT
    )
    salon = models.ForeignKey(
        'salons.Salon',
        verbose_name='Салон',
        related_name='orders',
        on_delete=models.PROTECT,
    )
    procedure = models.ForeignKey(
        'salons.Procedure',
        verbose_name='Салон',
        related_name='orders',
        on_delete=models.PROTECT,
        blank=True
    )
    master = models.ForeignKey(
        'salons.Master',
        verbose_name='Мастер',
        related_name='orders',
        on_delete=models.PROTECT,
        blank=True
    )
    datetime = models.DateTimeField(
        'Время записи'
    )


class Request(models.Model):
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Клиент',
        related_name='questions',
        on_delete=models.PROTECT
    )
    question = models.TextField('Вопрос', blank=True)
    
    asked_at = models.DateTimeField('Вопрос задан', auto_now_add=True, editable=False)

    
class Feedback(models.Model):
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Клиент',
        related_name='feedbacks',
        on_delete=models.PROTECT
    )
    salon = models.ForeignKey(
        'salons.Salon',
        verbose_name='Салон',
        related_name='feedbacks',
        on_delete=models.PROTECT,
        blank=True
    )
    staff = models.ForeignKey(
        'salons.Staff',
        verbose_name='Мастер',
        related_name='feedbacks',
        on_delete=models.PROTECT,
        blank=True
    )
    score = models.SmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True
    )
    feedback = models.TextField('Отзыв')
    leaved_at = models.DateTimeField(
        'Отзыв оставлен',
        auto_now_add=True,
        editable=False
    )

class Payment(models.Model):

    order = models.ForeignKey(
        'Order',
        verbose_name='Заказ',
        related_name='payments',
        on_delete=models.PROTECT
    )
    value = models.SmallIntegerField('Стоимость')