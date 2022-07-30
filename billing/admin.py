from django.contrib import admin
from .models import Invoice, InvoiceBills, Products, Payments, Costumersmodel, Test, Expenses
# Register your models here.

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['billnumber', 'ammountpaid']
    
class InvoiceBillsAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'item', 'totalammount']
    

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_price', 'gst']


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'ammount', 'refrence_number']


class CostumersAdmin(admin.ModelAdmin):
    list_display = ['costumer_name', 'gst_number', 'contact']
    
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceBills, InvoiceBillsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Costumersmodel, CostumersAdmin)
admin.site.register(Test)
admin.site.register(Expenses)
