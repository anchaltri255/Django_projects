from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from . models import Product
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from . forms import CustomerProfileForm ,Customer


# Create your views here.

def home(request):
    return render(request, "myapp/home.html")

def about(request):
    return render(request, "myapp/about.html")

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
    return redirect('myapp/login/')


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

   
   
class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        tittle = Product.objects.filter(category=val).values('tittle')
        #count function is that we count the total title of that to respect to the title
        #if we don't want to repated title so we use annotate

        return render(request, "myapp/category.html",locals())
    #local is built-in-function to pass all the local variables from this function to the this category of html file


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

class UpdateAddress(View):
    def get(self, request,pk):
        form = CustomerProfileForm()
        return render(request,'myapp/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        return render(request,'myapp/updateAddress.html',locals())