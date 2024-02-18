from datetime import datetime

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import site
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.views.generic.detail import DetailView

from .makro_bonnen import filter_list, read_makro_invoice, to_list
from .models import MakroInvoice, MakroInvoiceItem, Product, ProductGroup


# Filter for stock using simplelistfilter
class StockFilter(admin.SimpleListFilter):
    title = "stock"
    parameter_name = "stock"

    def lookups(self, request, model_admin):
        return (
            ("0-10", "Less than 10"),
            ("10-50", "10-50"),
            ("50-100", "50-100"),
            ("100-500", "100-500"),
            ("500>", "Greater than 500"),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        elif self.value() == "500>":
            return queryset.filter(stock__gte=500)
        else:
            min, max = self.value().split("-")
            return queryset.filter(stock__gte=min, stock__lte=max)


class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    fieldsets = (
        ("Name", {"fields": ("name",)}),
        ("Meta", {"fields": ("created", "last_modified")}),
    )
    readonly_fields = ("created", "last_modified")


class PDF_upload(forms.Form):
    upload_makro_invoice = forms.FileField()


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "article_number",
        "name",
        "product_group_formatted",
        "price_formatted",
        "stock",
        "image",
    )
    list_filter = ("product_group", StockFilter)
    search_fields = ("name", "article_number")
    fieldsets = (
        ("Name", {"fields": ("article_number", "name", "product_group")}),
        ("Details", {"fields": ("price", "stock", "image_url")}),
        ("Meta", {"fields": ("created", "last_modified")}),
    )
    readonly_fields = ("created", "last_modified")

    def image(self, obj):
        return format_html(
            '<img src="{0}" style="width: 45px; height:45px; object-fit: contain;" />'.format(
                obj.image_url
            )
        )

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload_makro/", self.upload_makro, name="upload_makro"),
            path("add_bulk/", self.add_bulk, name="add-bulk"),
        ]
        return new_urls + urls

    def upload_makro(self, request):
        form = PDF_upload()
        admin_site: AdminSite = site
        context = admin_site.each_context(request)
        context["form"] = form

        if request.method == "POST":
            pdf = request.FILES["upload_makro_invoice"]

            if not pdf.name.endswith(".pdf"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)
            invoice_data, makro_items = read_makro_invoice(pdf)
            request.session["makro_items"] = to_list(makro_items)
            request.session["invoice_data"] = invoice_data

            url = reverse("admin:add-bulk")

            if MakroInvoice.objects.filter(invoice_number=invoice_data["invoice_number"]).exists():
                messages.warning(
                    request, "This invoice has already been uploaded, maybe drink less Ketel?"
                )
                return HttpResponseRedirect(url)

            return HttpResponseRedirect(url)

        return render(request, "admin/pdf_upload.html", context)

    def add_bulk(self, request):
        ProductFormSet = forms.modelformset_factory(
            Product,
            fields=("article_number", "name", "price", "stock", "image_url", "product_group"),
        )

        if request.method == "POST":
            prod_forms = ProductFormSet(data=request.POST)

            if prod_forms.is_valid():
                invoice_data = request.session["invoice_data"]

                makro_invoice = MakroInvoice.objects.create(
                    invoice_number=invoice_data["invoice_number"],
                    invoice_date=datetime.strptime(invoice_data["invoice_date"], "%d-%m-%Y"),
                )

                for form in prod_forms:
                    try:
                        product = form.save(commit=False)
                        try:
                            ex_product = Product.objects.get(article_number=product.article_number)
                            ex_product.stock = ex_product.stock + product.stock
                            ex_product.price = product.price
                            ex_product.save()
                            MakroInvoiceItem.objects.create(
                                makro_bon=makro_invoice, product=ex_product, quantity=product.stock
                            )
                        except Product.DoesNotExist:
                            product = form.save()
                            MakroInvoiceItem.objects.create(
                                makro_bon=makro_invoice, product=product, quantity=product.stock
                            )
                    except:
                        continue
                return redirect("/admin/products/product")
            else:
                print(prod_forms)

        admin_site: AdminSite = site
        context = admin_site.each_context(request)
        if request.session["makro_items"] and request.session["invoice_data"]:
            formset = ProductFormSet(
                initial=filter_list(request.session["makro_items"]), queryset=Product.objects.none()
            )
            formset.extra = len(request.session["makro_items"])
            context["product_formset"] = formset
            context["invoice_data"] = request.session["invoice_data"]
        else:
            context["product_formset"] = ProductFormSet()

        return render(request, "admin/add_bulk.html", context)

    @admin.display(description="Price")
    def price_formatted(self, obj):
        """
        Formats the price of the product as €xx.xx
        """
        return f"€ {obj.price:.2f}"

    @admin.display(description="Product group")
    def product_group_formatted(self, obj):
        """
        Formats the product group. It returns a link to the products filtered on the specific product group
        """
        # formats the product group with a link to the group filter
        return format_html(
            f'<a href="?product_group__id__exact={obj.product_group.id}">{obj.product_group.name}</a>'
        )


class MakroInvoiceItemInline(admin.TabularInline):
    model = MakroInvoiceItem
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class MakroInvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "invoice_date", "uploaded_at")
    search_fields = ("invoice_number", "invoice_date")
    fieldsets = (
        ("Name", {"fields": ("invoice_number", "invoice_date")}),
        ("Meta", {"fields": ("uploaded_at",)}),
    )
    readonly_fields = ("uploaded_at",)
    inlines = [MakroInvoiceItemInline]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(MakroInvoice, MakroInvoiceAdmin)
