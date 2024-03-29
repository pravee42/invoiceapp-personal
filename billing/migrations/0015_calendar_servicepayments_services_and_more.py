# Generated by Django 4.0.6 on 2022-08-25 00:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0014_draftinvoices_alter_expenses_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
                ('task', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('contact_number', models.CharField(max_length=100)),
                ('costumer_name', models.CharField(max_length=100)),
                ('completed', models.CharField(default='false', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ServicePayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_number', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('ammount', models.IntegerField(default=0)),
                ('refrence_number', models.CharField(default='Cash', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_number', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('ammount', models.IntegerField(default=0)),
                ('paid', models.IntegerField(default=0)),
                ('costumer_name', models.CharField(default='General Service', max_length=100)),
                ('contact_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.CharField(default='2022-08-25', max_length=100),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.CharField(default=datetime.date(2022, 8, 25), max_length=100),
        ),
        migrations.AlterField(
            model_name='payments',
            name='date_created',
            field=models.CharField(default='2022-08-25', max_length=100),
        ),
    ]
