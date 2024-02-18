from django.db import models
import dbsettings

# Create your models here.
class ProductGroup(models.Model):
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    article_number = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    account_code = models.IntegerField(default=8310, help_text="""account code (grootboekrekeningnummer) for income""") # TODO: make default account code a setting
    vat_percentage = models.IntegerField(help_text="""BTW percentage of the transaction.""", default=0) # TODO: make default percentage code a setting
    image_url = models.CharField(max_length=2083, blank=True)
    product_group = models.ForeignKey(ProductGroup, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    
class ProductSettings(dbsettings.Group):
    default_VAT_value = dbsettings.PositiveIntegerValue()

product_settings = ProductSettings("Product Settings")