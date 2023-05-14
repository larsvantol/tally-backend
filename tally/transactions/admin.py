from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
from datetime import datetime
from .models import Customer, Transaction, SubTransaction, SubPurchase
import csv


# Filter transactions based on dates, day, month, year
class TransactionDateListFilter(admin.SimpleListFilter):
    title = "date"
    parameter_name = "date"

    def lookups(self, request, model_admin):
        return (
            ("today", "Today"),
            ("this_week", "This week"),
            ("this_month", "This month"),
            ("this_year", "This year"),
        )

    def queryset(self, request, queryset):
        if self.value() == "today":
            return queryset.filter(date__date=datetime.today())
        if self.value() == "this_week":
            return queryset.filter(date__week=datetime.today().isocalendar()[1])
        if self.value() == "this_month":
            return queryset.filter(date__month=datetime.today().month)
        if self.value() == "this_year":
            return queryset.filter(date__year=datetime.today().year)


class SubTransactionInline(admin.TabularInline):
    model = SubTransaction
    extra = 0


class SubPurchaseInline(admin.TabularInline):
    model = SubPurchase
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "relation_code")
    search_fields = ("first_name", "prefix", "last_name", "relation_code")
    fieldsets = (
        ("Name", {"fields": ("first_name", "prefix", "last_name")}),
        ("Authentication", {"fields": ("encrypted_uuid", "encrypted_code")}),
        ("Meta", {"fields": ("created", "last_modified")}),
        (
            "Exact",
            {
                "classes": ("collapse",),
                "fields": ("relation_code",),
            },
        ),
    )
    readonly_fields = ("created", "last_modified")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["encrypted_uuid"].widget = forms.PasswordInput(
            render_value=True,
            attrs={"autocomplete": "new-password"},
        )
        form.base_fields["encrypted_code"].widget = forms.PasswordInput(
            render_value=True,
            attrs={"autocomplete": "new-password"},
        )
        return form

    # Hash UUID and code before saving
    def save_model(self, request, obj, form, change):
        if not (form.cleaned_data.get("encrypted_uuid") == None):
            obj.encrypted_uuid = obj.hash_uuid(form.cleaned_data.get("encrypted_uuid"))
        if not (form.cleaned_data.get("encrypted_code") == None):
            obj.encrypted_code = obj.hash_code(form.cleaned_data.get("encrypted_code"))
        super().save_model(request, obj, form, change)


@admin.action(description="Export to csv")
def export_to_csv(self, request, queryset):
    result = []
    for transaction in queryset:
        result.extend(transaction.export_to_list_exact_format())

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="export.csv"'
        },  # TODO: Filename based on export date range and/or settings
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "nieuwe boeking",
            "Omschrijving: Kopregel",
            "Factuurdatum",
            "Code betalingsconditie",
            "Relatiecode",
            "Grootboekrekening",
            "Omschrijving",
            "Aantal",
            "Btw-code",
            "Bedrag",
        ]
    )
    writer.writerows(result)

    return response


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "customer_formatted", "date", "total_formatted")
    ordering = ("-date",)
    search_fields = (
        "transaction_id",
        "customer__first_name",
        "customer__prefix",
        "customer__last_name",
    )
    list_filter = (TransactionDateListFilter,)
    inlines = [SubTransactionInline, SubPurchaseInline]
    autocomplete_fields = ["customer"]
    actions = [export_to_csv]
    fieldsets = (
        ("Information", {"fields": ("transaction_id", "date", "customer")}),
        ("Meta", {"fields": ("created", "last_modified")}),
    )
    readonly_fields = ("transaction_id", "created", "last_modified")

    @admin.display(description="Total")
    def total_formatted(self, obj):
        return f"€ {obj.total()}"

    @admin.display(description="Customer")
    def customer_formatted(self, obj):
        link = reverse(
            f"admin:{obj.customer._meta.app_label}_{obj.customer._meta.model_name}_change",
            args=[obj.customer.id],
        )
        return format_html('<a href="{}">{}</a>', link, str(obj.customer))


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction, TransactionAdmin)
