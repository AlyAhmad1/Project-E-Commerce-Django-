from django.urls import path
from . import views
V = views.VIEWS()
V1 =views.Log()
urlpatterns = [
    path('', V.index, name='HOME'),
    path('add_item', V.add_Item, name='add_item'),
    path('delete_item/<pk>', V.delete_item, name='delete_item'),
    path('Details/<pk>', V.details, name='Details'),
    path('add_comment/<pk>', V.comment, name='add_comment'),
    path('Adding_cart', V.add_to_cart, name='Adding_cart'),
    path('delete_comment/<pk>/<t>', V.delete_comment, name='delete_comment'),
    path('signup', V1.signup, name='signup'),
    path('Submit', V1.submit, name='Submit'),
    path('login', V1.login, name='login'),
    path('check', V1.check, name='check'),
    path('logout', V1.logout, name='logout'),
]


