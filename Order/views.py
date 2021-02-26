from django.http import Http404
from django.shortcuts import render, redirect
from Shopping.models import Cart, Item,Stock, RecommendUser
from .models import All_Bill, PendingOrder, Dispatched
from django.contrib import messages
import _pickle as pickle
import datetime
from Shopping import login_required
from Shopping.forms import FormB
from django.core.paginator import Paginator
from Shopping.filte import ABC
import math

# Create your views here.
class Order:
    Bill_ = 0
    @login_required
    def make_order(self, request):
        User =request.session['user']
        All = Cart.objects.filter(user=request.session['user'])
        total = 0
        for i in All:
            total+=i.Total
        Shipping = 100
        Order.Bill_ = math.ceil(total) + Shipping
        Data = {'All':All,'User':User, 'order_total':math.ceil(total),'Net_Bill':Order.Bill_,'Shipping': Shipping}
        # return render(request,'Order/cart1.html', Data)
        return render(request,'Order/Cart.html', Data)

    def delete_item(self,request,pk):
        Data = Cart.objects.get(title=pk)
        Order.Bill_ = Order.Bill_ - Data.Total
        Cart.objects.filter(title=pk).delete()
        return redirect('cart')

    # Before Check Out
    @login_required
    def checkout(self,request):
        All = {'Bill':Order.Bill_}
        return render(request,'Order/Checkout.html',All)

    # After CheckOut
    @login_required
    def Checked(self, request):
            if request.method == 'POST':
                user = request.session['user']
                Data = Cart.objects.filter(user=user)
                All_items = []
                product_recommend = []
                for i in Data:
                    A = [i.title,i.Price,i.Quantity,i.Total]
                    All_items.append(A)
                    product_recommend.append(i.title)
                    A = []
                Items = pickle.dumps(All_items)
                product = pickle.dumps(product_recommend)

                try:
                    P = request.POST['payment']
                except:
                    P = False
                B_L = All_Bill.objects.filter(User=user)
                try:
                    Bill.Quantity_clear(Items)
                except Exception as e:
                    message = f'Sorry Selected Quantity of {e} is not Available Update it in Cart'
                    messages.error(request,message)
                    return redirect('cart')

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

                # Saving for Products Recommendation
                C = RecommendUser(RP=product)
                RecommendUser.save(C)

                Order.AdminOrder(user, Order.Bill_, datetime.datetime.today(),(len(B_L)+1))
                Cart.objects.filter(user=user).delete()
                return redirect('bill')
            messages.error(request,'Error In Posting Request Try Again')
            return redirect('checked_out')

    @classmethod
    def AdminOrder(self, name, amount, date, bill):
        d = PendingOrder(Receiver_Name=name, Amount=amount, Date=date, Bill_number=bill)
        d.save()


class Bill:
    @login_required
    def bills(self,request):
        # if request.session.has_key('user'):
            user = request.session['user']
            All = All_Bill.objects.filter(User=user)
            Data = {'All':All,'user':user}
            return render(request,'Order/bill.html', Data)

    def bill_detail(self, request, bill_number):
            All = All_Bill.objects.filter(User=request.session['user'], Bill_number=bill_number)
            All_items = pickle.loads(All[0].All_fields)
            Data = {'All':All,'All_items':All_items}
            return render(request, 'Order/Bill_Detail.html', Data)

    @classmethod
    def Quantity_clear(cls,items):
        All = pickle.loads(items)
        for i in All:
            title = i[0]
            Purchase_Quantity = i[2]
            Item_data=Stock.objects.get(title=title)
            Available = Item_data.Available
            if Available < Purchase_Quantity:
                raise Exception(title)
            Available = Available - Purchase_Quantity
            Sell = int(Item_data.Sell) + Purchase_Quantity
            Item_data.Available = Available
            Item_data.Sell = Sell
            Item_data.save()


class ShippedOrder:
    def orders(self, request):
        form = FormB()
        All_items = PendingOrder.objects.all().order_by('id')
        filter = ABC(request.GET, queryset=All_items)
        All_items = filter.qs

        paginator = Paginator(All_items, 10)
        page = request.GET.get('page')
        All_items = paginator.get_page(page)

        data = {'All_items': All_items,'form':form, 'filter':filter}
        return render(request, 'Shopping/orders.html', data)

    def order_detail(self, request, user, bill):
        D = All_Bill.objects.filter(User=user, Bill_number = bill )
        All_items = pickle.loads(D[0].All_fields)
        Data = {'All':D,'All_items': All_items}
        return render(request, 'Order/Bill_Detail.html', Data)

    def Dispatch(self, request, user, bill):
        d = PendingOrder.objects.filter(Receiver_Name=user, Bill_number=bill)
        ShippedOrder.Dis(d[0].Receiver_Name,d[0].Amount, d[0].Date,d[0].Bill_number)
        d.delete()
        return redirect('shipped')

    def shipped(self, request):
        form = FormB()
        All_items = Dispatched.objects.all().order_by('id')
        filter = ABC(request.GET, queryset=All_items)
        All_items = filter.qs
        paginator = Paginator(All_items, 10)
        page = request.GET.get('page')
        All_items = paginator.get_page(page)
        data = {'All_items': All_items,'form':form, 'filter':filter}
        return render(request, 'Shopping/shipped.html', data)


    @classmethod
    def Dis(self, name, amount, date, bill):
        d = Dispatched(Receiver_Name=name, Amount=amount, Date=date, Bill_number=bill)
        d.save()





