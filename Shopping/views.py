from django.shortcuts import render, redirect
from .forms import FormA, FormB
from .models import Logs, Item, Comment, Cart, Stock, Rating, RecommendedAdmin, RecommendedRating, RecommendedSearch, RecommendUser
from django.contrib import messages
from datetime import datetime
from . import login_required
from .filte import ABC
from django.core.paginator import Paginator
from math import *
import _pickle as pickle


# Create your views here.
class VIEWS:
    def index(self,request):
        form = FormB()
        all_items = Item.objects.all()
        if request.method == 'POST' and request.session.has_key('user'):
            filter = ABC(request.POST, queryset=all_items)
            all_items = filter.qs
            for i in all_items:
                try:
                    r_u = RecommendedSearch(User=request.session['user'] ,title=i.title, Description=i.Description, Price=i.Price, Time=i.Time, Picture=i.Picture, Quantity=i.Quantity)
                    r_u.save()
                except:
                    continue
        else:
            filter = ABC(request.POST, queryset=all_items)
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
                messages.error(request, 'Error Tittle Already Existed')
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
        messages.error(request,'Error in Adding Item try Again')
        return redirect('HOME')

    def del_item(self, request, pk):
        Item.objects.filter(title=pk).delete()
        Stock.objects.filter(title=pk).delete()
        return redirect('HOME')

    def details(self,request,pk):
        try:
            global se, User
            rated = True
            if request.method == 'POST':
                item = request.POST['item']
                user = request.session['user']
                value = request.POST['rating']
                R = Rating(user=user, item=item, value=value)
                R.save()
            if request.session.has_key('user') and request.session['user'] == 'admin':
                    se = True
                    User = True
                    rated = True
                    L = False
            elif request.session.has_key('user'):
                se = True
                User = False
                L = request.session['user']
                Rates = Rating.objects.filter(user=request.session['user'],item=pk).first()
                if Rates:
                    rated = range(0, Rates.value)
                else:
                    rated = False
            else:
                rated = True
                se = False
                User = False
                L = False
            All = Item.objects.filter(title=pk)
            All1 = Stock.objects.filter(title=pk)
            comments = Comment.objects.filter(title=pk)
            form = FormB()
            R_check = Rating.objects.filter(item=pk).all()
            f=s=t=fo=fi=0
            for i in R_check:
                if i.value==1:
                    f+=1
                elif i.value==2:
                    s+=1
                elif i.value==3:
                    t+=1
                elif i.value==4:
                    fo+=1
                elif i.value==5:
                    fi+=1
            R_star = [f,s,t,fo,fi]
            # Rating recommendation.
            try:
                if (fi>f and fi>s and fi>t and fi>fo) or (fo>f and fo>s and fo>t and fo>fi):
                    r_u = RecommendedRating(title=All[0].title, Description=All[0].Description, Price=All[0].Price, Time=All[0].Time, Picture=All[0].Picture, Quantity=All[0].Quantity)
                    r_u.save()
                elif (s>f and s>fi and s>t and s>fo) or (t>f and t>s and t>fo and t>fi)or (f>s and f>t and f>fo and f>fi):
                    if RecommendedRating(title=All[0].title):
                        RecommendedRating(title=All[0].title).delete()
            except Exception as e:
                print(e)
                pass

            R = RecommendUser.objects.all()
            SSS = []
            for i in R:
                K = pickle.loads(i.RP)
                for j in K:
                    if j == pk:
                        SSS.append(K)
                        break
            slider_items = []
            for J in SSS:
                for k in J:
                    if k==pk:
                        continue
                    try:
                        z=Item.objects.filter(title=k).first()
                    except:
                        continue
                    slider_items.append(z)
            Data = {'L':L, 'All':All, 'comments':comments,'form':form,'All1':All1, 'check': se,'User': User, 'Rated': rated, 'R_star':R_star, 'slider_items':slider_items}
        except:
            messages.error(request,'Error in Loading Item May Be it is no More Existed in Stock')
            return redirect('HOME')
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
        if request.method == 'POST':
            name = request.POST['title']
            sell_rate = request.POST['Price']
            available = request.POST['Quantity']
            buy_rate = request.POST['buy']
            d = Stock.objects.get(title=name)
            d.title = name
            d.Buy_rate = buy_rate
            d.Available = available
            d.Sell = sell_rate
            d.Quantity += int(available)
            d.save()
            messages.error(request,f'Updated Field {name}')
        form = FormB()
        All_items = Stock.objects.get_queryset().order_by('title')
        filter = ABC(request.GET, queryset=All_items)
        All_items = filter.qs

        paginator = Paginator(All_items, 10)
        page = request.GET.get('page')
        All_items = paginator.get_page(page)

        Data = {"All_items":All_items, 'form':form, 'filter':filter}
        return render(request,'Shopping/stock.html', Data)

    def up_stock(self, request,n,sp,q,br):
        data = {'name':n, 'price':sp, 'available':q, 'buy_rate':br}
        return render(request, 'Shopping/update_stock.html', data)

    def del_stock(self, request, name):
        Stock.objects.get(title=name).delete()
        Item.objects.get(title=name).delete()
        Rating.objects.get(item=name).delete()
        RecommendedSearch.objects.get(title=name).delete()
        RecommendedAdmin.objects.get(title=name).delete()
        RecommendedRating.objects.get(title=name).delete()

        messages.error(request, f'Deleted Field {name}')
        return redirect('stock')


class ForYou:
    def all_items(self, request):
        A = RecommendedAdmin.objects.all()
        B = RecommendedRating.objects.all()
        C = RecommendedSearch.objects.all()
        allProds = [[A,'Hot-Offers'],[B,'Products Have High Rating'],[C,'Products Related to your search']]
        if request.session.has_key('user'):
            user = request.session['user']
        else:
            user = ''
        data = {'allProds':allProds, 'user':user}
        return render(request, 'Shopping/foryou.html', data)

    # recommended by admin
    def R_A(self,request, name):
        all = Item.objects.get(title=name)
        all.Recommended = True
        all.save()
        R = RecommendedAdmin(title=all.title, Description=all.Description,Price=all.Price,Time=all.Time,Picture=all.Picture, Quantity=all.Quantity)
        RecommendedAdmin.save(R)
        messages.error(request, f'{name} Added in Recommended List')
        return redirect('HOME')

    def del_R_A(self,request,name):
        RecommendedAdmin.objects.filter(title=name).delete()
        R = Item.objects.get(title=name)
        R.Recommended = False
        R.save()
        messages.error(request, f'{name} Removed from Recommended List')
        return redirect('HOME')
