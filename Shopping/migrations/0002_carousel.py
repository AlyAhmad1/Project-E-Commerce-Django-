# Generated by Django 3.1.6 on 2021-03-15 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('title', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Description', models.CharField(max_length=200)),
                ('Price', models.FloatField()),
                ('Picture', models.ImageField(default='', upload_to='Shopping/static')),
            ],
        ),
    ]
