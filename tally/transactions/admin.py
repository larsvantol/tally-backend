from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Customer, Transaction, SubTransaction, SubPurchase


class SubTransactionInline(admin.TabularInline):
    model = SubTransaction
    extra = 0

class SubPurchaseInline(admin.TabularInline):
    model = SubPurchase
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'prefix', 'last_name')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer_formatted', 'date_created', 'total_formatted')
    inlines = [SubTransactionInline, SubPurchaseInline]

    @admin.display(description='Total')
    def total_formatted(self, obj):
        return f"€ {obj.total()}"

    @admin.display(description='Customer')
    def customer_formatted(self, obj):
        link = reverse(f'admin:{obj.customer._meta.app_label}_{obj.customer._meta.model_name}_change', args=[obj.customer.id])
        return format_html('<a href="{}">{}</a>', link, str(obj.customer))

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction, TransactionAdmin)