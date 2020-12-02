from django.contrib import admin
from .models import Logs, Item, Comment, Cart, Stock

# Register your models here.

admin.site.register(Logs)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Stock)
