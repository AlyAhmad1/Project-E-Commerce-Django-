# Generated by Django 3.1.6 on 2021-02-18 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0051_recommendedadmin_recommendedrating_recommendedsearch'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Recommended',
            field=models.BooleanField(default=False),
        ),
    ]
