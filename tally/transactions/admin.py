from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from datetime import datetime
from .models import Customer, Transaction, SubTransaction, SubPurchase

# Filter transactions based on dates, day, month, year
class TransactionDateListFilter(admin.SimpleListFilter):
    title = 'date'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This week'),
            ('this_month', 'This month'),
            ('this_year', 'This year'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(date__date=datetime.today())
        if self.value() == 'this_week':
            return queryset.filter(date__week=datetime.today().isocalendar()[1])
        if self.value() == 'this_month':
            return queryset.filter(date__month=datetime.today().month)
        if self.value() == 'this_year':
            return queryset.filter(date__year=datetime.today().year)

class SubTransactionInline(admin.TabularInline):
    model = SubTransaction
    extra = 0

class SubPurchaseInline(admin.TabularInline):
    model = SubPurchase
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'relation_code')
    search_fields = ('first_name', 'prefix', 'last_name', 'relation_code')
    fieldsets = (
        ('Name', {
            'fields': ('first_name', 'prefix', 'last_name')
        }),
        ('Meta', {
            'fields': ('created', 'last_modified')
        }),
        ('Exact', {
            'classes': ('collapse',),
            'fields': ('relation_code',),
        }),
    )
    readonly_fields = ('created', 'last_modified')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer_formatted', 'date', 'total_formatted')
    ordering = ('-date',)
    search_fields = ('transaction_id', 'customer__first_name', 'customer__prefix', 'customer__last_name')
    list_filter = (TransactionDateListFilter,)
    inlines = [SubTransactionInline, SubPurchaseInline]
    autocomplete_fields = ['customer']
    fieldsets = (
        ('Information', {
            'fields': ('transaction_id', 'date', 'customer')
        }),
        ('Meta', {
            'fields': ('created', 'last_modified')
        }),
    )
    readonly_fields = ('transaction_id', 'created', 'last_modified')

    @admin.display(description='Total')
    def total_formatted(self, obj):
        return f"€ {obj.total()}"

    @admin.display(description='Customer')
    def customer_formatted(self, obj):
        link = reverse(f'admin:{obj.customer._meta.app_label}_{obj.customer._meta.model_name}_change', args=[obj.customer.id])
        return format_html('<a href="{}">{}</a>', link, str(obj.customer))

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction, TransactionAdmin)