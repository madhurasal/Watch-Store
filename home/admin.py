from django.contrib import admin
from .models import *


class customeradmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email',)
    search_fields = ('name',)


class prodadmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price',)
    list_filter = ('category',)
    list_per_page = 10  


class oitemadmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added',)
    list_per_page = 10

class orderadmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'complete',)
    list_per_page = 10

class shipadmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'date_added',)
    list_per_page = 10
    list_filter = ('address',)

class conadmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'desc',)
    list_per_page = 10



         

# Register your models here.
admin.site.register(Customer, customeradmin)
admin.site.register(Product, prodadmin)
admin.site.register(Order, orderadmin)
admin.site.register(OrderItem, oitemadmin)
admin.site.register(ShippingAddress, shipadmin)
admin.site.register(Contact, conadmin )
















