# Generated by Django 4.1.7 on 2024-02-22 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MakroInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100)),
                ('invoice_date', models.DateField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Makro Invoices',
                'ordering': ['-invoice_date'],
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('account_code', models.IntegerField(default=8310, help_text='account code (grootboekrekeningnummer) for income')),
                ('vat_percentage', models.IntegerField(default=0, help_text='BTW percentage of the transaction.')),
                ('image_url', models.CharField(blank=True, max_length=2083)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('product_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.productgroup')),
            ],
        ),
        migrations.CreateModel(
            name='MakroInvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('makro_bon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.makroinvoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
