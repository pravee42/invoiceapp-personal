# Generated by Django 4.0.6 on 2022-07-24 11:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_invoice_costumer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='due_date',
            field=models.CharField(default=datetime.date(2022, 7, 24), max_length=100),
        ),
    ]
