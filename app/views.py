from django.shortcuts import render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages


class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})

        
class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add})

def orders(request):
 return render(request, 'app/orders.html')


def mobile(request,data=None):
    if data==None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'Vivo' or data == 'Oppo' or data == 'Realme' or data == 'Iphone' or data == 'Nokia' or data == 'Techno':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'Above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})


def topwear(request,data=None):
    if data==None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Full-shirt' or data == 'Half-shirt' or data == 'T-shirt' or data == 'Other':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'Below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data == 'Above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/topwear.html',{'topwears':topwears})

def bottomwear(request,data=None):
    if data==None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Jeans' or data == 'Formal' or data == 'Casual' or data == 'Nikkar' or data == 'Other':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'Below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data == 'Above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=500)
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})

def login(request):
 return render(request, 'app/login.html')


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You Are Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})


def checkout(request):
 return render(request, 'app/checkout.html')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg= Customer(user=usr,name=name, locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulation!! Profile Updated Successfully')
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})


# def passwordchange(request):
#     return render(request,'app/passwordchange.html')
