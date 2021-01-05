from django.contrib import admin
from .models import All_Bill, PendingOrder, Dispatched

# Register your models here.
admin.site.register(All_Bill)
admin.site.register(PendingOrder)
admin.site.register(Dispatched)
