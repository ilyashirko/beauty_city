# Generated by Django 4.1.4 on 2022-12-15 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_request_delete_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='question',
            field=models.TextField(blank=True, verbose_name='Вопрос'),
        ),
    ]
