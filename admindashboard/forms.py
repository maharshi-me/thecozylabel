from django import forms
from products.models import Item, Category
from .models import Contact

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email','name','message','image']


        