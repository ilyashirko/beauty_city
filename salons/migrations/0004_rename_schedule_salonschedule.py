# Generated by Django 4.1.4 on 2022-12-15 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salons', '0003_salon_email_socialnetwork'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Schedule',
            new_name='SalonSchedule',
        ),
    ]