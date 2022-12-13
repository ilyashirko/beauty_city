from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    firstname = models.CharField('Имя', max_length=200)
    lastname = models.CharField('Фамилия', max_length=200)
    patronymic = models.CharField('Отчество', max_length=200, blank=True)

    phonenumber = PhoneNumberField('Телефон')
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Question(models.Model):
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Клиент',
        related_name='questions',
        on_delete=models.PROTECT
    )
    question = models.TextField('Вопрос')
    
    answer = models.TextField('Ответ', blank=True)

    who_answered = models.ForeignKey(
        'salons.Staff',
        verbose_name='Кто ответил',
        related_name='answered_questions',
        on_delete=models.PROTECT,
        blank=True
    )

    asked_at = models.DateTimeField('Вопрос задан', auto_now_add=True, editable=False)

    answered_at = models.DateTimeField('Ответили', blank=True)


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