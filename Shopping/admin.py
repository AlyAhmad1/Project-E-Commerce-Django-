from django.contrib import admin
from .models import Logs, Item, Comment, Cart, Stock, Rating, RecommendedAdmin, RecommendedRating, RecommendedSearch,RecommendUser

# Register your models here.

admin.site.register(Logs)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Stock)
admin.site.register(Rating)
admin.site.register(RecommendedRating)
admin.site.register(RecommendedSearch)
admin.site.register(RecommendedAdmin)
admin.site.register(RecommendUser)
