# Generated by Django 4.1.7 on 2023-05-26 20:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0020_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='customer',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='transactions.customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 26, 20, 50, 52, 852190, tzinfo=datetime.timezone.utc), help_text='Date of the transaction.'),
        ),
    ]
