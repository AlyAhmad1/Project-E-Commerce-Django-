# Generated by Django 3.1.3 on 2021-01-01 19:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0020_dispatched_shipped_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatched',
            name='Shipped_Date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
