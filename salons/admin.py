from django.contrib import admin
from salons import models as salons_models


@admin.register(salons_models.Salon)
class SalonAdmin(admin.ModelAdmin):
    raw_id_fields = ('procedures',)
    


@admin.register(salons_models.SalonSchedule)
class SalonScheduleAdmin(admin.ModelAdmin):
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


@admin.register(salons_models.Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


@admin.register(salons_models.SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    pass


@admin.register(salons_models.MasterSchedule)
class MasterScheduleAdmin(admin.ModelAdmin):
    pass

