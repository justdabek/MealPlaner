from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from .models import Product, Goal, Breakfast, Lunch, Dinner
from .forms import ProductForm, SignUpForm, GoalForm, BreakfastForm, LunchForm, DinnerForm
from datetime import datetime, timedelta

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
    return render(request,'login.html',{'current_date':datetime.now()})

@login_required(redirect_field_name='login')
def change_password(request):
    if request.POST:
        user=request.user
        password=request.POST.get('password',None)
        if password:
            user.set_password(password)
            user.save()
        return redirect('index')

    return render(request,'change_password.html', {'current_date':datetime.now()})

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
        'form':form,
        'current_date': datetime.now(),
    }

    return render(request,'forms/product.html',context)

def product_delete(request,pk):
    p = Product.objects.get(id=pk)
    p.delete()
    return redirect('/products/')

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

def goal_view(request):
    flag_goal_registered = False

    form = GoalForm()
    
    #     form = GoalForm(request.POST)       # get to get dict value
    #     print(form.cleaned_data)
    #     Goal.objects.create(**form.cleaned_data)
    # else:
    #     print(form.errors)

    form = GoalForm(request.POST or None)
    user_goal = Goal()

    all_obj = Goal.objects.all()
    print("------------")
    print(all_obj)
    # print("all_obj[1]: ", all_obj[1])

    
    for x in all_obj:
        print(x.activity)
        print(x.user_id)
        print(request.user)
        print(str(request.user) == str(x.user_id))
        if str(x.user_id) == str(request.user):
            print("Username known")
            flag_goal_registered = True
            user_goal = x
            user_goal.get_kcal_needed()

    print("form activity", form['activity'])
    print(flag_goal_registered)

    if flag_goal_registered == True:
            
        # form = GoalForm({'activity': user_goal.activity,
        #                 'age': user_goal.age,
        #                 'sex': user_goal.sex,
        #                 'height_cm': user_goal.height_cm,
        #                 'target_weight': user_goal.target_weight
        #                 })
        print("FORM:", form)
        

    if form.is_valid():
        print(form.cleaned_data)
        print(form.cleaned_data['activity'])
        print('user:', request.user)
        
        if flag_goal_registered == False: 
            Goal.objects.create(**{"user_id":request.user},**form.cleaned_data)
        else:
            ### the goal already exists:
            Goal.objects.filter(user_id=request.user).update(
                activity=           form.cleaned_data['activity'],
                age=                form.cleaned_data['age'],
                sex=                form.cleaned_data['sex'],
                height_cm=          form.cleaned_data['height_cm'],
                target_weight=      form.cleaned_data['target_weight']
            )     

    if request.method == "POST":
        if "change_btn" in request.POST:
            if flag_goal_registered == True:
                Goal.objects.filter(user_id=request.user).delete()
                form = GoalForm(request.POST or None)
                flag_goal_registered = False
       

            # user_goal.save(**{"user_id":request.user},**form.cleaned_data)


        # user_goal.user_id = request.user
        # user_goal.activity = form.activity
        # user_goal.age = form.age
        # user_goal.sex = form.sex 
        # user_goal.height_cm = form.height_cm
        # user_goal.target_weight = form.target_weight 
        # user_goal.save()

        # form.save()
        # form = GoalForm()

    context = {
        'form': form,
        'user_goal': user_goal,
        'flag_goal_registered': flag_goal_registered,
    }
    return render(request, 'goal.html', context)

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
