from django.contrib import admin
from .models import Order, Customer, Technician, Onu, Router

# Register your models here.
@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Onu)
class OnuAdmin(admin.ModelAdmin):
    pass

@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    pass