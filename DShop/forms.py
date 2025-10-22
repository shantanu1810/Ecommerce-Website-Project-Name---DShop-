from django import forms
from .models import Products

class productsadd(forms.ModelForm):
    class Meta:
        model = Products
        fields=['product_id','name','price','description','image','product_type','brand','sub_type']