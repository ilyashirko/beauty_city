from django.core.management.base import BaseCommand
from salons import models as salons_models


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        salons_models.Salon.objects.all().delete()
        salons_models.SocialNetwork.objects.all().delete()
        salons_models.SalonSchedule.objects.all().delete()
        salons_models.Procedure.objects.all().delete()
        salons_models.Staff.objects.all().delete()
        salons_models.Specialization.objects.all().delete()
        salons_models.Master.objects.all().delete()
        salons_models.MasterSchedule.objects.all().delete()