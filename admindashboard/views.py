from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from orders.models import Order
from products.models import Item, Category, Color
from ecommerce.mixins import SuperuserRequiredMixin
from django.views.generic import View, CreateView, ListView, UpdateView, DeleteView
from .forms import ItemForm, CategoryForm, ColorForm
from .models import Contact
from django.contrib import messages
# Create your views here.

class Orders(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            'orders': Order.objects.filter(confirm=True).order_by('-timestamp')
        }
        return render(request, "admin_orders.html", context=data)


class OrdersDetail(SuperuserRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        data = {
            'order': Order.objects.get(pk=pk)
        }
        return render(request, "admin_orders_detail.html", context=data)

class Items(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form':ItemForm
        }
        return render(request, 'admin_item_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('a:item-list')
        context = {
            'form':ItemForm(request.POST, request.FILES)
        }
        messages.error(request, 'some error')
        return render(request, 'admin_item_create.html', context)


class ItemUpdate(SuperuserRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {
            'form':ItemForm(instance=Item.objects.get(pk=pk))
        }
        return render(request, 'admin_item_update.html', context)

    def post(self, request, pk,  *args, **kwargs):
        form = ItemForm(request.POST, request.FILES, instance=Item.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            return redirect('a:item-list')
        context = {
            'form':ItemForm(request.POST, request.FILES)
        }
        return render(request, 'admin_item_update.html', context)
    



class ItemsDisplay(SuperuserRequiredMixin, ListView):
    model = Item
    template_name = 'admin_item_list.html'
    context_object_name = 'items'



class ItemDelete(SuperuserRequiredMixin, DeleteView):
    model = Item
    template_name = 'admin_item_delete.html'
    success_url = reverse_lazy('a:item-list')

class OrdersDelete(SuperuserRequiredMixin, DeleteView):
    model = Order
    template_name = 'admin_order_delete.html'
    success_url = reverse_lazy('a:dashboard')



class ContactsList(SuperuserRequiredMixin, ListView):
    model = Contact
    template_name = 'admin_contacts_list.html'
    fields = ['email','name','timestamp']
    context_object_name = 'contacts'
    ordering = ['-timestamp']


class ContactsDetail(SuperuserRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        data = {
            'contact': Contact.objects.get(pk=pk)
        }
        return render(request, "admin_contacts_detail.html", context=data)


class AddColor(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form':ColorForm
        }
        return render(request, 'admin_color_create.html', context)

    def post(self, request, *args, **kwargs):
        form = ColorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('a:colors')
        context = {
            'form':ColorForm(request.POST)
        }
        return render(request, 'admin_color_create.html', context)


class Colors(SuperuserRequiredMixin, ListView):
    model = Color
    template_name = 'admin_colors_list.html'
    context_object_name = 'colors'