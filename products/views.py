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
        context['p1'] = Item.objects.all().filter(category__name='Tops & Blouses')[:8]
        context['p1_pk'] = Category.objects.get(name="Tops & Blouses").pk
        context['p2'] = Item.objects.all().filter(category__name='Dresses')[:8]
        context['p2_pk'] = Category.objects.get(name="Dresses").pk
        context['p3'] = Item.objects.all().filter(category__name='Jumpsuits')[:8]
        context['p3_pk'] = Category.objects.get(name="Jumpsuits").pk
        context['p4'] = Item.objects.all().filter(category__name="Co ord's")[:8]
        context['p4_pk'] = Category.objects.get(name="Co ord's").pk
        context['p5'] = Item.objects.all().filter(category__name='Bottoms')[:8]
        context['p5_pk'] = Category.objects.get(name="Bottoms").pk
        context['p6'] = Item.objects.all().filter(category__name='Winter')[:8]
        context['p6_pk'] = Category.objects.get(name="Winter").pk
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
        quantity = int(request.POST.get('quantity','1'))
        if size is None:
            messages.error(request, 'Please select Size.')
            return redirect('products:product_detail', pk=item.pk)
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = user_cart.cartitem_set.all().filter(item=item, size=size)
        if cart_item.exists():
            cart_item = cart_item.first()
            for i in range(quantity):
                cart_item.increment()
            cart_item.save()
        else:
            cart_item = Cartitem.objects.create(item=item, size=size ,cart=user_cart, quantity=quantity)
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
            # subject = 'Submission Received'
            # message = form.cleaned_data['message']
            # email = form.cleaned_data['email']
            # name = form.cleaned_data['name']
            # msg = 'Name : ' + name + '\nEmail : ' + email + '\nMessage : ' + message
            # if c.image:
            #     msg = msg + '\nImage: https://www.yctees.in/' + c.image.url
            # try:
            #     mail = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
            #     mail.send()
            #     return redirect('products:list_products')
            # except:
            #     messages.error(request, 'Attachment is too big or corrupt. Please try again.')
            #     return render(request, 'contact_us.html', {'form': form})
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































