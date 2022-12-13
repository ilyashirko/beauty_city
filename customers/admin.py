from django.contrib import admin
from customers import models as customers_models

@admin.register(customers_models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(customers_models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(customers_models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass