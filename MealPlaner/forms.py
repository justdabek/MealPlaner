from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=('name','kcalPer100g','proteinsPer100g','fiberPer100g','fatPer100g')
