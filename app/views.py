from django.shortcuts import render
from .models import *
from django.http import JsonResponse
# Create your views here.
def homepage(request):
    return render(request,"home.html")

def about(req):
    return render(req,"about.html")

def contact(req):
    return render(req,"contact.html")

def loginpage(req):
    return render(req,"login.html")

def register(req):
    countries = Countries.objects.all()
    return render(req,"register.html",{'countries': countries})

def forgotpassword(req):
    return render(req,"forgot.html")

def address(req):
    countries = Countries.objects.all()
    return render(req,"adress.html",{'countries': countries})

def states(req,id):
    states = States.objects.filter(country_id=id).values('id','state_name')
    return JsonResponse(list(states),safe=False)
def districts(req,id):
    districts = Districts.objects.filter(state_id=id).values('id','district_name')
    return JsonResponse(list(districts),safe=False)
def get_products(req):
    products = Products.objects.all()
    return render(req,"products.html",{'products': products})
def get_product(req,slug):
    product = Products.objects.get(slug=slug)
    return render(req,"product.html",{'product': product})