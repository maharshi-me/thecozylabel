from django import forms
from products.models import Item, Category, Carousel
from .models import Contact

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = ['image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email','name','message','image']


        