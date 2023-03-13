from django.db import models

# Create your models here.
class ProductGroup(models.Model):
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083, blank=True)
    product_group = models.ForeignKey(ProductGroup, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'