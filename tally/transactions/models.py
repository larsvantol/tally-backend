from django.db import models
from products.models import Product
import uuid

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    relation_code = models.IntegerField(null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.relation_code) + " - " + self.first_name + " " + (self.prefix + " " if self.prefix else "") + self.last_name
    
class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def total(self):
        total = 0
        for subtransaction in self.subtransaction_set.all():
            total += subtransaction.amount
        for subpurchase in self.subpurchase_set.all():
            total += subpurchase.price * subpurchase.quantity
        return total

    def __str__(self):
        return str(self.transaction_id)
    
class SubTransaction(models.Model):
    description = models.CharField(max_length=100, help_text="""Description of the transaction.""")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="""Amount to be deducted.""")
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    
    
class SubPurchase(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="""Price of the product at the time of purchase.""")

    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name