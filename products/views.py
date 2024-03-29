from django.shortcuts import render
from . models import Item, Category, Cart, Cartitem
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from ecommerce.mixins import LoginRequiredMixin
from admindashboard.forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings
import requests
import json
from django.urls import reverse

# Create your views here.


class ProductsList(ListView):
    template_name = 'home.html'
    model = Item
    paginate_by = 8
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('a:dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super(ProductsList, self).get_queryset()
        q1 = queryset.filter(label='N')  # 
        return q1

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context['p1'] = Category.objects.get(name="Tops & Blouses")
        context['p2'] = Category.objects.get(name="Dresses")
        context['p3'] = Category.objects.get(name="Jumpsuits")
        context['p4'] = Category.objects.get(name="Co ord's")
        context['p5'] = Category.objects.get(name="Bottoms")
        context['p6'] = Category.objects.get(name="Winter")
        return context



class All_ProductsList(ListView):
    template_name = 'all_product.html'
    model = Item
    paginate_by = 20
    context_object_name = 'products'
    title = 'All'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('a:dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super(All_ProductsList, self).get_queryset()
        c = self.request.GET.get('c',None)
        if c is not None:
            queryset = queryset.filter(category__pk=c)
            self.title = Category.objects.get(pk=c).name
        name = self.request.GET.get('name',None)
        if name is not None:
            queryset1 = queryset.filter(title__icontains=name)
            queryset2 = queryset.filter(category__name__icontains=name)
            queryset4 = queryset.filter(description__icontains=name)
            queryset = (queryset1 | queryset2 | queryset4).distinct()
            self.title = "Results for '"+ name +"'"
        label = self.request.GET.get('l',None)
        if label is not None:
            queryset = queryset.filter(label=label)
            self.title = 'New Arrivals'
        n = self.request.GET.get('n',None)
        if n is not None:
            if n == 'C':
                queryset = super(All_ProductsList, self).get_queryset()
                categories = ['Tops & Blouses','Dresses', 'Jumpsuits', "Co ord's", 'Bottoms', 'Winter']
                self.title = 'All Clothing'
                queryset = queryset.filter(category__name__in = categories)
            if n == 'A':
                queryset = super(All_ProductsList, self).get_queryset()
                categories = ['Footwear','Bags', 'Jewellery']
                self.title = 'All Accessories'
                queryset = queryset.filter(category__name__in = categories)
        queryset = queryset.order_by('title')
        s = self.request.GET.get('s',None)
        if s is not None:
            if s == 'atoz':
                queryset = queryset.order_by('title')
            if s == 'ztoa':
                queryset = queryset.order_by('-title')
            if s == 'p1':
                queryset = queryset.order_by('price')
            if s == 'p2':
                queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(All_ProductsList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = self.title
        return context





class CartList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        data = {
            'cart_items':user_cart.cartitem_set.all(),
            'total_price':user_cart.get_total_price()
        }
        return render(request, 'order_summary.html', context=data)



class ProductDetail(View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Item, pk=pk)
        
        return render(request, 'product_detail.html', {'product': product})

class AddToCart(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item = Item.objects.get(pk=(request.POST.get('pk')))
        if not item.is_in_stock:
            messages.error(request, 'Item Out of stock')
            return redirect('products:product_detail', pk=item.pk)
        size = request.POST.get('size',None)
        color = request.POST.get('color',None)
        quantity = int(request.POST.get('quantity','1'))
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        if size is not None:
            if color is not None:
                cart_item = user_cart.cartitem_set.all().filter(item=item, size=size, color=color)
            else:
                cart_item = user_cart.cartitem_set.all().filter(item=item, size=size)
        else:
            if color is not None:
                cart_item = user_cart.cartitem_set.all().filter(item=item, color=color)
            else:
                cart_item = user_cart.cartitem_set.all().filter(item=item)


        if cart_item.exists():
            cart_item = cart_item.first()
            for i in range(quantity):
                cart_item.increment()
            cart_item.save()
        else:
            if size is not None:
                if color is not None:
                    cart_item = Cartitem.objects.create(item=item, size=size ,cart=user_cart, color=color, quantity=quantity)
                else:
                    cart_item = Cartitem.objects.create(item=item, size=size ,cart=user_cart, quantity=quantity)
            else:
                if color is not None:
                    cart_item = Cartitem.objects.create(item=item, cart=user_cart, color=color, quantity=quantity)
                else:
                    cart_item = Cartitem.objects.create(item=item ,cart=user_cart, quantity=quantity)

        messages.info(request, 'Item is added to your cart')
        return redirect('products:cart')

class IncrementCart(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        cart_item = Cartitem.objects.get(pk=pk)
        if not cart_item.item.is_in_stock:
            cart_item.delete()
            messages.error(request, 'Item Out of stock')
            return redirect('products:cart')
        
        cart_item.increment()
        cart_item.save()
        messages.info(request, 'Item has been added to your cart')
        return redirect('products:cart')

class DecrementCart(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        cart_item = Cartitem.objects.get(pk=pk)
        if not cart_item.item.is_in_stock:
            cart_item.delete()
            messages.error(request, 'Item Out of stock')
            return redirect('products:cart')
        cart_item.decrement()
        cart_item.save()
        if cart_item.quantity == 0:
            cart_item.delete()
        messages.info(request, 'Item has been removed from your cart')
        return redirect('products:cart')


class DeleteFromCart(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        cart_item = Cartitem.objects.get(pk=pk)
        cart_item.delete()
        messages.info(request, 'Item has been removed from your cart')
        return redirect('products:cart')

class ContactFormPage(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form':ContactForm,
        }
        return render(request, 'contact_us.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save()
        context = {
            'form':form
        }
        return render(request, 'contact_us.html', context)


def Terms_Condition(request):
    return render(request, 'terms_condition.html')


def Privacy_Policy(request):
    return render(request, 'privacy_policy.html' )

def about_us(request):
    return render(request, 'about_us.html')

def return_refund(request):
    return render(request, 'return_refund.html')

def exchange(request):
    return render(request, 'exchange.html')

def size(request):
    return render(request, 'size.html')

def how_to_buy(request):
    return render(request, 'how_to_buy.html')































