# Generated by Django 3.1.6 on 2021-03-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0003_item_crousal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Description',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.TextField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='title',
            field=models.TextField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
