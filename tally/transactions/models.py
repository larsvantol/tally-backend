from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from products.models import Product
import uuid


# Create your models here.
class Customer(models.Model):
    relation_code = models.IntegerField(
        help_text="""Relation code of the customer.""", unique=True
    )

    sub = models.CharField(max_length=100, unique=True, blank=True, null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="customer"
    )

    encrypted_uuid = models.CharField(max_length=100, blank=True, null=True)
    encrypted_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="""Code to login, must be 4 digits.""",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.relation_code) + " - " + self.full_name()

    def check_uuid(self, uuid):
        return check_password(uuid, self.encrypted_uuid)

    def check_code(self, code):
        return check_password(code, self.encrypted_code)

    def verify_encrypted_code_requirements(self, code):
        return len(code) == 4 and code.isnumeric()

    def verify_encrypted_uuid_requirements(self, uuid_to_test, version=None):
        try:
            uuid_obj = uuid.UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    @admin.display(boolean=True)
    def has_uuid(self):
        return not (self.encrypted_uuid == "" or self.encrypted_uuid == None)

    @admin.display(boolean=True)
    def has_code(self):
        return not (self.encrypted_code == "" or self.encrypted_code == None)

    @admin.display(boolean=True)
    def has_user(self):
        return not (self.user == None)

    def hash_uuid(self, uuid):
        return make_password(uuid)

    def hash_code(self, code):
        return make_password(code)

    def full_name(self):
        if self.user == None:
            return "unknown"
        return self.user.first_name + " " + self.user.last_name


class Transaction(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    date = models.DateTimeField(
        default=timezone.now(), help_text="""Date of the transaction."""
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def total(self):
        total = 0
        for subtransaction in SubTransaction.objects.filter(
            transaction=self.transaction_id
        ):
            total += subtransaction.amount
        for subpurchase in SubPurchase.objects.filter(transaction=self.transaction_id):
            total += subpurchase.price * subpurchase.quantity
        return total

    def __str__(self):
        return str(self.transaction_id)

    def export_to_list_exact_format(self):
        # formatting:
        # nieuwe boeking, omschrijving:kopregel, datum, betalingsconditie, relatiecode, grootboekrekening, omschrijving, aantal, btw code, bedrag
        # TODO: make setting for betalingsconditie (DS)
        result = [
            [
                1,
                f"tally transaction {self.transaction_id}",
                self.date.strftime("%d-%m-%Y"),
                "DS",
                self.customer.relation_code,
            ]
        ]
        for subtransaction in SubTransaction.objects.filter(
            transaction=self.transaction_id
        ):
            result.append(
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    subtransaction.account_code,
                    subtransaction.description,
                    "",
                    subtransaction.vat_percentage,
                    subtransaction.amount,
                ]
            )
        for subpurchase in SubPurchase.objects.filter(transaction=self.transaction_id):
            result.append(
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    subpurchase.product.account_code,
                    subpurchase.product.name,
                    subpurchase.quantity,
                    subpurchase.product.vat_percentage,
                    subpurchase.amount(),
                ]
            )
        return result


class SubTransaction(models.Model):
    description = models.CharField(
        max_length=100, help_text="""Description of the transaction."""
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="""Amount to be deducted."""
    )
    account_code = models.IntegerField(
        default=3002, help_text="""account code (grootboekrekeningnummer) for income"""
    )  # TODO: make default account code a setting
    vat_percentage = models.IntegerField(
        help_text="""BTW percentage of the transaction.""", default=0
    )  # TODO: make default vat percentage a setting
    transaction = models.ForeignKey(
        "Transaction", related_name="subtransactions", on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def summary(self) -> tuple:
        return (self.description, self.amount)


class SubPurchase(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="""Price of the product at the time of purchase.""",
    )

    transaction = models.ForeignKey(
        "Transaction", related_name="subpurchases", on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def amount(self):
        return self.price * self.quantity

    def summary(self) -> tuple:
        return (f"{self.quantity}x {self.product.name}", self.amount())

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super(SubPurchase, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name
