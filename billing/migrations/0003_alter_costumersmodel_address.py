# Generated by Django 4.0.6 on 2022-07-21 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_rename_costumers_costumersmodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costumersmodel',
            name='address',
            field=models.CharField(max_length=1000),
        ),
    ]
