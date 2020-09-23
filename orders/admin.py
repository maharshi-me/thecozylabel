from django.contrib import admin
from .models import Order, Shipping_Details

# Register your models here.
admin.site.register(Order)
admin.site.register(Shipping_Details)

