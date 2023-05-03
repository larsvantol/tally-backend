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
    search_fields = ('name',)
    fieldsets = (
        ('Name', {
            'fields': ('name',)
        }),
        ('Meta', {
            'fields': ('created', 'last_modified')
        }),
    )
    readonly_fields = ('created', 'last_modified')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_group_formatted', 'price_formatted', 'vat_percentage_formatted', 'stock', 'account_code')
    list_filter = ('product_group', StockFilter)
    search_fields = ('name',)
    fieldsets = (
        ('Name', {
            'fields': ('name', 'product_group')
        }),
        ('Details', {
            'fields': ('price', 'stock', 'image_url')
        }),
        ('Meta', {
            'fields': ('created', 'last_modified')
        }),
    )
    readonly_fields = ('created', 'last_modified')

    @admin.display(description='Price')
    def price_formatted(self, obj):
        """
        Formats the price of the product as €xx.xx
        """
        return f'€ {obj.price:.2f}'
    
    @admin.display(description='Product group')
    def product_group_formatted(self, obj):
        """
        Formats the product group. It returns a link to the products filtered on the specific product group
        """
        # formats the product group with a link to the group filter
        return format_html(f'<a href="?product_group__id__exact={obj.product_group.id}">{obj.product_group.name}</a>')

    def vat_percentage_formatted(self, obj):
        """
        Formats the vat percentage of the product as xx%
        """
        return f'{obj.vat_percentage}%'

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)