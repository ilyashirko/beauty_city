# Generated by Django 4.1.4 on 2022-12-13 13:54

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(upload_to='media/services', verbose_name='Изображение')),
                ('price', models.SmallIntegerField(verbose_name='Стоимость')),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('image', models.ImageField(upload_to='media/salons', verbose_name='Изображение')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
                ('procedures', models.ManyToManyField(related_name='salons', to='salons.procedure', verbose_name='Procedures')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200, verbose_name='Имя')),
                ('lastname', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=200, verbose_name='Отчество')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
                ('started_working_at', models.DateField(verbose_name='Работает с')),
                ('image', models.ImageField(upload_to='media/masters', verbose_name='Изображение')),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('staff_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='salons.staff')),
                ('specialization', models.CharField(max_length=200, verbose_name='Специализация')),
            ],
            bases=('salons.staff',),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.CharField(choices=[('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'), ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'), ('sunday', 'Воскресенье')], max_length=30, verbose_name='День недели')),
                ('open', models.TimeField(verbose_name='Открывается в')),
                ('close', models.TimeField(verbose_name='Закрывается в')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='salons.salon', verbose_name='Salon')),
            ],
        ),
    ]
