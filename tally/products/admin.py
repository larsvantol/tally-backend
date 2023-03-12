from django.contrib import admin
from django.utils.html import format_html
from math import log, exp
from .models import Product, ProductGroup

# Filter for stock using simplelistfilter
class StockFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return (
            ('0-10', 'Less than 10'),
            ('10-50', '10-50'),
            ('50-100', '50-100'),
            ('100-500', '100-500'),
            ('500>', 'Greater than 500'),
        )
    
    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        elif self.value() == '500>':
            return queryset.filter(stock__gte=500)
        else:
            min, max = self.value().split('-')
            return queryset.filter(stock__gte=min, stock__lte=max)
        


class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_group_formatted', 'price_formatted', 'stock')
    list_filter = ('product_group', StockFilter)

    def price_formatted(self, obj):
        # format price as €xx.xx
        return f'€ {obj.price:.2f}'
    
    def product_group_formatted(self, obj):
        # formats the product group with a link to the group filter
        return format_html(f'<a href="?product_group__id__exact={obj.product_group.id}">{obj.product_group.name}</a>')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)