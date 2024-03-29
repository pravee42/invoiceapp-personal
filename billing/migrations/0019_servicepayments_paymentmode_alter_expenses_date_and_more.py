# Generated by Django 4.0.6 on 2022-09-11 02:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0018_services_taskid_alter_expenses_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepayments',
            name='paymentmode',
            field=models.CharField(default='cash', max_length=100),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.CharField(default='2022-09-11', max_length=100),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.CharField(default=datetime.date(2022, 9, 11), max_length=100),
        ),
        migrations.AlterField(
            model_name='payments',
            name='date_created',
            field=models.CharField(default='2022-09-11', max_length=100),
        ),
        migrations.AlterField(
            model_name='servicepayments',
            name='refrence_number',
            field=models.CharField(default='01234', max_length=100),
        ),
    ]
