from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Order, Orderitem, Shipping_Details
from django.views.decorators.csrf import csrf_exempt
from products.models import Cart
from .paytm import Checksum
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from ecommerce.mixins import LoginRequiredMixin, CustomerRequiredMixin, ActiveOrderRequiredMixin
import requests
import json
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import Settings



# Create your views here.
class Checkout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_cart = Cart.objects.get(user=request.user)
        shipping = Shipping_Details.objects.filter(user=request.user).last()
        for cart_item in user_cart.cartitem_set.all():
            if not cart_item.item.is_in_stock:
                cart_item.delete()
        if len(user_cart.cartitem_set.all()) == 0:
            messages.error(request, 'Item Out of stock')
            return redirect('products:cart')
        data = {
            'cart' : Cart.objects.get(user=request.user),
            'items' : user_cart.cartitem_set.all(),
            'shipping':shipping

        }
        return render(request, 'checkout.html', context=data)
        
    def post(self, request, *args, **kwargs):
        obj = Shipping_Details.objects.create(user=request.user)
        obj.first_name = request.POST.get('first_name','')
        obj.last_name = request.POST.get('last_name','')
        obj.email = request.POST.get('email','')
        obj.phone = request.POST.get('phone1','')
        obj.zipcode = request.POST.get('zipcode','')
        obj.city = request.POST.get('city','')
        obj.state = request.POST.get('state','')
        obj.address1 = request.POST.get('address1','')
        obj.address2 = request.POST.get('address2','')
        obj.save()
            
        #Create an order with the shipping details we created above 
        order = Order.objects.create(
            customer = request.user,
            shipping_details = obj,
            order_id = Order.objects.create_new_id(),
        )


        user_cart = Cart.objects.get(user=request.user)
        for cart_item in user_cart.cartitem_set.all():
            if not cart_item.item.is_in_stock:
                cart_item.delete()
        user_cart = Cart.objects.get(user=request.user)
        if len(user_cart.cartitem_set.all()) == 0:
            messages.error(request, 'Item Out of stock')
            return redirect('products:cart')
        user_cart = Cart.objects.get(user=request.user)
        for cart_item in user_cart.cartitem_set.all():
            if not cart_item.item.is_in_stock:
                cart_item.delete()
        user_cart = Cart.objects.get(user=request.user)

        for cart_item in user_cart.cartitem_set.all():
            Orderitem.objects.create(
                item = cart_item.item,
                order = order,
                size = cart_item.size,
                quantity = cart_item.quantity,
                price_each = cart_item.get_item_final_price_single(),
                price_total = cart_item.get_item_final_price(),
            )
        order.update_total()
        order.save()
        return redirect('orders:confirm-order', pk=order.pk)


class ConfirmOrder(LoginRequiredMixin, CustomerRequiredMixin, ActiveOrderRequiredMixin ,View):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        if len(order.orderitem_set.all()) == 0:
            order.delete()
            messages.error(request, 'Item Out of stock')
            return redirect('products:cart')
        for oitem in order.orderitem_set.all():
            if not oitem.item.is_in_stock:
                order.delete()
                messages.error(request, 'Item Out of stock')
                return redirect('products:cart')
        data = {
            'order':order
        }
        return render(request, 'confirm-order.html', context=data)
    
    def post(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        if len(order.orderitem_set.all()) == 0:
            order.delete()
            messages.error(request, 'Item Out of stock')
            return redirect('products:cart')
        for oitem in order.orderitem_set.all():
            if not oitem.item.is_in_stock:
                order.delete()
                messages.error(request, 'Item Out of stock')
                return redirect('products:cart')
        order.confirm=True
        order.save()
        user_cart = Cart.objects.get(user=request.user)
        param_dict = {
        'MID': settings.MID,
        'ORDER_ID':str(order.order_id),
        'CUST_ID': str(order.customer.email),
        'TXN_AMOUNT': str(order.total),
        'CHANNEL_ID': 'WEB',
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': settings.WEBSITE, 
        'CALLBACK_URL': settings.CALLBACK_URL
        }
        param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict, settings.MERCHANT_KEY )
        return render(request, 'paytm.html', {'param_dict':param_dict})





@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i =='CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, settings.MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            order = Order.objects.get(order_id=response_dict['ORDERID'])
            order.is_paid = True 
            order.save()
            message = '[The Cozy Label]: Thanks for shopping with us! We have received your payment of Rs.' + str(order.total) + ' for order no - ' + str(response_dict['ORDERID'])
            user_cart = Cart.objects.get(user=order.customer)
            user_cart.delete()
           
            
            
            # Generate pdf Invoice
            # html = render_to_string('pdf.html', {'order':order})
            # out = BytesIO()
            # stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +'/css/pdf.css')]
            # weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            link = settings.FULL_DOMAIN_NAME + "/profile/your-orders/" + str(order.pk) + '/'
            subject = 'New order from The Cozy Label'
            email_message = 'Thank you for shopping in TheCozyLabel. Your order details can be viewed here: ' + link
            from_email = settings.DEFAULT_FROM_EMAIL
            to = order.customer.email
            email = EmailMessage(subject,email_message, from_email, [to])
            # email.attach('invoice.pdf',out.getvalue(), 'application/pdf')
            email.send()
            messages.success(request, "Order Placed Successfully.")
        else:
            messages.error(request, "Something went wrong. Please try again")
    order = Order.objects.get(order_id = response_dict['ORDERID'])
    order.payment_status = response_dict['STATUS']
    try:
        order.transaction_id = response_dict['TXNID']
    except:
        pass
    order.save()
    return redirect('profile:your-orders')

































