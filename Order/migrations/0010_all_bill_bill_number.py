# Generated by Django 3.1.3 on 2020-11-21 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0009_all_bill_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_bill',
            name='Bill_number',
            field=models.TextField(null=True),
        ),
    ]