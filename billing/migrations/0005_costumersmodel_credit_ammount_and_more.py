# Generated by Django 4.0.6 on 2022-07-24 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_invoice_invoice_type_alter_payments_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='costumersmodel',
            name='credit_ammount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='costumersmodel',
            name='paid_ammount',
            field=models.IntegerField(default=0),
        ),
    ]
