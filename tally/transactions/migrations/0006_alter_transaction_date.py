# Generated by Django 4.1.7 on 2023-03-12 11:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 12, 11, 19, 15, 584569, tzinfo=datetime.timezone.utc), help_text='Date of the transaction.'),
        ),
    ]