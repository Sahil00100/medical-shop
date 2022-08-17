from django.shortcuts import render,redirect
from.forms import UserForm
from django import forms
# Create your views here.
from django.contrib.auth.decorators import login_required
import datetime
from.models import Medicine,Cart,Order,RateAndReview
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import EmailMessage,send_mail,BadHeaderError
from django.contrib import messages
#index page views
def index_view(request):
    if request.method=="POST":
        search=request.POST.get('search')
        print(search)
        product=Medicine.objects.filter(Q(name__contains=search))
        return render(request,'search.html',{'product':product,'media_url':settings.MEDIA_URL})
   
    latest=Medicine.objects.order_by('-id')[:3]
    return render(request, 'index.html',{'latest':latest,'media_url':settings.MEDIA_URL,})


#registration

def register_view(request):
    print(1)
    if request.method=='POST':
        print(2)
        form=UserForm(request.POST)
        if form.is_valid():
            print(3)
            user=form.create_user()
            user.save()
            return redirect('login')
        else:
            print('failed')
    else:
        form=UserForm()
    return render(request, 'register.html',{'form':form})

#login

def login_view(request):
    if request.method=="POST":
        username=request.POST.get('email')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            print('invalid username or password')    
    return render(request,'login.html',{})

#log out
def logout_view(request):
    logout(request)
    print('logout success!')
    return redirect('login')

#single product
def single_product_view(request,id):
    
    if request.method=="POST":
        if request.user.is_authenticated:
            print(1212)
            rate=request.POST.get('rate')
            review=request.POST.get('review')
            product=Medicine.objects.get(id=id)
            user=User.objects.get(username=request.user)
            
            if RateAndReview.objects.filter(product=product,user=user).exists():
                    print('testing///')
                    update=RateAndReview.objects.get(
                        product=product,
                        user=user
                        )
                    if rate=='0':
                        print('hei')
                        messages.add_message(
                        request,
                        messages.INFO,
                        'please do rate and review both'
                        )
                        
                        return redirect('product',id=id)
                    else:
                        print('hello')
                        update.rate=rate
                        update.review=review
                        update.save()
                        return redirect('product',id=id)             
            else:
                
                q=RateAndReview(
                    product=product,
                    user=user,
                    rate=rate,
                    review=review
                )
                q.save()
                return redirect('product',id=id)

        else:
            return redirect('login')

    product=Medicine.objects.get(id=id)
    
    #rate and review showing
    review=RateAndReview.objects.filter(product=product).order_by('-id')
    r=RateAndReview.objects.filter(product=product)
    length=len(r)
    sume=0

    for x in r:
        y=x.rate
        sume=sume+y

    if length==0:
        length=1
        rate=sume/length
    else:
        rate=sume/length
        rate=int(rate)
    print(rate)    
    
    return render(request,'single-product.html',{'product':product,'media_url':settings.MEDIA_URL,'rate':rate,'review':review})

@login_required(login_url='login')
def cart_view(request):
    cart=Cart.objects.filter(user=request.user).order_by('-id')
    sume=0
    for x in cart:
        y=x.product.price
        y=int(y)
        sume=sume+y
    print(sume)

    if request.method=="POST":
        print('yes')
        user=User.objects.get(username=request.user)
        cart=Cart.objects.filter(user=request.user)
        
                    
        name=request.POST['name']
        #price=request.POST['price']
        mobile_no=request.POST['mobile']
        pincode=request.POST['pincode']
        house=request.POST['house']
        street=request.POST['street']
        landmark=request.POST['landmark']
        town=request.POST['town']
        state=request.POST['state']
        date=datetime.datetime.today()

        for x in cart:
            y=x.product
            p=x.product.price
            Order.objects.get_or_create(
                user=user,
                product=y,
                name=name,
                price=p,
                mobile_no=mobile_no,
                pincode=pincode,
                house=house,
                street=street,
                landmark=landmark,
                town=town,
                state=state,
                date=date,
            )
            c=Cart.objects.filter(user=request.user)
            for x in c:
                x.delete()
        return redirect('index')
    else:
        print('nothing')
    return render(request,'cart.html',{'cart':cart,'media_url':settings.MEDIA_URL,'total':sume})
login_required(login_url='login')
def cart_adder(request,id):
    x=True
    if x==True:
        cart=Cart.objects.filter(user=request.user).order_by('-id')
        product=Medicine.objects.get(id=id)
        cart_product=Cart.objects.filter(product=product)
        user=User.objects.get(username=request.user)
        save_cart=Cart.objects.get_or_create(
            user=user,
            product=product,
        )
        return redirect('cart')
    else:
        print('something wrong')
    return render(request,'cart.html',{'cart':cart,'media_url':settings.MEDIA_URL})


@login_required(login_url='login')
def orders_view(request):
    orders=Order.objects.all()
    return render(request,'orders1.html',{'orders':orders,'media_url':settings.MEDIA_URL})


def search_view(request):

    if request.method=="POST":
        search=request.POST.get('search')
        print(search)
        product=Medicine.objects.filter(Q(name__contains=search))
        return render(request,'search.html',{'product':product,'media_url':settings.MEDIA_URL})
   
       
    else:
        product=Medicine.objects.all()    

        return render(request,'search.html',{'product':product,'media_url':settings.MEDIA_URL})

def delete(request,id):

    product=Cart.objects.get(id=id)
    product.delete()
    return redirect('cart')
