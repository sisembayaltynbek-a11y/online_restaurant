from django.contrib import admin
from .models import MealType, Meal, Deliveries

# Register your models here.
admin.site.register(Deliveries)
admin.site.register(MealType)
admin.site.register(Meal)