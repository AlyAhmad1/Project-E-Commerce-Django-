# Generated by Django 3.1.6 on 2021-03-02 11:29

import creditcards.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='All_Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.CharField(max_length=50, null=True)),
                ('Receiver', models.CharField(max_length=50, null=True)),
                ('City', models.CharField(max_length=50, null=True)),
                ('Address', models.CharField(max_length=50, null=True)),
                ('Zip', models.IntegerField(null=True)),
                ('Name_on_Card', models.CharField(max_length=50, null=True)),
                ('Credit_card_number', creditcards.models.CardNumberField(max_length=25, null=True)),
                ('Exp_Month', models.CharField(max_length=50, null=True)),
                ('Exp_Year', models.IntegerField(null=True)),
                ('CVV', models.IntegerField(null=True)),
                ('Payment', models.CharField(max_length=30, null=True)),
                ('All_fields', models.BinaryField(max_length=1000, null=True)),
                ('Amount', models.FloatField(null=True)),
                ('Date', models.DateField(null=True)),
                ('Bill_number', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dispatched',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Receiver_Name', models.CharField(max_length=50)),
                ('Amount', models.IntegerField()),
                ('Date', models.DateField()),
                ('Bill_number', models.TextField(null=True)),
                ('Shipped_Date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='PendingOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Receiver_Name', models.CharField(max_length=50)),
                ('Amount', models.IntegerField()),
                ('Date', models.DateField()),
                ('Bill_number', models.TextField(null=True)),
            ],
        ),
    ]
