# Generated by Django 3.1.3 on 2020-11-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0010_all_bill_bill_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_bill',
            name='All_fields',
            field=models.TextField(max_length=300, null=True),
        ),
    ]
