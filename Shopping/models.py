from django.db import models


class Logs(models.Model):
    Email = models.EmailField(primary_key=True)
    Password = models.CharField(max_length=8)


class Item(models.Model):
    title = models.CharField(primary_key=True, max_length=20)
    Description = models.CharField(max_length=100)
    Price = models.FloatField()
    Time = models.DateTimeField(null=True)
    Picture = models.ImageField(upload_to='Shopping/static', default='')
    Quantity = models.IntegerField(null=True)


class Comment(models.Model):
    title = models.CharField(max_length=50) # the post on which user commenting
    comment = models.CharField(max_length=500)
    commenter = models.CharField(max_length=500, null=True)    # user name who is commenting


class Cart(models.Model):
    user = models.CharField(max_length=50, default='')
    title = models.CharField(primary_key=True,max_length=20)
    Quantity = models.FloatField()
    Price = models.FloatField()
    Total = models.FloatField()


class Stock(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    Buy_rate = models.FloatField()
    Sell_rate = models.FloatField()
    Quantity = models.IntegerField()
    Available = models.IntegerField(default=0)
    Sell = models.IntegerField(default=0)
