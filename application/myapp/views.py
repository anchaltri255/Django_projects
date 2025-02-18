from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from . models import Product, Cart, Customer
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from . forms import CustomerProfileForm 
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json
from .models import Order, OrderItem  # Ensure these models exist or create them

# Create your views here.

def home(request):
    return render(request, "myapp/home.html")

def about(request):
    return render(request, "myapp/about.html")

def all_category(request):
    return render(request,"myapp/all_category.html")

def contact(request):
    return render(request, "myapp/contact.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect( '/login/')


        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:   
            login(request, user)
            return render(request, 'myapp/home.html')
        

    return render(request, 'myapp/login.html')


def logout_page(requset):
    logout(requset)
    return redirect('/login/')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Congratulations! User Register Successfully')
        return render(request, 'myapp/register.html')
    return render(request, 'myapp/register.html')

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('prod_id')
        try:
            product = Product.objects.get(id=product_id)
            Cart.objects.create(user=request.user, product=product)
            # return redirect('/cart')
            return JsonResponse({"message": "Product added to cart successfully!"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product added to cart successfully!"}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400) 

def show_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('prod_id')
        try:
            product = Product.objects.get(id=product_id)
            Cart.objects.create(user=request.user, product=product)
            
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product does not exist."}, status=404)
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount = amount+value
    totalamount = amount + 40
    return render(request,'myapp/add_to_cart.html',locals()) 

def update_cart_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')

        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                return JsonResponse({"status": "error", "message": "Invalid action or quantity cannot be less than 1."}, status=400)

            cart_item.save()

            # Recalculate total amounts
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            total_amount = amount + 40  # Add shipping

            return JsonResponse({
                "status": "success",
                "new_quantity": cart_item.quantity,
                "new_amount": amount,
                "new_total": total_amount
            })
        except Cart.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cart item does not exist."}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

def remove_from_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get('product_id')  # Ensure this key matches the JS payload

        if product_id:
            try:
                cart_item = Cart.objects.get(user=request.user, product_id=product_id)
                cart_item.delete()
                return JsonResponse({"status": "success", "message": "Item removed successfully"})
            except Cart.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Product does not exist in your cart."}, status=404)
        return JsonResponse({"status": "error", "message": "Invalid product ID"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def place_order(request):
    if request.method == "POST":
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            return JsonResponse({"message": "Cart is empty, cannot place order."}, status=400)

        # Create an order
        order = Order.objects.create(user=user, total_amount=0)
        
        total_amount = 0
        for item in cart_items:
            total_price = item.quantity * item.product.discounted_price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=total_price
            )
            total_amount += total_price

        # Update the order with the total amount
        order.total_amount = total_amount + 40  # Add shipping
        order.save()

        # Clear the user's cart
        cart_items.delete()

        return JsonResponse({"message": "Order placed successfully!", "status": "success"})

    return JsonResponse({"message": "Invalid request method", "status": "error"})

def orders(request):
    user = request.user
    if user.is_authenticated:
        
        user_orders = Order.objects.filter(user=user)
        return render(request, 'myapp/orders.html', {'orders': user_orders})
    else:
        return HttpResponse("You need to log in to view your orders.", status=401)

def order_view(request):
    orders = Order.objects.all()  
    return render(request, 'your_template.html', {'orders': orders})


def search_view(request):
    query = request.GET.get('q', '')  
    products = Product.objects.all()

    if query:
        # Filter products based on the search query
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'shop/search_results.html', {'products': products, 'query': query})


class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        tittle = Product.objects.filter(category=val).values('tittle')

        return render(request, "myapp/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(tittle=val)
        tittle = Product.objects.filter(category=product[0].category).values('tittle')
        return render(request, "myapp/category.html",locals())


class  ProductDetail(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, "myapp/productdetail.html",locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'myapp/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            locality = form.cleaned_data['locality']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,city=city,locality=locality,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'myapp/profile.html',locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'myapp/address.html',locals())

class checkout(View):
    def get(self, request):
        return render(request,'myapp/checkout.html',locals())

class UpdateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'myapp/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")

        return redirect("address")
    


