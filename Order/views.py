from django.shortcuts import render, redirect
from Shopping.models import Cart
from .models import All_Bill
from django.contrib import messages
import _pickle as pickle
import datetime



# Create your views here.
class Order:
    Bill_ = 0
    def make_order(self, request):
        if request.session.has_key('user'):
            User =request.session['user']
            All = Cart.objects.filter(user=User)
            total = 0
            for i in All:
                total+=i.Total
            Shipping = 100
            Order.Bill_ = total + Shipping
            Data = {'All':All,'User':User,'order_total':total,'Net_Bill':Order.Bill_,'Shipping': Shipping}
            return render(request,'Order/Cart.html', Data)
        else:
            messages.error(request,'You Need to Login First')
            return redirect('login')

    def delete_item(self,request,pk):
        Data = Cart.objects.get(title=pk)
        Order.Bill_ = Order.Bill_ - Data.Total
        Cart.objects.filter(title=pk).delete()

        return redirect('cart')

    # Before Check Out
    def checkout(self,request):
        All = {'Bill':Order.Bill_}
        return render(request,'Order/Checkout.html',All)

    # After CheckOut
    def Checked(self, request):
        if request.session.has_key('user'):
            if request.method == 'POST':
                user = request.session['user']
                Data = Cart.objects.filter(user=user)
                All_items = []
                for i in Data:
                    A = [i.title,i.Price,i.Quantity,i.Total]
                    All_items.append(A)
                    A = []
                Items = pickle.dumps(All_items)
                try:
                    P = request.POST['payment']
                except:
                    P = False
                B_L = All_Bill.objects.filter(User=user)
                if P:
                    Pay = 'On Delivery'
                    D = All_Bill(User=user,Receiver=request.POST['Name'],Address=request.POST['Address'],City=request.POST['City'],
                                 Zip=request.POST['Zip'],
                                 Payment=Pay,All_fields=Items, Amount=Order.Bill_, Date=datetime.datetime.today(),Bill_number=(len(B_L)+1))
                    All_Bill.save(D)
                else:
                    Pay = 'By Card'
                    D = All_Bill(User=user,Receiver=request.POST['Name'],Address=request.POST['Address'],City=request.POST['City'],
                             Zip=request.POST['Zip'],Name_on_Card=request.POST['cardname'],
                             Credit_card_number=request.POST['cardnumber'],
                             Exp_Month=request.POST['expmonth'],CVV=request.POST['cvv'],Exp_Year=request.POST['expyear'],
                             Payment=Pay,All_fields=Items, Amount=Order.Bill_, Date=datetime.datetime.today(),Bill_number=(len(B_L)+1))
                    All_Bill.save(D)
                Cart.objects.filter(user=user).delete()
                return redirect('bill')
            messages.error(request,'Error In Posting Request Try Again')
            return redirect('checked_out')
        messages.error(request,'Session Time Out')
        return redirect('checked_out')


class Bill:
    def bills(self,request):
        if request.session.has_key('user'):
            user = request.session['user']
            All = All_Bill.objects.filter(User=user)
            Data = {'All':All}
            return render(request,'Order/bill.html', Data)

    def bill_detail(self, request, bill_number):
        if request.session.has_key('user'):
            All = All_Bill.objects.filter(User=request.session['user'],Bill_number=bill_number )
            All_items=pickle.loads(All[0].All_fields)
            Data = {'All':All,'All_items':All_items}
            return render(request,'Order/Bill_Detail.html',Data)
