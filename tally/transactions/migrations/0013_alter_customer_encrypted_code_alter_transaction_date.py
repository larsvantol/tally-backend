# Generated by Django 4.1.7 on 2023-05-20 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='encrypted_code',
            field=models.CharField(blank=True, help_text='Code to login, must be 4 digits.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 16, 23, 43, 536027, tzinfo=datetime.timezone.utc), help_text='Date of the transaction.'),
        ),
    ]