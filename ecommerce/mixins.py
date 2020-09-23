from orders.models import Order
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(request, 'Please Login first')
            return redirect('account_login')

class CustomerRequiredMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        if Order.objects.get(pk=pk).customer == request.user:
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            raise Http404

class ActiveOrderRequiredMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        if Order.objects.get(pk=pk).confirm == False:
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            raise Http404

class SuperuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
    
