# Generated by Django 3.1.3 on 2020-11-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0044_stockquantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='Available',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='Sell',
            field=models.IntegerField(default=0),
        ),
    ]
