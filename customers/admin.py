from django.contrib import admin
from customers import models as customers_models

@admin.register(customers_models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(customers_models.Request)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(customers_models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass

@admin.register(customers_models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(customers_models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass