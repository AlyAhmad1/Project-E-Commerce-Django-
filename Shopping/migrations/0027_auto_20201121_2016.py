# Generated by Django 3.1.3 on 2020-11-21 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0026_auto_20201121_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 11, 21, 20, 16, 40, 606816)),
        ),
    ]