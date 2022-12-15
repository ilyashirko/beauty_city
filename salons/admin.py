from django.contrib import admin
from salons import models as salons_models


@admin.register(salons_models.Salon)
class SalonAdmin(admin.ModelAdmin):
    raw_id_fields = ('procedures',)
    list_display = ('social_networks', 'schedule')


@admin.register(salons_models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(salons_models.Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    pass


@admin.register(salons_models.Staff)
class StaffAdmin(admin.ModelAdmin):
    pass


@admin.register(salons_models.Master)
class MasterAdmin(admin.ModelAdmin):
    pass