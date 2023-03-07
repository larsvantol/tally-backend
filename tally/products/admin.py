from django.contrib import admin
from .models import Product, ProductGroup

class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)