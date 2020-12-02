from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.db import models

# Create your models here.

# Data Contain After CheckOut
class All_Bill(models.Model):
    User = models.CharField(max_length=50, null=True)          # Who is Buying the item
    Receiver = models.CharField(max_length=50, null=True)      # Who will receive the Item
    City = models.CharField(max_length=50, null=True)
    Address = models.CharField(max_length=50, null=True)
    Zip = models.IntegerField(null=True)
    Name_on_Card = models.CharField(max_length=50,  null=True)
    Credit_card_number= CardNumberField( null=True)
    Exp_Month = models.CharField(max_length=50, null=True)
    Exp_Year = models.IntegerField(null=True)
    CVV = models.IntegerField(null=True)                     # CVV Stands for Cad Verification Value
    Payment = models.CharField(max_length=30, null=True)       # On Delivery / Or By Card
    All_fields = models.BinaryField(max_length=1000,  null=True)  # This is For Storing Items Data Prices/ Pickled Object
    Amount = models.FloatField( null=True)                    # Total Bill
    Date = models.DateField(null=True)
    Bill_number = models.TextField(null=True)
