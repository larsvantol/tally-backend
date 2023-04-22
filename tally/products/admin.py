from django.contrib import messages
from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html

from .makro_bonnen import read_makro_invoice, to_list
from .models import Product, ProductGroup
from django.views.generic.detail import DetailView
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import site

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

class PDF_upload(forms.Form):
    upload_makro_invoice = forms.FileField()

class ProductAdmin(admin.ModelAdmin):
    list_display = ('article_number','name', 'product_group_formatted', 'price_formatted', 'stock')
    list_filter = ('product_group', StockFilter)
    search_fields = ('name',)
    fieldsets = (
        ('Name', {
            'fields': ('article_number', 'name', 'product_group')
        }),
        ('Details', {
            'fields': ('price', 'stock', 'image_url')
        }),
        ('Meta', {
            'fields': ('created', 'last_modified')
        }),
    )
    readonly_fields = ('created', 'last_modified')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_makro/', self.upload_makro, name="upload_makro"), path('add_bulk/', self.add_bulk, name="add-bulk")]
        return new_urls + urls
    
    def upload_makro(self, request):
        form = PDF_upload()
        admin_site: AdminSite = site
        context = admin_site.each_context(request)
        context['form'] = form

        if request.method == "POST":
            pdf = request.FILES["upload_makro_invoice"]
            
            if not pdf.name.endswith('.pdf'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            makro_items = read_makro_invoice(pdf)
            request.session['makro_items'] = to_list(makro_items)

            url = reverse('admin:add-bulk')
            return HttpResponseRedirect(url)
        
        return render(request, "admin/pdf_upload.html", context)
    
    def add_bulk(self, request):
        ProductFormSet = forms.modelformset_factory(
            Product, fields=("article_number", "name", "price", "stock", "image_url", "product_group")
        )

        if request.method == "POST":
            prod_forms = ProductFormSet(data=request.POST)

            if prod_forms.is_valid():
                prod_forms.save()
                return redirect(reverse("admin:index"))
            else:
                print(prod_forms)

        admin_site: AdminSite = site
        context = admin_site.each_context(request)
        if request.session['makro_items']:
            formset = ProductFormSet(initial=request.session['makro_items'])
            formset.extra = len(request.session['makro_items'])
            context['product_formset'] = formset
        else:
            context['product_formset'] = ProductFormSet()

        return render(request, "admin/add_bulk.html", context)
    

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

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)