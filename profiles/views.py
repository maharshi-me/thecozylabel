from django.shortcuts import render
from django.views.generic import View
from orders.models import Order, Orderitem
from ecommerce import mixins

# Create your views here.

class Profile(mixins.LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request,'profile.html')

class CustomerOrders(mixins.LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(customer=request.user, confirm=True).order_by('-timestamp')
        context = {
            'orders':orders,
        }
        return render(request, 'customer_orders.html', context)


class CustomerOrderDetail(mixins.LoginRequiredMixin, mixins.CustomerRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        context = {
            'order':order,
        }
        return render(request, 'customer_order_detail.html', context)