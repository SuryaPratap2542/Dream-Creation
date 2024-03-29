from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404



class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops': laptops})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        cn=0
        if request.user.is_authenticated:
            user = request.user
            cn = Cart.objects.filter(user=user).count()
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops': laptops, 'cn': cn})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def addtocart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')
    else:
        # Handle other HTTP methods or provide a default response
        pass



@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        cn = Cart.objects.filter(user=user).count()
        # print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount, 'cn': cn})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
            totalamount = amount+shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        # print(data)
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
            amount = 0.0
            shipping_amount = 70.0
            cart_product = [
                p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount+shipping_amount
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        # print(data)
        return JsonResponse(data)


@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'Vivo' or data == 'Oppo' or data == 'Realme' or data == 'Iphone' or data == 'Nokia' or data == 'Techno':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=10000)
    elif data == 'Above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Full-shirt' or data == 'Half-shirt' or data == 'T-shirt' or data == 'Other':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'Below':
        topwears = Product.objects.filter(
            category='TW').filter(discounted_price__lt=500)
    elif data == 'Above':
        topwears = Product.objects.filter(
            category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/topwear.html', {'topwears': topwears})


def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Jeans' or data == 'Formal' or data == 'Casual' or data == 'Nikkar' or data == 'Other':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'Below':
        bottomwears = Product.objects.filter(
            category='BW').filter(discounted_price__lt=500)
    elif data == 'Above':
        bottomwears = Product.objects.filter(
            category='BW').filter(discounted_price__gt=500)
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})



def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Dell' or data == 'HP' or data == 'Asus' or data == 'Redmi' or data == 'Lenovo' or data == 'MacBook':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'Below':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__lt=50000)
    elif data == 'Above':
        laptops = Product.objects.filter(
            category='L').filter(discounted_price__gt=50000)
    return render(request, 'app/laptop.html', {'laptops': laptops})


def login(request):
    return render(request, 'app/login.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! You Are Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0

    cart_product = Cart.objects.filter(user=user)  # Use filter directly here

    for p in cart_product:
        tempamount = p.quantity * p.product.discounted_price
        amount += tempamount

    if amount > 500:
        totalamount = amount
    else:
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


@login_required
def payment_done(request):
    user = request.user

    if request.method == 'POST':
        custid = request.POST.get('custid')
        try:
            customer = Customer.objects.get(id=custid)
            cart = Cart.objects.filter(user=user)
            for c in cart:
                OrderPlaced(user=user, customer=customer,
                            product=c.product, quantity=c.quantity).save()
                c.delete()
            return redirect("orders")
        except Customer.DoesNotExist:
            messages.info(request, 'Please select an Address !')
            return redirect("checkout")

    return HttpResponseBadRequest("Invalid request method")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulation!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    

@method_decorator(login_required, name='dispatch')
class editAddress(View):
    def get(self, request, address_id):
        address = get_object_or_404(Customer, user=request.user, id=address_id)
        form = CustomerProfileForm(instance=address)
        return render(request, 'app/edit_address.html', {'form': form, 'address': address})
    
    def post(self, request, address_id):
        address = get_object_or_404(Customer, user=request.user, id=address_id)
        form = CustomerProfileForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address Updated Successfully')
            return redirect('address')  # Redirect to the address list page
        return render(request, 'app/edit_address.html', {'form': form, 'address': address})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Customer, user=request.user, id=address_id)
    if request.method == "POST":
        address.delete()
        messages.success(request, 'Address Deleted Successfully')
    return redirect('address')  # Redirect to the address list page


def explorer(request):
    products = Product.objects.all()
    return render(request, 'app/explorer.html', {'products': products})


# from django.db.models import Q  # Import Q from django.db.models


def search_results(request):
    query = request.GET.get('q')  # Get the user's search query from the URL parameters
    sort_option = request.GET.get('sort')  # Get the sorting option from the URL parameters
    price_option = request.GET.get('price')  # Get the price range option from the URL parameters

    if query:
        # Filter products based on the title containing the user's query
        search_results = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        
        if sort_option == 'low_to_high':
            # Sort the search results in ascending order of discounted price
            search_results = search_results.order_by('discounted_price')
        elif sort_option == 'high_to_low':
            # Sort the search results in descending order of discounted price
            search_results = search_results.order_by('-discounted_price')
        
        if price_option == 'above_500':
            # Filter search results for products with discounted price above 500
            search_results = search_results.filter(discounted_price__gt=500)
        elif price_option == 'below_500':
            # Filter search results for products with discounted price below or equal to 500
            search_results = search_results.filter(discounted_price__lte=500)

        # Prepare the context to be passed to the template for rendering
        context = {
            'query': query,
            'search_results': search_results,
        }
        return render(request, 'app/searchpage.html', context)
    
    # If there's no query, render the search page without any results
    return render(request, 'app/searchpage.html')


