# Generated by Django 3.1.3 on 2020-11-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0042_auto_20201121_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('title', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Buy_rate', models.IntegerField()),
                ('Sell_rate', models.IntegerField()),
                ('Quantity', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='Quantity',
            field=models.IntegerField(null=True),
        ),
    ]
