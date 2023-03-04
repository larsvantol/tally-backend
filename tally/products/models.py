from django.db import models

# Create your models here.
class ProductGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    product_group = models.ForeignKey(ProductGroup, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name