from django.db import models
from django.utils import timezone
from products.models import Product
import uuid

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    relation_code = models.IntegerField(help_text="""Relation code of the customer.""", unique=True)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.relation_code) + " - " + self.first_name + " " + (self.prefix + " " if self.prefix else "") + self.last_name
    
    def full_name(self):
        return self.first_name + " " + (self.prefix + " " if self.prefix else "") + self.last_name
    
class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now(), help_text="""Date of the transaction.""")

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def total(self):
        total = 0
        for subtransaction in SubTransaction.objects.filter(transaction=self.transaction_id):
            total += subtransaction.amount
        for subpurchase in SubPurchase.objects.filter(transaction=self.transaction_id):
            total += subpurchase.price * subpurchase.quantity
        return total

    def __str__(self):
        return str(self.transaction_id)
    
class SubTransaction(models.Model):
    description = models.CharField(max_length=100, help_text="""Description of the transaction.""")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="""Amount to be deducted.""")
    transaction = models.ForeignKey('Transaction', related_name='subtransactions', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def summary(self) -> tuple:
        return (self.description, self.amount)
    
    
class SubPurchase(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="""Price of the product at the time of purchase.""")

    transaction = models.ForeignKey('Transaction', related_name='subpurchases', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def amount(self):
        print(f'price: {self.price}, quantity: {self.quantity} = {self.price * self.quantity}')
        return self.price * self.quantity
    
    def summary(self) -> tuple:
        return (f'{self.quantity}x {self.product.name}', self.amount())
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super(SubPurchase, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name