from django.urls import path,include
from .views import Order, Bill
O = Order()
B = Bill()

urlpatterns = [
    path('', O.make_order, name='cart'),
    path('delete_item/<pk>', O.delete_item, name='delete_item'),
    path('checkout', O.checkout, name='checkout'),
    path('bill', B.bills, name='bill'),
    path('checked_out', O.Checked, name='checked_out'),
    path('bill_detail/<bill_number>', B.bill_detail, name='bill_detail'),
]

