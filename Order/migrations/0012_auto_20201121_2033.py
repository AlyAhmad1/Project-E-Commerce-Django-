# Generated by Django 3.1.3 on 2020-11-21 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0011_auto_20201121_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_bill',
            name='All_fields',
            field=models.SlugField(max_length=300, null=True),
        ),
    ]