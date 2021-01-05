from django.shortcuts import render, redirect
from .forms import FormA, FormB
from .models import Logs, Item, Comment, Cart, Stock
from django.contrib import messages
from datetime import datetime
from . import login_required
from .filte import ABC
from django.core.paginator import Paginator


# Create your views here.
class VIEWS:
    def index(self,request):
        form = FormB()
        all_items = Item.objects.all()
        filter = ABC(request.GET, queryset=all_items)
        all_items = filter.qs

        paginator = Paginator(all_items,10)
        page = request.GET.get('page')
        all_items = paginator.get_page(page)

        if request.session.has_key('user'):
            se = request.session['user']
            if se == 'admin':
                data = {'form': form,'All_items': all_items, 'se': se, 'filter':filter}
                return render(request,'Shopping/Admin_dashboard.html', data)
            user = True
        else:
            se = False
            user = False
        data = {'form': form, 'se': se, 'All_items': all_items, 'User': user, 'filter':filter}
        return render(request, 'Shopping/Index.html',data)

    def add_Item(self,request):
        all = FormB(request.POST,request.FILES)
        if all.is_valid():
            query = Item.objects.filter(title=request.POST['title'])
            if query is None:
                messages.error(request,'Item Already Existed')
                return redirect('HOME')

            data = Item(title=request.POST['title'],Description=request.POST['Description'],Price=request.POST['Price'],
                       Picture=request.FILES['Image'], Time = datetime.now(), Quantity = request.POST['Quantity'])
            Item.save(data)
            Sell_Price = (int(request.POST['Price']) * 0.1) + int(request.POST['Price'])
            S = Stock(title= request.POST['title'], Buy_rate= request.POST['Price'],
                      Sell_rate=Sell_Price, Quantity= request.POST['Quantity'],Available=request.POST['Quantity'])
            Stock.save(S)
            messages.error(request,'ITEM ADDED SUCCESSFULLY')
            return redirect('HOME')
        messages.error(request,'Error in Adding Item try Again ')
        return redirect('HOME')

    def del_item(self, request, pk):
        Item.objects.filter(title=pk).delete()
        Stock.objects.filter(title=pk).delete()
        return redirect('HOME')

    def details(self,request,pk):
        global se, User
        if request.session.has_key('user') and request.session['user'] == 'admin':
            # c = request.session['user']
            # if c == 'admin':
                se = True
                User = True
        elif request.session.has_key('user'):
            se = True
            User = False
        else:
            se = False
            User = False
        All = Item.objects.filter(title=pk)
        All1 = Stock.objects.filter(title=pk)
        comments = Comment.objects.filter(title=pk)
        form = FormB()
        Data = {'All':All, 'comments':comments,'form':form,'All1':All1, 'check': se,'User':User}
        return render(request,'Shopping/Details.html',Data)

    def comment(self, request, pk):
        if request.session.has_key('user'):
            if request.method=='POST':
                comment = request.POST['com']
                title = pk
                Data = Comment(title=title,comment=comment,commenter=request.session['user'])
                Comment.save(Data)
                return redirect('Details', pk=pk)
            return redirect('HOME')
        else:
            messages.error(request, 'Before Commenting You Need to Login first')
            return redirect('login')

    def delete_comment(self,request,pk,t):
            Comment.objects.filter(comment=pk).delete()
            return redirect('Details', pk=t)

    @login_required
    def add_to_cart(self,request):
        if request.method == 'POST':
            title = request.POST['title']
            Price = request.POST['Price']
            Quantity = request.POST['Quantity']
            user = request.session['user']
            Total = float(Quantity) * float(Price)
            Data = Cart(title=title,Price=Price,Quantity=Quantity,Total=Total, user=user)
            Data.save()
            return redirect('Details', pk=title)


class Log:
    def signup(self,request):
        if request.session.has_key('user'):
            messages.error(request,'Please First Logout Then Signup Thanks')
            return redirect('HOME')
        else:
            form=FormA()
            Data = {'form':form, 'signup':True}
            return render(request, 'Shopping/login.html', Data)

    # it is for saving User Sign-Up
    def submit(self, request):
        if request.method == 'POST':
            Items = FormA(request.POST)
            if Items.is_valid():
                All = Logs.objects.all()
                for i in range(0,len(All)):
                    if All[i].Email==request.POST['Email']:
                        messages.error(request,'USER ALREADY EXISTED PLEASE TRY ANOTHER EMAIL')
                        return redirect('signup')
                F = Logs(Email=request.POST['Email'],Password=request.POST['Password'])
                Logs.save(F)
                request.session['user'] = str(request.POST['Email']).split('@')[0]
                return redirect('HOME')
        return redirect('signup')

    def login(self,request):
        if request.session.has_key('user'):
            messages.error(request,'You Are Already Login')
            return redirect('HOME')
        else:
            form=FormA()
            Data = {'form':form, 'signup':False}
            return render(request, 'Shopping/login.html', Data)

    def check(self,request):
        All = Logs.objects.all()
        if request.method == 'POST':
            E=request.POST['Email']
            P=request.POST['Password']
            for i in range(0,len(All)):
                if All[i].Email==E and All[i].Password==P:
                    request.session['user'] = str(All[i].Email).split('@')[0]
                    return redirect('HOME')
            return redirect('login')

    def logout(self, request):
        del request.session['user']
        messages.error(request,'You are Logged Out')
        return redirect('HOME')


class StockManage:
    available = 0
    sell = 0

    def stock(self, request):

        form = FormB()
        All_items = Stock.objects.get_queryset().order_by('title')
        filter = ABC(request.GET, queryset=All_items)
        All_items = filter.qs

        paginator = Paginator(All_items, 10)
        page = request.GET.get('page')
        All_items = paginator.get_page(page)

        Data = {"All_items":All_items, 'form':form, 'filter':filter}
        return render(request,'Shopping/stock.html', Data)


