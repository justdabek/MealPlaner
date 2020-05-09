from django.shortcuts import render
from datetime import datetime
from .models import Product

def index(request):
    context = {
        'current_date':datetime.now(),
        'title':'Home'
    }
    return render(request,'index.html',context)

def products(request):
    populate_db()
    products=get_products()
    context = {
        'products':products,
        'current_date':datetime.now(),
        'title':'Product list'
    }
    return render(request, 'products.html', context)

def get_products():
    result=Product.objects.all()
    return result

def populate_db():
    if Product.objects.count()==0:
        Product(name='Jogurt',kcalPer100g=80,proteinsPer100g=0.2,fiberPer100g=0.1,fatPer100g=10).save()
        Product(name='Chleb',kcalPer100g=30,proteinsPer100g=0.2,fiberPer100g=1.1,fatPer100g=64).save()
        Product(name='Jajka',kcalPer100g=10,proteinsPer100g=0.3,fiberPer100g=0.1,fatPer100g=7).save()
        Product(name='Mleko',kcalPer100g=70,proteinsPer100g=5.2,fiberPer100g=3.1,fatPer100g=56).save()
        Product(name='Pomidor',kcalPer100g=8,proteinsPer100g=4.2,fiberPer100g=0.1,fatPer100g=4).save()
