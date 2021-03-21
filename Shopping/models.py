from django.db import models


class Logs(models.Model):
    Email = models.EmailField(primary_key=True)
    Password = models.CharField(max_length=8)


class Item(models.Model):
    title = models.TextField(primary_key=True, max_length=50)
    Description = models.TextField(max_length=200)
    Price = models.FloatField()
    Time = models.DateTimeField(null=True)
    Picture = models.ImageField(upload_to='Shopping/static', default='')
    Quantity = models.IntegerField(null=True)
    Recommended = models.BooleanField(default=False)
    Crousal = models.BooleanField(default=False)


class RecommendedAdmin(models.Model):
    title = models.CharField(primary_key=True, max_length=50)
    Description = models.CharField(max_length=200)
    Price = models.FloatField()
    Time = models.DateTimeField(null=True)
    Picture = models.ImageField(upload_to='Shopping/static', default='')
    Quantity = models.IntegerField(null=True)


class RecommendedRating(models.Model):
    title = models.CharField(primary_key=True, max_length=50)
    Description = models.CharField(max_length=200)
    Price = models.FloatField()
    Time = models.DateTimeField(null=True)
    Picture = models.ImageField(upload_to='Shopping/static', default='')
    Quantity = models.IntegerField(null=True)


class RecommendedSearch(models.Model):
    title = models.CharField(primary_key=True, max_length=50)
    Description = models.CharField(max_length=200)
    Price = models.FloatField()
    Time = models.DateTimeField(null=True)
    Picture = models.ImageField(upload_to='Shopping/static', default='')
    Quantity = models.IntegerField(null=True)
    User = models.CharField(max_length=100, null=True)


class RecommendUser(models.Model):
    RP = models.BinaryField(max_length=1000)


class Comment(models.Model):
    title = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)
    commenter = models.CharField(max_length=500, null=True)


class Cart(models.Model):
    user = models.CharField(max_length=50, default='')
    title = models.CharField(primary_key=True, max_length=50)
    Quantity = models.FloatField()
    Price = models.FloatField()
    Total = models.FloatField()


class Stock(models.Model):
    title = models.TextField(max_length=50, primary_key=True)
    Buy_rate = models.FloatField()
    Sell_rate = models.FloatField()
    Quantity = models.IntegerField()
    Available = models.IntegerField(default=0)
    Sell = models.IntegerField(default=0)


class Rating(models.Model):
    user = models.CharField(max_length=50)
    value = models.IntegerField()
    item = models.CharField(max_length=200)


class Carousel(models.Model):
    title = models.CharField(primary_key=True, max_length=50)
    Description = models.CharField(max_length=200)
    Price = models.FloatField()
    Picture = models.ImageField(upload_to='Shopping/static', default='')
