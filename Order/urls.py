from django.urls import path
from .views import Order, Bill, ShippedOrder
O = Order()
B = Bill()
S = ShippedOrder()

urlpatterns = [
    path('', O.make_order, name='cart'),
    path('delete_item/<pk>', O.delete_item, name='delete_item'),
    path('checkout', O.checkout, name='checkout'),
    path('bill', B.bills, name='bill'),
    path('checked_out', O.Checked, name='checked_out'),
    path('bill_detail/<bill_number>', B.bill_detail, name='bill_detail'),
    path('orders', S.orders, name='orders'),  # for admin to view all orders
    path('shipped', S.shipped, name='shipped'),  # for admin to view all shipped orders
    path('Dispatch/<user>/<bill>', S.Dispatch, name='Dispatch'),  # for admin to ship an order
    path('orders/detail/<user>/<bill>', S.order_detail, name='OrderDetail'), # for admin to view details of placed Order
]

