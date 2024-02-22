import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_code', models.IntegerField(help_text='Relation code of the customer.', unique=True)),
                ('sub', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('encrypted_uuid', models.CharField(blank=True, max_length=100, null=True)),
                ('encrypted_code', models.CharField(blank=True, help_text='Code to login, must be 4 digits.', max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=100)),
                ('prefix', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2024, 2, 20, 15, 54, 14, 809316, tzinfo=datetime.timezone.utc), help_text='Date of the transaction.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transactions.customer')),
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
