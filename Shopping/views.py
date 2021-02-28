from django.http import HttpResponse
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
            # Products Related to your search
            C = RecommendedSearch.objects.filter(User=request.session['user'])
            if len(C) == 0:
                Z = [[],'']
            else:
                Z = [C,'Products Related to your search']
        else:
            se = False
            user = False
            C =[]
            Z = [C,'']
        # Hot-Offers
        A = RecommendedAdmin.objects.all()
        # Products Have High Rating
        B = RecommendedRating.objects.all()


        if len(B) == 0:
            YY = [[],'']
        else:
            YY = [B,'Products Have High Rating']
        if len(A) == 0:
            XX = [[],'']
        else:
            XX = [A,'Hot Offer']

        allProds = [XX,YY,Z]
        data = {'form': form, 'se': se, 'All_items': all_items, 'User': user, 'filter':filter, 'allProds':allProds}
        return render(request, 'Shopping/index1.html',data)

    def shop(self, request):
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
        paginator = Paginator(all_items,15)
        page = request.GET.get('page')
        all_items = paginator.get_page(page)
        if request.session.has_key('user'):
            se = request.session['user']
            if se == 'admin':
                # data = {'form': form,'All_items': all_items, 'se': se, 'filter':filter}
                # return render(request,'Shopping/Admin_dashboard.html', data)
                pass
            user = True
        else:
            se = False
            user = False
        data = {'form': form,'All_items':all_items, 'User':user, 'filter':filter, 'se':se}
        return render(request, 'Shopping/shop.html', data)


    def add_Item(self,request):
        all = FormB(request.POST,request.FILES)
        if all.is_valid():
            query = Item.objects.filter(title=request.POST['title'])
            if query:
                messages.error(request, 'Error Tittle Already Existed')
                return redirect('HOME')

            data = Item(title=request.POST['title'],Description=request.POST['Description'],Price=request.POST['Price'],
                       Picture=request.FILES['Image'], Time = datetime.now(), Quantity = request.POST['Quantity'])
            Item.save(data)
            # Sell_Price = ceil(int(request.POST['Price']) * 0.1) + int(request.POST['Price'])
            Sell_Price = ceil(float(request.POST['Price']))
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
                rated = False
                se = False
                User = False
                L = False
            All = Item.objects.filter(title=pk)
            All1 = Stock.objects.filter(title=pk)
            comments = Comment.objects.filter(title=pk)
            if request.session.has_key('user'):
                comments_once = Comment.objects.filter(title=pk, commenter=request.session['user'])
            else:
                comments_once = []
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

            C_E =len(slider_items)
            Data = {'L':L, 'All':All, 'comments':comments,'form':form,'All1':All1, 'check': se,'User': User, 'Rated': rated, 'R_star':R_star, 'slider_items':slider_items,
                    'C_E':C_E, 'comments_once':len(comments_once)}
        except Exception as e:
            return HttpResponse(e)
        return render(request,'Shopping/Detail1.html',Data)

    def comment(self, request, pk):
        if request.session.has_key('user'):
            if request.method=='POST':
                comment = request.POST['com']
                title = pk
                Data = Comment(title=title,comment=comment,commenter=request.session['user'])
                Comment.save(Data)
                return redirect('Details1', pk=pk)
            return redirect('HOME')
        else:
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
            Total = ceil(float(Quantity) * float(Price))
            Data = Cart(title=title,Price=Price,Quantity=Quantity,Total=Total, user=user)
            Data.save()
            return redirect('Details1', pk=title)


class Log:
    def signup(self,request):
        if request.session.has_key('user'):
            return redirect('HOME')
        else:
            form=FormA()
            R = request.META.get('HTTP_REFERER')
            Data = {'form':form, 'signup':True, 'R':R}
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
                return redirect(request.POST['next'])
        return redirect('signup')

    def login(self,request):
        if request.session.has_key('user'):
            return redirect('HOME')
        else:
            R = request.META.get('HTTP_REFERER')
            form=FormA()
            Data = {'form':form, 'signup':False, 'R':R}
            return render(request, 'Shopping/login.html', Data)

    def check(self,request):
        All = Logs.objects.all()
        if request.method == 'POST':
            E=request.POST['Email']
            P=request.POST['Password']
            for i in range(0,len(All)):
                if All[i].Email==E and All[i].Password==P:
                    request.session['user'] = str(All[i].Email).split('@')[0]
                    if 'admin' == request.session['user']:
                        return redirect('HOME')
                    return redirect(request.POST.get('next'))
            return redirect('login')

    def logout(self, request):
        if request.session['user'] == 'admin':
            R = 'HOME'
        else:
            R = request.META.get('HTTP_REFERER')
        del request.session['user']
        # messages.error(request,'You are Logged Out')
        return redirect(R)


class StockManage:
    available = 0
    sell = 0

    def stock(self, request):
        if request.method == 'POST':
            name = request.POST['title']
            # sell_rate = request.POST['Price']
            available = request.POST['Quantity']
            buy_rate = request.POST['buy']
            d = Stock.objects.get(title=name)
            d.title = name
            d.Buy_rate = buy_rate
            d.Available = available
            # d.Sell = sell_rate
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
        try:
            Rating.objects.get(item=name).delete()
        except:
            pass
        try:
            RecommendedSearch.objects.get(title=name).delete()
        except:
            pass
        try:
            RecommendedAdmin.objects.get(title=name).delete()
        except:
            pass
        try:
            RecommendedRating.objects.get(title=name).delete()
        except:
            pass
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
        R_S = request.META.get('HTTP_REFERER')
        messages.error(request, f'{name} Added in Recommended List')
        return redirect(R_S)

    def del_R_A(self,request,name):
        RecommendedAdmin.objects.filter(title=name).delete()
        R = Item.objects.get(title=name)
        R.Recommended = False
        R.save()
        R_S = request.META.get('HTTP_REFERER')
        messages.error(request, f'{name} Removed from Recommended List')
        return redirect(R_S)
