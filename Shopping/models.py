from django.db import models
from datetime import datetime
# Create your models here.


class Logs(models.Model):
    Email = models.EmailField(primary_key=True)
    Password = models.CharField(max_length=8)


class Item(models.Model):
    title = models.CharField(primary_key=True, max_length=20)
    Description = models.CharField(max_length=100)
    Price = models.FloatField()
    Time = models.DateTimeField(null=True)
    Picture = models.ImageField(upload_to='Shopping/static', default='')


class Comment(models.Model):
    title = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)


class Cart(models.Model):
    user = models.CharField(max_length=50, default='')
    title = models.CharField(primary_key=True,max_length=20)
    Quantity = models.FloatField()
    Price = models.FloatField()
    Total = models.FloatField()

