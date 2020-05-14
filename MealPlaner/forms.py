from django import forms
from .models import Product, Goal, Breakfast, Lunch, Dinner

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('name','kcalPer100g','proteinsPer100g','fiberPer100g','fatPer100g')

class SignUpForm(forms.Form):
    username=forms.CharField(max_length=100, required=True)
    email=forms.EmailField(required=True)
    password=forms.CharField(widget=forms.PasswordInput())

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attr={
            'class':'form-control'
        }
        self.fields['email'].widget.attr={
            'class':'form-control'
        }
        self.fields['password'].widget.attr={
            'class':'form-control'
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = [
            'activity',
            'age',
            'sex',
            'height_cm',
            'target_weight',
        ]
# class MealForm(forms.ModelForm):
#     products=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Product.objects.all())
#     class Meta:
#         model=Meal
#         fields=('date','typeOfMeal','products')

class BreakfastForm(forms.ModelForm):
    products=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Product.objects.all())
    class Meta:
        model=Breakfast
        fields=('products',)

class LunchForm(forms.ModelForm):
    products=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Product.objects.all())
    class Meta:
        model=Lunch
        fields=('products',)

class DinnerForm(forms.ModelForm):
    products=forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Product.objects.all())
    class Meta:
        model=Dinner
        fields=('products',)