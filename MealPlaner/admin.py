from django.contrib import admin
from .models import Product,Breakfast,Lunch,Dinner, Goal

admin.site.register(Product)
admin.site.register(Breakfast)
admin.site.register(Lunch)
admin.site.register(Dinner)
admin.site.register(Goal)
