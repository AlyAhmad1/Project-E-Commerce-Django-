# Generated by Django 3.1.3 on 2020-11-21 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0022_auto_20201120_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 11, 21, 14, 27, 8, 218880)),
        ),
    ]