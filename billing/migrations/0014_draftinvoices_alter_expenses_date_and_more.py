# Generated by Django 4.0.6 on 2022-08-13 07:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0013_alter_invoice_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftInvoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.CharField(default='2022-08-13', max_length=100),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.CharField(default=datetime.date(2022, 8, 13), max_length=100),
        ),
        migrations.AlterField(
            model_name='payments',
            name='date_created',
            field=models.CharField(default='2022-08-13', max_length=100),
        ),
    ]
