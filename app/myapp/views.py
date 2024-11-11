from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from . models import Product
from django.db.models import Count



# Create your views here.
def home(request):
    return render(request, "myapp/home.html")
   
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
