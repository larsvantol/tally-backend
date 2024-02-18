# Generated by Django 4.1.7 on 2024-02-18 14:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0009_alter_product_account_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('prefix', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('relation_code', models.IntegerField(help_text='Relation code of the customer.', unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2024, 2, 18, 14, 16, 20, 871727, tzinfo=datetime.timezone.utc), help_text='Date of the transaction.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.customer')),
            ],
        ),
        migrations.CreateModel(
            name='SubTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Description of the transaction.', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount to be deducted.', max_digits=10)),
                ('account_code', models.IntegerField(default=3002, help_text='account code (grootboekrekeningnummer) for income')),
                ('vat_percentage', models.IntegerField(default=0, help_text='BTW percentage of the transaction.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtransactions', to='transactions.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='SubPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, help_text='Price of the product at the time of purchase.', max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subpurchases', to='transactions.transaction')),
            ],
        ),
    ]
