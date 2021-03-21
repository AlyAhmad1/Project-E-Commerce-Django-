from django.urls import path
from . import views
V = views.VIEWS()
V1 =views.Log()
V2 = views.StockManage()
V3 = views.ForYou()
urlpatterns = [
    path('', V.index, name='HOME'),
    path('shop', V.shop, name='shop'),
    path('add_item', V.add_Item, name='add_item'),
    path('del_item/<pk>', V.del_item, name='del_item'),
    path('Details/<pk>', V.details, name='Details1'),
    path('add_comment/<pk>', V.comment, name='add_comment'),
    path('Adding_cart', V.add_to_cart, name='Adding_cart'),
    path('delete_comment/<pk>/<t>', V.delete_comment, name='delete_comment'),
    path('signup', V1.signup, name='signup'),
    path('Submit', V1.submit, name='Submit'),
    path('login', V1.login, name='login'),
    path('check', V1.check, name='check'),
    path('logout', V1.logout, name='logout'),
    path('stock', V2.stock, name='stock'),
    path('updatestock/<n>/<sp>/<q>/<br>', V2.up_stock, name='up_stock'),
    path('deletestock/<name>', V2.del_stock, name='del_stock'),
    path('foryou', V3.all_items, name='foryou'),
    path('recommendedadmin/<name>', V3.R_A, name='recommendedadmin'),
    path('del_recommendedadmin/<name>', V3.del_R_A, name='del_recommendedadmin'),
    path('Carousel/<name>', V3.crousal, name='Carousel'),
    path('del_Carousel/<name>', V3.del_crousal, name='del_Carousel'),
]
