# Generated by Django 4.1.7 on 2023-03-13 06:30

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_transaction_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subpurchase',
            name='date_created',
        ),
        migrations.AddField(
            model_name='subpurchase',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subpurchase',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='subtransaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subtransaction',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 13, 6, 30, 26, 756238, tzinfo=datetime.timezone.utc), help_text='Date of the transaction.'),
        ),
    ]
