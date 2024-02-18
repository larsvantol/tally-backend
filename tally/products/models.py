from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# Create your models here.
class ProductGroup(models.Model):
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    article_number = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083, blank=True)
    product_group = models.ForeignKey(ProductGroup, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class MakroInvoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_number}"

    class Meta:
        verbose_name_plural = "Makro Invoices"
        ordering = ["-invoice_date"]


class MakroInvoiceItem(models.Model):
    makro_bon = models.ForeignKey(MakroInvoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {self.makro_bon.invoice_number}"


@receiver(pre_delete, sender=MakroInvoiceItem)
def delete_makrobonitem_hook(sender, instance, using, **kwargs):
    print(f"Deleting {instance.quantity} of {instance.product.name}")
    instance.product.stock -= instance.quantity
    instance.product.save()
