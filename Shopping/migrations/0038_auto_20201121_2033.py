# Generated by Django 3.1.3 on 2020-11-21 15:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0037_auto_20201121_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 11, 21, 20, 33, 10, 783368)),
        ),
    ]
