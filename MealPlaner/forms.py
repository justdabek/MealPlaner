from django import forms
from .models import Product

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