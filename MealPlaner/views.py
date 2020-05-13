from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Product, Breakfast, Lunch, Dinner
from .forms import ProductForm, SignUpForm, BreakfastForm, LunchForm, DinnerForm


def index(request):
    auth = True
    if not request.user.is_authenticated:
        auth = False

    context = {
        'current_date':datetime.now(),
        'title':'Home',
        'auth':auth
    }
    return render(request, 'index.html', context)




def login_user(request,user):
    login(request,user)
    return True

def logout_view(request):
    logout(request)
    return redirect('login')

def signUp(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(is_staff=True,is_active=True,**form.cleaned_data)
            messages.success(request,"Your account has been created")
            if login_user(request,user):
                return redirect('index')
    else:
        form= SignUpForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Check your user name and password")
    return render(request,'login.html')

@login_required(redirect_field_name='login')
def change_password(request):
    if request.POST:
        user=request.user
        password=request.POST.get('password',None)
        if password:
            user.set_password(password)
            user.save()
        return redirect('index')
    return render(request,'change_password.html')

def products(request,pk='None'):
    populate_db()
    products=get_products()

    context = {
        'products':products,
        'current_date':datetime.now(),
        'title':'Product list',
    }

    return render(request, 'products.html', context)

def product_single(request,pk):
    if (pk == 'new'):
        product = Product()
        form = ProductForm()
    else:
        product = Product.objects.get(id=pk)
        form=ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()

    context={
        'form':form
    }

    return render(request,'forms/product.html',context)

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

def meals(request,date):
    try:
        lunch = Lunch.objects.get(date=date)
        formLunch = LunchForm(instance=lunch)
    except:
        lunch = Lunch()
        formLunch = LunchForm()

    try:
        breakfast = Breakfast.objects.get(date=date)
        formBreakfast = BreakfastForm(instance=breakfast)

    except:
        breakfast = Breakfast()
        formBreakfast = BreakfastForm()

    try:
        dinner = Dinner.objects.get(date=date)
        formDinner = DinnerForm(instance=dinner)
    except:
        dinner = Dinner()
        formDinner = DinnerForm()

    if request.method == "POST" and 'btnbreakfast' in request.POST:
        form = BreakfastForm(request.POST, instance=breakfast)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.date = date
            meal.save()
            form.save_m2m()
            return redirect('/meals/'+date)

    if request.method == "POST" and 'btnlunch' in request.POST:
        form = LunchForm(request.POST, instance=lunch)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.date = date
            meal.save()
            form.save_m2m()
            return redirect('/meals/'+date)

    if request.method == "POST" and 'btndinner' in request.POST:
        form = DinnerForm(request.POST, instance=dinner)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.date = date
            meal.save()
            form.save_m2m()
            return redirect('/meals/'+date)


    # meal_currentdate=get_meals(date)
    context={
        'title':'Meals',
        'date':date,
        'prev_day_date': datetime.strptime(date, '%Y-%m-%d') + timedelta(days=-1),
        'next_day_date': datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1),
        'current_date': datetime.now(),
        'formBreakfast':formBreakfast,
        'formLunch':formLunch,
        'formDinner':formDinner
    }




    return render(request,'meals.html',context)

# def get_meals(date):
#     result=Meal.objects.filter(date=date)
#     return result